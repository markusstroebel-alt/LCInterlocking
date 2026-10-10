#!/usr/bin/env python

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import os

from lasercut.holetemplate import cut_targets
from panel import selection


__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(__dir__, '../icons')


def _object_label(obj):
    label = getattr(obj, 'Label', obj.Name)
    return "%s (%s)" % (label, obj.Name)


def _objects_from_names(document, names):
    objects = []
    for name in names:
        obj = selection.get_object_from_reference(document, name)
        if obj:
            objects.append(obj)
    return objects


def _normalize_reference_names(document, names):
    normalized_names = []
    for name in names:
        obj = selection.get_object_from_reference(document, name)
        normalized_name = obj.Name if obj else name
        if normalized_name not in normalized_names:
            normalized_names.append(normalized_name)
    return normalized_names


def _new_objects(objects, known_names):
    return [obj for obj in objects if obj.Name not in known_names]


def _fit_all(document):
    try:
        FreeCADGui.getDocument(document.Name).activeView().fitAll()
    except Exception:
        pass


def _set_reference_visibility(document, reference_name, visible):
    resolved_object = selection.get_object_from_reference(document, reference_name)
    if selection.is_resolved_component(resolved_object):
        root_object = resolved_object.root_object
        sub_path = resolved_object.sub_path
    else:
        root_name, sub_path = selection.split_reference_name(reference_name)
        root_object = document.getObject(root_name)
    if root_object is None:
        return

    if sub_path:
        try:
            if root_object.setElementVisible(sub_path, visible) == 1:
                return
        except Exception:
            pass
        try:
            child_object, unused_new_name, unused_old_name = root_object.resolveSubElement(
                sub_path, False, 0)
            view_object = child_object.ViewObject
        except Exception:
            return
    else:
        view_object = root_object.ViewObject

    if view_object is None:
        return
    if visible:
        view_object.show()
    else:
        view_object.hide()


class HoleTemplateGroup:
    def __init__(self, obj):
        obj.addProperty("App::PropertyStringList", "TemplateBodyNames", "Hole template")
        obj.addProperty("App::PropertyStringList", "TargetBodyNames", "Hole template")
        obj.addProperty("App::PropertyLinkList", "generatedParts", "Hole template")
        obj.addProperty("App::PropertyPythonObject", "namesMapping", "Hole template")
        obj.addProperty("App::PropertyBool", "need_recompute", "Hole template")
        obj.addProperty("App::PropertyBool", "edit", "Hole template")
        obj.TemplateBodyNames = []
        obj.TargetBodyNames = []
        obj.generatedParts = []
        obj.namesMapping = {}
        obj.need_recompute = False
        obj.edit = False
        obj.Proxy = self

    def ensure_result_properties(self, fp):
        if not hasattr(fp, "generatedParts"):
            fp.addProperty("App::PropertyLinkList", "generatedParts", "Hole template")
            fp.generatedParts = []
        if not hasattr(fp, "namesMapping"):
            fp.addProperty("App::PropertyPythonObject", "namesMapping", "Hole template")
            fp.namesMapping = {}

    def onChanged(self, fp, prop):
        self.ensure_result_properties(fp)
        if prop == "need_recompute" and fp.need_recompute:
            self.execute(fp)
        elif prop == "edit":
            self.edit_mode(fp)

    def execute(self, fp):
        self.ensure_result_properties(fp)
        fp.need_recompute = False
        template_names = _normalize_reference_names(fp.Document, fp.TemplateBodyNames)
        target_names = _normalize_reference_names(fp.Document, fp.TargetBodyNames)
        if template_names != list(fp.TemplateBodyNames):
            fp.TemplateBodyNames = template_names
        if target_names != list(fp.TargetBodyNames):
            fp.TargetBodyNames = target_names
        template_objects = _objects_from_names(fp.Document, template_names)
        target_objects = _objects_from_names(fp.Document, target_names)
        try:
            generated = cut_targets(template_objects, target_objects)
        except ValueError as err:
            FreeCAD.Console.PrintError("[LCInterlocking] Hole template: %s\n" % err)
            return

        previous_mapping = dict(fp.namesMapping or {})
        fp.namesMapping = {}
        generated_parts = []
        result_names = []
        for target_object, shape in generated:
            result_key = target_object.Name
            result = fp.Document.getObject(previous_mapping.get(result_key, ""))
            if result is None:
                result = fp.Document.addObject("Part::Feature",
                                                "%s_hole_template" % target_object.Name)
                result.addProperty("App::PropertyString", "SourceTargetName", "Hole template")
                result.addProperty("App::PropertyStringList", "TemplateBodyNames", "Hole template")
            result.Label = "%s hole template" % target_object.Label
            result.SourceTargetName = target_object.Name
            result.TemplateBodyNames = list(fp.TemplateBodyNames)
            result.Shape = shape
            result.purgeTouched()
            fp.namesMapping[result_key] = result.Name
            result_names.append(result.Name)
            generated_parts.append(result)

        for result in fp.generatedParts:
            if result.Name not in result_names:
                fp.Document.removeObject(result.Name)
        fp.generatedParts = generated_parts
        fp.edit = False
        self.edit_mode(fp)
        _fit_all(fp.Document)

    def edit_mode(self, fp):
        self.ensure_result_properties(fp)
        generated_target_names = set((fp.namesMapping or {}).keys())
        for target_name in fp.TargetBodyNames:
            _set_reference_visibility(
                fp.Document, target_name,
                fp.edit or target_name not in generated_target_names)
        for result in fp.generatedParts:
            view_object = result.ViewObject
            if view_object is None:
                continue
            if fp.edit:
                view_object.hide()
            else:
                view_object.show()


class HoleTemplateViewProvider:
    def __init__(self, vobj):
        vobj.Proxy = self

    def setEdit(self, vobj=None, mode=0):
        if mode == 0:
            objects = _objects_from_names(
                self.Object.Document,
                list(self.Object.TemplateBodyNames) + list(self.Object.TargetBodyNames))
            self.Object.edit = True
            FreeCADGui.Control.showDialog(HoleTemplatePanel(objects, self.Object))
            return True
        return False

    def unsetEdit(self, vobj, mode=0):
        FreeCADGui.Control.closeDialog()
        return

    def setupContextMenu(self, obj, menu):
        action = menu.addAction("Edit")
        action.triggered.connect(self.setEdit)

    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object

    def claimChildren(self):
        return getattr(self.Object, "generatedParts", [])

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class HoleTemplatePanel:
    def __init__(self, objects, hole_template=None):
        self.document = FreeCAD.ActiveDocument
        self.objects_by_name = {obj.Name: obj for obj in objects}
        self.hole_template = hole_template
        self.editing_existing = hole_template is not None
        self.template_names_origin = []
        self.target_names_origin = []
        if hole_template:
            self.template_names_origin = list(hole_template.TemplateBodyNames)
            self.target_names_origin = list(hole_template.TargetBodyNames)
        self.preview_document = None
        self.form = QtGui.QWidget()
        self.form.setObjectName("HoleTemplatePanel")
        self.form.setWindowTitle("Hole templates")

        layout = QtGui.QVBoxLayout(self.form)
        layout.addWidget(QtGui.QLabel("Assign each selected body to a role.", self.form))

        configured_names = set(self.template_names_origin + self.target_names_origin)
        available_objects = [obj for obj in objects if obj.Name not in configured_names]
        self.available_list = self._make_list("Selected bodies", available_objects)
        layout.addWidget(self.available_list)

        add_selected_button = QtGui.QPushButton("Add selected bodies", self.form)
        add_selected_button.clicked.connect(self.add_selected_bodies)
        layout.addWidget(add_selected_button)

        role_buttons = QtGui.QHBoxLayout()
        template_button = QtGui.QPushButton("Set as template", self.form)
        template_button.clicked.connect(self.set_as_template)
        target_button = QtGui.QPushButton("Set as target", self.form)
        target_button.clicked.connect(self.set_as_target)
        restore_button = QtGui.QPushButton("Clear role", self.form)
        restore_button.clicked.connect(self.clear_role)
        role_buttons.addWidget(template_button)
        role_buttons.addWidget(target_button)
        role_buttons.addWidget(restore_button)
        layout.addLayout(role_buttons)

        lists_layout = QtGui.QHBoxLayout()
        template_objects = [self.objects_by_name[name]
                    for name in self.template_names_origin
                    if name in self.objects_by_name]
        target_objects = [self.objects_by_name[name]
                  for name in self.target_names_origin
                  if name in self.objects_by_name]
        self.template_list = self._make_list("Template bodies", template_objects)
        self.target_list = self._make_list("Target bodies", target_objects)
        lists_layout.addWidget(self.template_list)
        lists_layout.addWidget(self.target_list)
        layout.addLayout(lists_layout)

        preview_button = QtGui.QPushButton("Preview", self.form)
        preview_button.clicked.connect(self.preview)
        layout.addWidget(preview_button)

    def _make_list(self, title, objects=None):
        group = QtGui.QGroupBox(title, self.form)
        group_layout = QtGui.QVBoxLayout(group)
        list_widget = QtGui.QListWidget(group)
        list_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        group_layout.addWidget(list_widget)
        group.setMinimumHeight(100)
        if objects:
            for obj in objects:
                self._add_object(group, obj)
        return group

    def _list_widget(self, group):
        return group.findChild(QtGui.QListWidget)

    def _add_object(self, group, obj):
        item = QtGui.QListWidgetItem(_object_label(obj))
        item.setData(QtCore.Qt.UserRole, obj.Name)
        self._list_widget(group).addItem(item)

    def _listed_object_names(self):
        names = set()
        for group in [self.available_list, self.template_list, self.target_list]:
            for index in range(self._list_widget(group).count()):
                item = self._list_widget(group).item(index)
                name = item.data(QtCore.Qt.UserRole)
                if hasattr(name, 'toPyObject'):
                    name = name.toPyObject()
                names.add(str(name))
        return names

    def add_selected_bodies(self):
        selected_objects = selection.get_freecad_objects_list()
        new_objects = _new_objects(selected_objects, self._listed_object_names())
        for obj in new_objects:
            self.objects_by_name[obj.Name] = obj
            self._add_object(self.available_list, obj)

        if not new_objects:
            QtGui.QMessageBox.information(
                None, "Hole templates",
                "Select at least one new body in the 3D view before adding it.")

    def _item_object(self, item):
        name = item.data(QtCore.Qt.UserRole)
        if hasattr(name, 'toPyObject'):
            name = name.toPyObject()
        return self.objects_by_name[str(name)]

    def _selected_objects(self, group):
        objects = []
        for item in self._list_widget(group).selectedItems():
            objects.append(self._item_object(item))
        return objects

    def _move_selected(self, source_group, destination_group):
        source_list = self._list_widget(source_group)
        for item in list(source_list.selectedItems()):
            obj = self._item_object(item)
            self._add_object(destination_group, obj)
            source_list.takeItem(source_list.row(item))

    def set_as_template(self):
        self._move_selected(self.available_list, self.template_list)

    def set_as_target(self):
        self._move_selected(self.available_list, self.target_list)

    def clear_role(self):
        self._move_selected(self.template_list, self.available_list)
        self._move_selected(self.target_list, self.available_list)

    def _roles(self):
        return (self._selected_objects_from_all(self.template_list),
                self._selected_objects_from_all(self.target_list))

    def _selected_objects_from_all(self, group):
        objects = []
        for index in range(self._list_widget(group).count()):
            item = self._list_widget(group).item(index)
            objects.append(self._item_object(item))
        return objects

    def _generated_shapes(self):
        template_objects, target_objects = self._roles()
        return template_objects, target_objects, cut_targets(template_objects, target_objects)

    def preview(self):
        try:
            _, _, generated = self._generated_shapes()
        except ValueError as err:
            QtGui.QMessageBox.warning(None, "Hole templates", str(err))
            return

        if not generated:
            QtGui.QMessageBox.information(None, "Hole templates",
                                          "No template body intersects a target body.")
            return

        if self.preview_document is None:
            self.preview_document = FreeCAD.newDocument("HoleTemplate_preview")
        for obj in list(self.preview_document.Objects):
            self.preview_document.removeObject(obj.Name)
        for target_object, shape in generated:
            result = self.preview_document.addObject("Part::Feature",
                                                     "%s_preview" % target_object.Name)
            result.Label = "%s hole template preview" % target_object.Label
            result.Shape = shape
        self.preview_document.recompute()
        FreeCADGui.getDocument(self.preview_document.Name).activeView().fitAll()

    def accept(self):
        try:
            template_objects, target_objects, generated = self._generated_shapes()
        except ValueError as err:
            QtGui.QMessageBox.warning(None, "Hole templates", str(err))
            return False

        if not generated:
            QtGui.QMessageBox.warning(None, "Hole templates",
                                      "No template body intersects a target body.")
            return False

        if self.hole_template is None:
            self.hole_template = self.document.addObject("Part::FeaturePython", "HoleTemplate")
            self.hole_template.Label = "Hole template"
            HoleTemplateGroup(self.hole_template)
            HoleTemplateViewProvider(self.hole_template.ViewObject)

        self.hole_template.TemplateBodyNames = [obj.Name for obj in template_objects]
        self.hole_template.TargetBodyNames = [obj.Name for obj in target_objects]
        self.hole_template.need_recompute = True
        if self.editing_existing:
            FreeCADGui.ActiveDocument.resetEdit()
        return True

    def reject(self):
        if self.editing_existing:
            self.hole_template.TemplateBodyNames = self.template_names_origin
            self.hole_template.TargetBodyNames = self.target_names_origin
            self.hole_template.edit = False
            FreeCADGui.ActiveDocument.resetEdit()
        return True

    def getStandardButtons(self):
        buttons = QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel
        return buttons.value if hasattr(buttons, 'value') else int(buttons)


class HoleTemplateCommand:
    def GetResources(self):
        return {'Pixmap': os.path.join(iconPath, 'hole_template.xpm'),
            'MenuText': "Hole templates",
            'ToolTip': "Cut selected template bodies from selected target bodies"}

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None and len(selection.get_freecad_objects_list()) >= 2

    def Activated(self):
        objects = selection.get_freecad_objects_list()
        if len(objects) < 2:
            QtGui.QMessageBox.warning(None, "Hole templates",
                                      "Select at least two bodies before starting the tool.")
            return
        FreeCADGui.Control.showDialog(HoleTemplatePanel(objects))


if hasattr(FreeCADGui, 'addCommand'):
    FreeCADGui.addCommand('hole_templates', HoleTemplateCommand())