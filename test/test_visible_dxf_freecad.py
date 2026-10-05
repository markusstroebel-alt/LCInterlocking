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
                         visible_export_objects)


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
    second_visible = ExportObjectStub("SecondVisible", "same label", plate, True)
    hidden = ExportObjectStub("Hidden", "hidden label", plate, False)
    visible_document = ExportDocumentStub([first_visible, second_visible, hidden])
    if visible_export_objects(visible_document) != [first_visible, second_visible]:
        raise AssertionError("Only objects visible in the model tree may be exported")
    output_directory = tempfile.mkdtemp(prefix="lci-visible-dxf-")
    try:
        written_paths, errors = export_visible_parts(visible_document, output_directory)
        if errors or [os.path.basename(path) for path in written_paths] != [
                "same_label.dxf", "same_label_2.dxf"]:
            raise AssertionError("Visible exports need unique DXF names and no errors")
    finally:
        shutil.rmtree(output_directory)
finally:
    FreeCAD.closeDocument(document.Name)