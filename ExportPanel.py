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
from lasercut.helper import biggest_area_faces
from panel import selection

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(__dir__, 'icons')


PLANAR_NORMAL_TOLERANCE = 0.999
POCKET_DEPTH_TOLERANCE = 0.01


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
            })

    if views:
        return views

    outer_record = max(records, key=lambda record: record["face"].Area)
    return [{"face": outer_record["face"], "normal": outer_record["normal"],
             "pockets": []}]


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


def _view_text(part, view, thickness):
    text = [getattr(part, "Label", part.Name), _view_label(view["normal"]),
            "MATERIAL %.2f mm" % thickness]
    depths = sorted({round(pocket["depth"], 2) for pocket in view["pockets"]})
    text.extend("TASCHE %.2f mm" % depth for depth in depths)
    return " | ".join(text)


def manufacturing_layer_shapes(part):
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

        thickness = 0.0
        for pocket in view["pockets"]:
            thickness = max(thickness, pocket["depth"])
        text_position = FreeCAD.Vector(x_position, box.YLength + 2 * margin, 0)
        text_height = max(3.0, min(12.0, box.XLength / 20.0))
        text_shape = _label_shape(
            FreeCAD.ActiveDocument, _view_text(part, view, thickness),
            text_position, text_height)
        if text_shape is not None:
            layer_shapes.setdefault("TEXT", []).append(text_shape)
        x_position += box.XLength + margin

    return layer_shapes


def export_part_dxf(part, output_path):
    """Export one part's labelled machining views to an Estlcam-ready DXF."""
    previous_document = FreeCAD.ActiveDocument
    export_document = FreeCAD.newDocument("LCInterlocking_dxf_export")
    try:
        layer_shapes = manufacturing_layer_shapes(part)
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


if hasattr(FreeCADGui, 'addCommand'):
    FreeCADGui.addCommand('export_command', ExportCommand())
