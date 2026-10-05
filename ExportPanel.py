#!/usr/bin/env python

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2016 execuc                                             *
# *                                                                         *
# *   This file is part of LCInterlocking module.                           *
# *   LCInterlocking module is free software; you can redistribute it and/or*
# *   modify it under the terms of the GNU Lesser General Public            *
# *   License as published by the Free Software Foundation; either          *
# *   version 2.1 of the License, or (at your option) any later version.    *
# *                                                                         *
# *   This module is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU     *
# *   Lesser General Public License for more details.                       *
# *                                                                         *
# *   You should have received a copy of the GNU Lesser General Public      *
# *   License along with this library; if not, write to the Free Software   *
# *   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,            *
# *   MA  02110-1301  USA                                                   *
# *                                                                         *
# ***************************************************************************

import FreeCAD
import FreeCADGui
import os
import math
import re
import Draft
import Part
import importDXF
from PySide import QtGui
from lasercut.helper import biggest_area_faces
from panel import selection

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(__dir__, 'icons')


PLANAR_NORMAL_TOLERANCE = 0.999
POCKET_DEPTH_TOLERANCE = 0.01
GEOMETRY_COMPARISON_TOLERANCE = 0.000001


def _normalized(vector):
    normalized = FreeCAD.Vector(vector.x, vector.y, vector.z)
    normalized.normalize()
    return normalized


def _is_planar_face(face):
    try:
        return face.Surface.__class__.__name__ == "Plane"
    except Exception:
        return False


def _planar_face_records(shape):
    records = []
    for index, face in enumerate(shape.Faces):
        if not _is_planar_face(face):
            continue
        try:
            normal = _normalized(face.normalAt(0, 0))
        except Exception:
            continue
        records.append({
            "face": face,
            "index": index,
            "normal": normal,
            "coordinate": face.CenterOfMass.dot(normal),
        })
    return records


def _parallel_face_groups(records):
    groups = []
    for record in records:
        for group in groups:
            if group["normal"].dot(record["normal"]) >= PLANAR_NORMAL_TOLERANCE:
                group["records"].append(record)
                break
        else:
            groups.append({"normal": record["normal"], "records": [record]})
    return groups


def _opposite_surface_coordinate(records, normal):
    coordinates = []
    for record in records:
        if record["normal"].dot(normal) <= -PLANAR_NORMAL_TOLERANCE:
            coordinates.append(record["face"].CenterOfMass.dot(normal))
    return min(coordinates) if coordinates else None


def machining_views(shape):
    """Return machining sides with their pocket floors and depths.

    Each returned side contains a planar outer face, its outward normal and
    interior parallel faces that represent pocket floors from that direction.
    """
    records = _planar_face_records(shape)
    if not records:
        return []

    views = []
    for group in _parallel_face_groups(records):
        normal = group["normal"]
        outer_coordinate = max(record["coordinate"] for record in group["records"])
        outer_records = [record for record in group["records"]
                         if abs(record["coordinate"] - outer_coordinate)
                         <= POCKET_DEPTH_TOLERANCE]
        outer_record = max(outer_records, key=lambda record: record["face"].Area)
        if len(outer_record["face"].Wires) < 2:
            continue
        opposite_coordinate = _opposite_surface_coordinate(records, normal)
        thickness = None if opposite_coordinate is None else (
            outer_coordinate - opposite_coordinate)

        pockets = []
        for record in group["records"]:
            depth = outer_coordinate - record["coordinate"]
            if depth <= POCKET_DEPTH_TOLERANCE:
                continue
            if thickness is not None and depth >= thickness - POCKET_DEPTH_TOLERANCE:
                continue
            pockets.append({"face": record["face"], "depth": depth})

        if pockets:
            views.append({
                "face": outer_record["face"],
                "normal": normal,
                "pockets": pockets,
                "thickness": thickness or 0.0,
            })

    if views:
        return views

    outer_record = max(records, key=lambda record: record["face"].Area)
    opposite_coordinate = _opposite_surface_coordinate(records,
                                                       outer_record["normal"])
    thickness = 0.0 if opposite_coordinate is None else (
        outer_record["coordinate"] - opposite_coordinate)
    return [{"face": outer_record["face"], "normal": outer_record["normal"],
             "pockets": [], "thickness": thickness}]


def pocket_layer_name(depth):
    return ("TASCHE_%0.2fMM" % round(depth, 2)).replace(".", "_")


def safe_file_name(name):
    clean_name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return clean_name or "part"


def _wire_bounds_match(first_wire, second_wire, tolerance=POCKET_DEPTH_TOLERANCE):
    first_box = first_wire.BoundBox
    second_box = second_wire.BoundBox
    return (abs(first_box.XMin - second_box.XMin) <= tolerance and
            abs(first_box.XMax - second_box.XMax) <= tolerance and
            abs(first_box.YMin - second_box.YMin) <= tolerance and
            abs(first_box.YMax - second_box.YMax) <= tolerance and
            abs(first_box.ZMin - second_box.ZMin) <= tolerance and
            abs(first_box.ZMax - second_box.ZMax) <= tolerance)


def _shape_for_view(shape, normal, translation):
    transformed = shape.copy()
    rotation = FreeCAD.Rotation(normal, FreeCAD.Vector(0, 0, 1))
    transformed.Placement = FreeCAD.Placement(
        FreeCAD.Vector(0, 0, 0), rotation).multiply(transformed.Placement)
    transformed.translate(translation)
    return transformed


def _view_label(normal):
    axes = [(abs(normal.x), normal.x, "RECHTS", "LINKS"),
            (abs(normal.y), normal.y, "HINTEN", "VORNE"),
            (abs(normal.z), normal.z, "OBEN", "UNTEN")]
    unused_size, value, positive_label, negative_label = max(axes)
    return positive_label if value >= 0 else negative_label


def _view_layer_shapes(view):
    outer_face = view["face"]
    layer_shapes = {"KONTUR": [outer_face.OuterWire], "DURCHBRUCH": []}
    pocket_wires = []
    for pocket in view["pockets"]:
        layer_name = pocket_layer_name(pocket["depth"])
        wires = list(pocket["face"].Wires)
        layer_shapes.setdefault(layer_name, []).extend(wires)
        pocket_wires.extend(wires)

    for wire in list(outer_face.Wires)[1:]:
        if not any(_wire_bounds_match(wire, pocket_wire)
                   for pocket_wire in pocket_wires):
            layer_shapes["DURCHBRUCH"].append(wire)

    return {name: shapes for name, shapes in layer_shapes.items() if shapes}


def _font_file():
    preferences = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
    candidates = [
        preferences.GetString("textfont", ""),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate
    return None


def _label_shape(document, text, position, height):
    font_file = _font_file()
    if font_file is None:
        return None
    text_object = Draft.make_shapestring(text, font_file, height)
    document.recompute()
    text_shape = text_object.Shape.copy()
    text_shape.translate(position)
    document.removeObject(text_object.Name)
    return text_shape


def _wrapped_text_lines(text, width, height):
    """Wrap ShapeString text so it stays inside one machining view."""
    character_width = max(height * 0.7, 0.1)
    line_length = max(8, int(width / character_width))
    lines = []
    remaining = text
    while len(remaining) > line_length:
        split_at = remaining.rfind(" ", 0, line_length + 1)
        if split_at <= 0:
            split_at = line_length
        lines.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    if remaining:
        lines.append(remaining)
    return lines


def _view_text(part, view, quantity=1):
    text = [getattr(part, "Label", part.Name), _view_label(view["normal"]),
            "MATERIAL %.2f mm" % view["thickness"]]
    depths = sorted({round(pocket["depth"], 2) for pocket in view["pockets"]})
    text.extend("TASCHE %.2f mm" % depth for depth in depths)
    if quantity > 1:
        text.append("MENGE %d" % quantity)
    return " | ".join(text)


def manufacturing_layer_shapes(part, quantity=1):
    """Build 2D manufacturing geometry grouped by Estlcam DXF layer name."""
    views = machining_views(part.Shape)
    layer_shapes = {}
    x_position = 0.0
    margin = 20.0

    for view in views:
        view_shapes = _view_layer_shapes(view)
        outer_shape = _shape_for_view(view["face"].OuterWire, view["normal"],
                                      FreeCAD.Vector(0, 0, 0))
        box = outer_shape.BoundBox
        translation = FreeCAD.Vector(x_position - box.XMin, margin - box.YMin, 0)
        for layer_name, shapes in view_shapes.items():
            transformed_shapes = [_shape_for_view(shape, view["normal"], translation)
                                  for shape in shapes]
            layer_shapes.setdefault(layer_name, []).extend(transformed_shapes)

        text_height = max(2.0, min(6.0, box.XLength / 20.0))
        text_y = box.YLength + 2 * margin
        for text_line in _wrapped_text_lines(_view_text(part, view, quantity),
                                             box.XLength, text_height):
            text_shape = _label_shape(
                FreeCAD.ActiveDocument, text_line,
                FreeCAD.Vector(x_position, text_y, 0), text_height)
            if text_shape is not None:
                layer_shapes.setdefault("TEXT", []).append(text_shape)
            text_y += text_height * 1.5
        x_position += box.XLength + margin

    return layer_shapes


def export_part_dxf(part, output_path, quantity=1):
    """Export one part's labelled machining views to an Estlcam-ready DXF."""
    previous_document = FreeCAD.ActiveDocument
    export_document = FreeCAD.newDocument("LCInterlocking_dxf_export")
    try:
        layer_shapes = manufacturing_layer_shapes(part, quantity)
        export_objects = []
        for layer_name, shapes in layer_shapes.items():
            layer_object = export_document.addObject("Part::Feature", layer_name)
            layer_object.Label = layer_name
            layer_object.Shape = Part.makeCompound(shapes)
            export_objects.append(layer_object)
        export_document.recompute()
        importDXF.export(export_objects, output_path)
        return output_path
    finally:
        FreeCAD.closeDocument(export_document.Name)
        if previous_document is not None:
            FreeCAD.setActiveDocument(previous_document.Name)


def _is_visible_export_object(obj):
    view_object = getattr(obj, "ViewObject", None)
    shape = getattr(obj, "Shape", None)
    if view_object is None or not getattr(view_object, "Visibility", False):
        return False
    if shape is None or shape.isNull():
        return False
    if not shape.Solids:
        return False
    if getattr(obj, "TypeId", "").startswith("App::DocumentObjectGroup"):
        return False
    if getattr(obj, "TypeId", "") in ("App::Part", "Assembly::AssemblyObject",
                                         "Assembly::AssemblyLink"):
        return False
    return True


def visible_export_objects(document):
    return [obj for obj in document.Objects if _is_visible_export_object(obj)]


def _normalized_shape(shape):
    """Return a copy whose instance placement and translation are normalized."""
    normalized_shape = shape.copy()
    normalized_shape.Placement = FreeCAD.Placement()
    box = normalized_shape.BoundBox
    normalized_shape.translate(FreeCAD.Vector(-box.XMin, -box.YMin, -box.ZMin))
    return normalized_shape


def _shape_signature(shape):
    """Return compact geometry metadata for a duplicate-comparison prefilter."""
    box = shape.BoundBox
    return (len(shape.Solids), len(shape.Faces), len(shape.Edges),
            round(shape.Volume, 6), round(shape.Area, 6), round(box.XLength, 6),
            round(box.YLength, 6), round(box.ZLength, 6))


def _shapes_match(first_shape, second_shape):
    """Check candidate duplicates without creating a tessellation in memory."""
    if abs(first_shape.Volume - second_shape.Volume) > GEOMETRY_COMPARISON_TOLERANCE:
        return False
    try:
        overlap = first_shape.common(second_shape)
    except Exception:
        return False
    return abs(overlap.Volume - first_shape.Volume) <= GEOMETRY_COMPARISON_TOLERANCE


def grouped_visible_export_objects(document):
    """Group visible solids with matching finished machining geometry."""
    groups_by_signature = {}
    groups = []
    for part in visible_export_objects(document):
        try:
            normalized_shape = _normalized_shape(part.Shape)
        except Exception:
            groups.append([part])
            continue
        signature = _shape_signature(normalized_shape)
        candidate_groups = groups_by_signature.setdefault(signature, [])
        for reference_shape, group in candidate_groups:
            if _shapes_match(reference_shape, normalized_shape):
                group.append(part)
                break
        else:
            group = [part]
            candidate_groups.append((normalized_shape, group))
            groups.append(group)
    return groups


def _dxf_output_path(output_directory, part, used_names):
    base_name = safe_file_name(getattr(part, "Label", part.Name))
    candidate_name = "%s.dxf" % base_name
    index = 2
    while candidate_name.lower() in used_names or os.path.exists(
            os.path.join(output_directory, candidate_name)):
        candidate_name = "%s_%d.dxf" % (base_name, index)
        index += 1
    used_names.add(candidate_name.lower())
    return os.path.join(output_directory, candidate_name)


def export_visible_parts(document, output_directory):
    """Write one labelled DXF for each group of visible identical parts."""
    written_paths = []
    errors = []
    used_names = set()
    for group in grouped_visible_export_objects(document):
        part = group[0]
        output_path = _dxf_output_path(output_directory, part, used_names)
        try:
            export_part_dxf(part, output_path, len(group))
            written_paths.append(output_path)
        except Exception as error:
            errors.append("%s: %s" % (part.Label, error))
    return written_paths, errors


def get_freecad_object():
    obj_list = selection.get_freecad_objects_list()
    if not obj_list:
        raise ValueError("No selection")
    return obj_list


def transform_shape(part_feature, new_part_feature, freecad_document):
    new_part_feature.Shape = part_feature.Shape.removeSplitter()
    freecad_document.recompute()
    normal_face_prop = biggest_area_faces(part_feature.Shape)
    normal_ref = normal_face_prop[0]
    rotation_to_apply = FreeCAD.Rotation(normal_ref, FreeCAD.Vector(0, 0, 1))
    current_rotation = new_part_feature.Placement.Rotation
    new_rotation = rotation_to_apply.multiply(current_rotation)
    new_part_feature.Placement.Rotation = new_rotation
    freecad_document.recompute()

    return True


class ExportCommand:

    def __init__(self):
        return

    def GetResources(self):
        return {'Pixmap': os.path.join(iconPath, 'export.xpm'),  # the name of a svg file available in the resources
                'MenuText': "Export",
                'ToolTip': "Export"}

    def IsActive(self):
        return len(FreeCADGui.Selection.getSelection()) > 0

    def Activated(self):
        parts_list = get_freecad_object()
        new_doc = FreeCAD.newDocument("export_shape")
        self.export_list(parts_list, new_doc)
        FreeCADGui.getDocument(new_doc.Name).ActiveView.fitAll()
        return

    def export_list(self, parts_list, freecad_document):
        x_pos = 0.
        y_pos = 0.
        margin = 10.
        max_line_y = 0
        z_fix = 30
        new_parts_list = []
        per_line = int(math.sqrt(len(parts_list)))
        for i in range(len(parts_list)):
            part = parts_list[i]
            new_part = freecad_document.addObject("Part::Feature", "test")

            transform_shape(part, new_part, freecad_document)
            bound_box = new_part.Shape.BoundBox
            shift_vector = FreeCAD.Vector(-bound_box.XMin + x_pos, -bound_box.YMin + y_pos, z_fix - bound_box.ZMin)
            x_pos += bound_box.XLength + margin
            new_part.Placement.Base = new_part.Placement.Base.add(shift_vector)
            bound_box = new_part.Shape.BoundBox
            freecad_document.recompute()

            if (bound_box.YLength + y_pos) > max_line_y:
                max_line_y = bound_box.YLength + y_pos

            if (i+1) % per_line == 0:
                y_pos = max_line_y + margin
                x_pos = 0

            new_parts_list.append(new_part)

        for tmppart in new_parts_list:
            Draft.makeShape2DView(tmppart)

        freecad_document.recompute()

        return new_parts_list


class VisibleDxfExportCommand:

    def GetResources(self):
        return {'Pixmap': os.path.join(iconPath, 'export.xpm'),
                'MenuText': "Export visible DXF",
                'ToolTip': "Export visible model-tree parts as layered DXF files"}

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def Activated(self):
        output_directory = QtGui.QFileDialog.getExistingDirectory(
            None, "Export visible DXF files")
        if not output_directory:
            return

        written_paths, errors = export_visible_parts(
            FreeCAD.ActiveDocument, str(output_directory))
        if not written_paths:
            QtGui.QMessageBox.warning(
                None, "Export visible DXF",
                "No visible exportable parts were found in the model tree.")
            return

        message = "%d DXF file(s) exported to:\n%s" % (
            len(written_paths), output_directory)
        if errors:
            message += "\n\nSkipped parts:\n%s" % "\n".join(errors)
            QtGui.QMessageBox.warning(None, "Export visible DXF", message)
        else:
            QtGui.QMessageBox.information(None, "Export visible DXF", message)


if hasattr(FreeCADGui, 'addCommand'):
    FreeCADGui.addCommand('export_command', ExportCommand())
    FreeCADGui.addCommand('export_visible_dxf_command', VisibleDxfExportCommand())
