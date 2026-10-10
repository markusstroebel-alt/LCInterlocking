import os
import sys

import FreeCAD
import Part

workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if workspace not in sys.path:
    sys.path.insert(0, workspace)

from lasercut.holetemplate import cut_targets
from panel.selection import (_get_link_component_for_object, get_object_from_reference,
                             get_selection_arguments, resolve_selection_component)
from panel.holetemplates import (HoleTemplateGroup, HoleTemplateViewProvider,
                                 _new_objects, _set_reference_visibility)
from ExportPanel import transform_shape


class ShapeObject:
    def __init__(self, name, shape):
        self.Name = name
        self.Label = name
        self.Shape = shape


class ViewObjectStub:
    def __init__(self, obj):
        self.Object = obj
        self.Proxy = None


class VisibilityViewObjectStub:
    def __init__(self):
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False


class VisibilityObjectStub:
    def __init__(self, element_visibility_result, resolved_child=None):
        self.Document = None
        self.Name = "AssemblyLink"
        self.Label = "Assembly link"
        self.LinkedObject = object()
        self.ViewObject = VisibilityViewObjectStub()
        self.element_visibility_result = element_visibility_result
        self.element_visibility_calls = []
        self.resolved_child = resolved_child

    def getSubObject(self, sub_path):
        return Part.makeBox(1, 1, 1)

    def resolveSubElement(self, sub_path, append, resolve_type):
        if self.resolved_child is None:
            raise ValueError("No nested child")
        return self.resolved_child, "", ""

    def setElementVisible(self, sub_path, visible):
        self.element_visibility_calls.append((sub_path, visible))
        return self.element_visibility_result


class VisibilityDocumentStub:
    def __init__(self, obj):
        self.obj = obj

    def getObject(self, name):
        return self.obj if name == "AssemblyLink" else None


class VisibilityFeatureStub:
    def __init__(self, document, target_names, names_mapping, edit=False):
        self.Document = document
        self.TargetBodyNames = target_names
        self.namesMapping = names_mapping
        self.generatedParts = []
        self.edit = edit


class SelectionStub:
    def __init__(self, obj):
        self.Object = obj


class NestedSelectionChildStub:
    def __init__(self, document, name):
        self.Document = document
        self.Name = name
        self.InList = []


class NestedSelectionParentStub:
    def __init__(self, document, child, shape):
        self.Document = document
        self.Name = "NestedAssembly"
        self.Label = "Nested assembly"
        self.LinkedObject = object()
        self.Group = [child]
        self.shape = shape

    def getSubObject(self, sub_path):
        if sub_path == "NestedBase.":
            return self.shape
        return None


class ObjectLookupStub:
    def __init__(self, objects):
        self.objects = objects

    def getObject(self, name):
        return self.objects.get(name)


def assert_less(first, second, message):
    if not first < second:
        raise AssertionError(message)


document = FreeCAD.newDocument("HoleTemplateGeometryTest")
try:
    lower_plate = ShapeObject("LowerPlate", Part.makeBox(10, 10, 2))
    upper_plate = ShapeObject("UpperPlate", Part.makeBox(
        10, 10, 2, FreeCAD.Vector(0, 0, 5)))
    screw = ShapeObject("Screw", Part.makeCylinder(
        1, 10, FreeCAD.Vector(5, 5, -1)))
    remote_template = ShapeObject("Remote", Part.makeBox(
        1, 1, 1, FreeCAD.Vector(20, 20, 20)))

    generated = cut_targets([screw], [lower_plate, upper_plate])
    if len(generated) != 2:
        raise AssertionError("The screw must cut both intersecting plates")

    generated_by_source = {source.Name: shape for source, shape in generated}
    assert_less(generated_by_source["LowerPlate"].Volume, lower_plate.Shape.Volume,
                "The lower plate must lose screw volume")
    assert_less(generated_by_source["UpperPlate"].Volume, upper_plate.Shape.Volume,
                "The upper plate must lose screw volume")

    if cut_targets([remote_template], [lower_plate]):
        raise AssertionError("A non-intersecting template must not create a result")

    source = document.addObject("Part::Feature", "Source")
    new_source = document.addObject("Part::Feature", "NewSource")
    first_link = document.addObject("App::Link", "FirstLink")
    second_link = document.addObject("App::Link", "SecondLink")
    first_link.LinkedObject = source
    second_link.LinkedObject = source

    if _get_link_component_for_object(document, first_link) != first_link:
        raise AssertionError("An explicitly selected Assembly link must be preserved")
    if _get_link_component_for_object(document, source) != source:
        raise AssertionError("Ambiguous source links must not select an arbitrary instance")
    if _new_objects([source, new_source], {source.Name}) != [new_source]:
        raise AssertionError("Only newly selected bodies must be added to a template operation")

    nested_child = NestedSelectionChildStub(document, "NestedBase")
    nested_child_shape = Part.makeBox(10, 10, 2, FreeCAD.Vector(50, 0, 0))
    nested_parent = NestedSelectionParentStub(document, nested_child,
                                              nested_child_shape)
    nested_child.InList = [nested_parent]
    resolved_nested_child = resolve_selection_component(
        SelectionStub(nested_child), "Face1")
    if resolved_nested_child.Name != "NestedAssembly__LCI_PATH__NestedBase.":
        raise AssertionError("Direct child selection must retain the parent Assembly path")
    if resolved_nested_child.Shape.BoundBox.XMin != 50.0:
        raise AssertionError("Nested child selection must use its effective Assembly shape")
    nested_lookup_document = ObjectLookupStub({"NestedBase": nested_child})
    restored_nested_child = get_object_from_reference(
        nested_lookup_document, "NestedBase")
    if restored_nested_child.Name != resolved_nested_child.Name:
        raise AssertionError("Legacy child references must resolve through the parent Assembly")

    generated_result = document.addObject(
        "Part::Feature", "NestedAssembly__LCI_PATH__NestedBase__hole_template")
    if get_object_from_reference(document, generated_result.Name) != generated_result:
        raise AssertionError("Generated result names must not be parsed as nested references")

    nested_visibility_object = VisibilityObjectStub(-1)
    nested_visibility_document = VisibilityDocumentStub(nested_visibility_object)
    _set_reference_visibility(nested_visibility_document,
                              "AssemblyLink__LCI_PATH__Base.", False)
    if not nested_visibility_object.ViewObject.visible:
        raise AssertionError("Unsupported nested visibility must keep the parent visible")
    if nested_visibility_object.element_visibility_calls != [("Base.", False)]:
        raise AssertionError("Nested visibility must use the selected Assembly path")

    nested_child_visibility_object = VisibilityObjectStub(-1)
    nested_visibility_parent = VisibilityObjectStub(
        -1, nested_child_visibility_object)
    nested_visibility_document = VisibilityDocumentStub(nested_visibility_parent)
    _set_reference_visibility(nested_visibility_document,
                              "AssemblyLink__LCI_PATH__Base.", False)
    if nested_child_visibility_object.ViewObject.visible:
        raise AssertionError("Nested child must be hidden when element visibility is unsupported")
    if not nested_visibility_parent.ViewObject.visible:
        raise AssertionError("Hiding a nested child must not hide the parent Assembly")

    direct_visibility_object = VisibilityObjectStub(-1)
    direct_visibility_document = VisibilityDocumentStub(direct_visibility_object)
    _set_reference_visibility(direct_visibility_document, "AssemblyLink", False)
    if direct_visibility_object.ViewObject.visible:
        raise AssertionError("Direct targets must still be hidden after generation")

    no_result_visibility_object = VisibilityObjectStub(-1)
    no_result_visibility_document = VisibilityDocumentStub(no_result_visibility_object)
    no_result_feature = VisibilityFeatureStub(
        no_result_visibility_document, ["AssemblyLink"], {})
    HoleTemplateGroup.__new__(HoleTemplateGroup).edit_mode(no_result_feature)
    if not no_result_visibility_object.ViewObject.visible:
        raise AssertionError("Targets without an intersection must remain visible")

    result_visibility_object = VisibilityObjectStub(-1)
    result_visibility_document = VisibilityDocumentStub(result_visibility_object)
    result_feature = VisibilityFeatureStub(
        result_visibility_document, ["AssemblyLink"], {"AssemblyLink": "Result"})
    HoleTemplateGroup.__new__(HoleTemplateGroup).edit_mode(result_feature)
    if result_visibility_object.ViewObject.visible:
        raise AssertionError("Targets with a generated result must be hidden")

    result = document.addObject("Part::Feature", "Result")
    result.addProperty("App::PropertyString", "SourceTargetName", "Hole template")
    result.addProperty("App::PropertyStringList", "TemplateBodyNames", "Hole template")
    result.SourceTargetName = source.Name
    result.TemplateBodyNames = [first_link.Name, second_link.Name]
    if result.getTypeIdOfProperty("SourceTargetName") != "App::PropertyString":
        raise AssertionError("Result provenance must not use a scoped PropertyLink")

    legacy_feature = document.addObject("Part::FeaturePython", "LegacyHoleTemplate")
    legacy_feature.addProperty("App::PropertyStringList", "TemplateBodyNames", "Hole template")
    legacy_feature.addProperty("App::PropertyStringList", "TargetBodyNames", "Hole template")
    legacy_feature.addProperty("App::PropertyBool", "need_recompute", "Hole template")
    legacy_feature.addProperty("App::PropertyBool", "edit", "Hole template")
    legacy_feature.TemplateBodyNames = []
    legacy_feature.TargetBodyNames = []
    legacy_feature.need_recompute = False
    legacy_proxy = HoleTemplateGroup.__new__(HoleTemplateGroup)
    legacy_proxy.onChanged(legacy_feature, "edit")
    if legacy_feature.getTypeIdOfProperty("generatedParts") != "App::PropertyLinkList":
        raise AssertionError("Editing a legacy template must add managed result properties")

    managed_template = document.addObject("Part::Feature", "ManagedTemplate")
    managed_template.Shape = Part.makeCylinder(1, 10, FreeCAD.Vector(5, 5, -1))
    managed_target = document.addObject("Part::Feature", "ManagedTarget")
    managed_target.Shape = Part.makeBox(10, 10, 2)
    managed_feature = document.addObject("Part::FeaturePython", "ManagedHoleTemplate")
    HoleTemplateGroup(managed_feature)
    managed_view_object = ViewObjectStub(managed_feature)
    managed_view_provider = HoleTemplateViewProvider(managed_view_object)
    managed_view_provider.attach(managed_view_object)
    managed_feature.TemplateBodyNames = [managed_template.Name]
    managed_feature.TargetBodyNames = [managed_target.Name]
    managed_feature.need_recompute = True
    document.recompute()

    if len(managed_feature.generatedParts) != 1:
        raise AssertionError("Managed templates must create one child result")
    managed_result = managed_feature.generatedParts[0]
    if managed_view_provider.claimChildren() != [managed_result]:
        raise AssertionError("Managed result must appear below the HoleTemplate tree node")
    if managed_result.SourceTargetName != managed_target.Name:
        raise AssertionError("Managed result must retain its target name")

    managed_result_name = managed_result.Name
    managed_feature.need_recompute = True
    document.recompute()
    if managed_feature.generatedParts[0].Name != managed_result.Name:
        raise AssertionError("Managed recompute must reuse the existing result")

    remote_target = document.addObject("Part::Feature", "RemoteManagedTarget")
    remote_target.Shape = Part.makeBox(1, 1, 1, FreeCAD.Vector(20, 20, 20))
    managed_feature.TargetBodyNames = [remote_target.Name]
    managed_feature.need_recompute = True
    document.recompute()
    if managed_feature.generatedParts:
        raise AssertionError("Non-intersecting targets must remove obsolete managed results")
    if document.getObject(managed_result_name) is not None:
        raise AssertionError("Obsolete managed result must be removed from the document")

    nested_template_source = document.addObject("Part::Feature", "NestedTemplateSource")
    nested_template_source.Shape = Part.makeCylinder(1, 10, FreeCAD.Vector(5, 5, -1))
    nested_target_source = document.addObject("Part::Feature", "NestedTargetSource")
    nested_target_source.Shape = Part.makeBox(10, 10, 2)
    nested_template = document.addObject("App::Link", "NestedTemplate")
    nested_template.LinkedObject = nested_template_source
    nested_target = document.addObject("App::Link", "NestedTarget")
    nested_target.LinkedObject = nested_target_source
    nested_assembly = document.addObject("App::Part", "NestedAssembly")
    nested_assembly.addObject(nested_template)
    nested_assembly.addObject(nested_target)
    outer_assembly = document.addObject("App::Link", "OuterAssembly")
    outer_assembly.LinkedObject = nested_assembly
    outer_assembly.Placement.Base = FreeCAD.Vector(0, 0, 20)
    document.recompute()

    nested_selection = SelectionStub(outer_assembly)
    resolved_template = resolve_selection_component(
        nested_selection, "OuterAssembly.NestedTemplate.Face1")
    resolved_target = resolve_selection_component(
        nested_selection, "OuterAssembly.NestedTarget.Face1")
    if resolved_template.Name != "OuterAssembly__LCI_PATH__NestedTemplate.":
        raise AssertionError("Nested selection must persist the full component path")
    if resolved_template.Shape.BoundBox.ZMin != 19.0:
        raise AssertionError("Nested template shape must include the outer placement")
    restored_template = get_object_from_reference(document, resolved_template.Name)
    if restored_template.Shape.BoundBox.ZMin != resolved_template.Shape.BoundBox.ZMin:
        raise AssertionError("Nested references must resolve identically after recompute")
    selection_root, selection_path = get_selection_arguments(
        document, resolved_target.Name, "Face1")
    if selection_root != outer_assembly or selection_path != "NestedTarget.Face1":
        raise AssertionError("Tree selection must restore the nested component path")

    nested_generated = cut_targets([resolved_template], [resolved_target])
    if len(nested_generated) != 1:
        raise AssertionError("Nested template and target must intersect at their assembly placement")
    assert_less(nested_generated[0][1].Volume, resolved_target.Shape.Volume,
                "Nested target must lose template volume")

    nested_feature = document.addObject("Part::FeaturePython", "NestedHoleTemplate")
    HoleTemplateGroup(nested_feature)
    nested_feature.TemplateBodyNames = [resolved_template.Name]
    nested_feature.TargetBodyNames = [resolved_target.Name]
    nested_feature.need_recompute = True
    document.recompute()
    if len(nested_feature.generatedParts) != 1:
        raise AssertionError("HoleTemplate must recompute from stored nested references")

    export_document = FreeCAD.newDocument("NestedExportTest")
    export_part = export_document.addObject("Part::Feature", "NestedExportPart")
    transform_shape(resolved_target, export_part, export_document)
    if export_part.Shape.isNull():
        raise AssertionError("Export must accept a placed nested component shape")
    FreeCAD.closeDocument(export_document.Name)
finally:
    FreeCAD.closeDocument(document.Name)