import os
import sys
import tempfile
import shutil

import FreeCAD
import Part

workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if workspace not in sys.path:
    sys.path.insert(0, workspace)

from ExportPanel import (VisibleDxfExportCommand, export_part_dxf,
                         export_visible_parts, machining_views, pocket_layer_name,
                         visible_export_objects, grouped_visible_export_objects,
                         _view_text, _wrapped_text_lines)


class VisibilityStub:
    def __init__(self, visible):
        self.Visibility = visible


class ExportObjectStub:
    TypeId = "Part::Feature"

    def __init__(self, name, label, shape, visible):
        self.Name = name
        self.Label = label
        self.Shape = shape
        self.ViewObject = VisibilityStub(visible)


class ExportDocumentStub:
    def __init__(self, objects):
        self.Objects = objects


document = FreeCAD.newDocument("VisibleDxfPocketViews")
try:
    plate = Part.makeBox(100, 50, 10)
    top_pocket = Part.makeBox(20, 20, 3, FreeCAD.Vector(10, 10, 7))
    bottom_pocket = Part.makeBox(15, 15, 2, FreeCAD.Vector(60, 10, 0))
    pocketed_plate = plate.cut(top_pocket).cut(bottom_pocket)

    views = machining_views(pocketed_plate)
    depths = sorted(round(pocket["depth"], 2)
                    for view in views for pocket in view["pockets"])
    if depths != [2.0, 3.0]:
        raise AssertionError("Two-sided pockets must retain their individual depths")
    if {pocket_layer_name(depth) for depth in depths} != {
            "TASCHE_2_00MM", "TASCHE_3_00MM"}:
        raise AssertionError("Pocket depths must map to stable Estlcam layer names")

    through_hole_plate = plate.cut(Part.makeCylinder(3, 10, FreeCAD.Vector(50, 25, 0)))
    through_hole_views = machining_views(through_hole_plate)
    if any(view["pockets"] for view in through_hole_views):
        raise AssertionError("Through holes must not be classified as pockets")
    if round(through_hole_views[0]["thickness"], 2) != 10.0:
        raise AssertionError("Contour views must retain the material thickness")
    if not VisibleDxfExportCommand().IsActive():
        raise AssertionError("Visible DXF export must be available in an open document")

    export_part = document.addObject("Part::Feature", "PocketedPlate")
    export_part.Label = "Pocketed plate"
    export_part.Shape = pocketed_plate
    output_path = os.path.join(tempfile.gettempdir(), "lci-pocketed-plate.dxf")
    if os.path.exists(output_path):
        os.remove(output_path)
    export_part_dxf(export_part, output_path)
    with open(output_path, "r") as output_file:
        output = output_file.read()
    for layer_name in ["KONTUR", "TASCHE_2_00MM", "TASCHE_3_00MM", "TEXT"]:
        if layer_name not in output:
            raise AssertionError("DXF must contain the %s Estlcam layer" % layer_name)

    first_visible = ExportObjectStub("FirstVisible", "same label", plate, True)
    second_shape = plate.copy()
    second_shape.Placement.Base = FreeCAD.Vector(120, 10, 0)
    second_visible = ExportObjectStub("SecondVisible", "same label", second_shape, True)
    rotated_shape = plate.copy()
    rotated_shape.Placement = FreeCAD.Placement(
        FreeCAD.Vector(250, 0, 0), FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 90))
    rotated_visible = ExportObjectStub("RotatedVisible", "same label", rotated_shape, True)
    different_visible = ExportObjectStub("DifferentVisible", "different label",
                                         Part.makeBox(101, 50, 10), True)
    hidden = ExportObjectStub("Hidden", "hidden label", plate, False)
    axis = ExportObjectStub("XAxis", "X axis",
                            Part.makePolygon([FreeCAD.Vector(0, 0, 0),
                                              FreeCAD.Vector(10, 0, 0)]), True)
    visible_document = ExportDocumentStub([first_visible, second_visible, rotated_visible,
                                           different_visible, hidden, axis])
    if visible_export_objects(visible_document) != [first_visible, second_visible,
                                                     rotated_visible, different_visible]:
        raise AssertionError("Only visible solid parts may be exported")
    if grouped_visible_export_objects(visible_document) != [
            [first_visible, second_visible, rotated_visible], [different_visible]]:
        raise AssertionError("Identical visible parts must be grouped by geometry")
    if "MENGE 3" not in _view_text(first_visible, views[0], 3):
        raise AssertionError("Grouped exports must label their quantity")
    label_lines = _wrapped_text_lines(
        "Balken_70x42X730 hole template | VORNE | MATERIAL 42.00 mm | "
        "TASCHE 17.00 mm | TASCHE 20.00 mm", 70, 3.5)
    if len(label_lines) < 2 or any(len(line) > 28 for line in label_lines):
        raise AssertionError("Long view labels must wrap within the part width")
    output_directory = tempfile.mkdtemp(prefix="lci-visible-dxf-")
    try:
        written_paths, errors = export_visible_parts(visible_document, output_directory)
        if errors or [os.path.basename(path) for path in written_paths] != [
                "same_label.dxf", "different_label.dxf"]:
            raise AssertionError("Grouped exports need one DXF per geometry and no errors")
    finally:
        shutil.rmtree(output_directory)
finally:
    FreeCAD.closeDocument(document.Name)