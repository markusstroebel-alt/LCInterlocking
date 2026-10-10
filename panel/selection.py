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


_REFERENCE_SEPARATOR = "__LCI_PATH__"


def _debug(message):
    FreeCAD.Console.PrintMessage("[LCInterlocking] %s\n" % message)


class ResolvedComponent:
    """A placed subcomponent addressed by a stable root-object/path reference."""

    def __init__(self, root_object, sub_path):
        self.root_object = root_object
        self.sub_path = sub_path
        self.Document = root_object.Document
        self.Name = make_reference_name(root_object.Name, sub_path)
        path_label = sub_path.rstrip('.').replace('.', ' / ')
        self.Label = root_object.Label if not path_label else "%s / %s" % (
            root_object.Label, path_label)
        self.LinkedObject = getattr(root_object, 'LinkedObject', None)
        self.Shape = root_object.getSubObject(sub_path)
        if self.Shape is None:
            raise ValueError("Cannot resolve Assembly path %s on %s" %
                             (sub_path, root_object.Name))


def make_reference_name(root_name, sub_path=""):
    if not sub_path:
        return root_name
    return "%s%s%s" % (root_name, _REFERENCE_SEPARATOR, sub_path)


def split_reference_name(reference_name):
    if _REFERENCE_SEPARATOR not in reference_name:
        return reference_name, ""
    return reference_name.split(_REFERENCE_SEPARATOR, 1)


def get_object_from_reference(document, reference_name):
    document_object = document.getObject(reference_name)
    if document_object is not None:
        if _REFERENCE_SEPARATOR not in reference_name:
            parent_component = _get_parent_link_component(document_object)
            if parent_component is not None:
                return parent_component
        return document_object

    root_name, sub_path = split_reference_name(reference_name)
    root_object = document.getObject(root_name)
    if root_object is None:
        return None
    if not sub_path:
        parent_component = _get_parent_link_component(root_object)
        if parent_component is not None:
            return parent_component
        return root_object
    return ResolvedComponent(root_object, sub_path)


def get_root_object_from_reference(document, reference_name):
    root_name, unused_sub_path = split_reference_name(reference_name)
    return document.getObject(root_name)


def is_resolved_component(obj):
    return isinstance(obj, ResolvedComponent)


def get_selection_arguments(document, reference_name, sub_element_name=""):
    """Return ``(document_object, full_sub_element_name)`` for tree selection."""
    root_name, sub_path = split_reference_name(reference_name)
    root_object = document.getObject(root_name)
    if root_object is None:
        return None, sub_element_name
    return root_object, "%s%s" % (sub_path, sub_element_name)


def _is_geometry_element(name):
    return name.startswith(("Face", "Edge", "Vertex"))


def _selection_path_parts(sub_element_name, keep_geometry_element):
    if not sub_element_name:
        return []
    parts = [part for part in sub_element_name.rstrip('.').split('.') if part]
    if not keep_geometry_element and parts and _is_geometry_element(parts[-1]):
        return parts[:-1]
    return parts


def _resolve_path_component(document, selected_object, sub_element_name,
                            keep_geometry_element=False):
    parts = _selection_path_parts(sub_element_name, keep_geometry_element)
    if not parts:
        return None

    path_root = document.getObject(parts[0])
    if path_root:
        root_object = path_root
        parts = parts[1:]
    else:
        root_object = selected_object

    sub_path = ".".join(parts)
    if not sub_path:
        return root_object
    return ResolvedComponent(root_object, "%s." % sub_path)


def _get_component_from_sub_element(selection_obj, sub_element_name):
    if not sub_element_name or '.' not in sub_element_name:
        return selection_obj.Object

    component_name = sub_element_name.split('.', 1)[0]
    component = selection_obj.Object.Document.getObject(component_name)
    if component:
        _debug("Resolved selection path %s to component %s" %
               (sub_element_name, component.Name))
    return component if component else selection_obj.Object


def _get_local_sub_element_name(sub_element_name):
    if not sub_element_name:
        return sub_element_name
    return sub_element_name.rstrip('.').split('.')[-1]


def _contains_object(parent, child, visited=None):
    if parent == child:
        return True
    if visited is None:
        visited = set()
    object_key = (parent.Document.Name, parent.Name)
    if object_key in visited:
        return False
    visited.add(object_key)

    for nested_object in getattr(parent, 'Group', []):
        if _contains_object(nested_object, child, visited):
            return True
    return False


def _get_link_component_for_object(document, selected_object,
                                   preferred_component_names=None):
    if getattr(selected_object, 'LinkedObject', None) is not None:
        return selected_object

    matching_components = []
    for document_object in document.Objects:
        linked_object = getattr(document_object, 'LinkedObject', None)
        if linked_object and _contains_object(linked_object, selected_object):
            matching_components.append(document_object)

    if preferred_component_names:
        preferred_components = [component for component in matching_components
                                if component.Name in preferred_component_names]
        if len(preferred_components) == 1:
            component = preferred_components[0]
            _debug("Resolved feature %s to configured Assembly link %s" %
                   (selected_object.Name, component.Name))
            return component

    if matching_components:
        if len(matching_components) > 1:
            _debug("Ambiguous Assembly links for feature %s; using the explicit selection path" %
                   selected_object.Name)
            return selected_object
        component = matching_components[0]
        _debug("Resolved feature %s to Assembly link %s" %
               (selected_object.Name, component.Name))
        return component
    return selected_object


def _get_parent_link_component(selected_object):
    for parent_object in getattr(selected_object, 'InList', []):
        if getattr(parent_object, 'LinkedObject', None) is None:
            continue
        if selected_object not in getattr(parent_object, 'Group', []):
            continue
        try:
            return ResolvedComponent(parent_object, "%s." % selected_object.Name)
        except ValueError:
            continue
    return None


def resolve_selection_component(selection_obj, sub_element_name=None,
                                preferred_component_names=None,
                                keep_geometry_element=False):
    """Resolve a selection to a direct component or a placed nested component."""
    document = selection_obj.Object.Document
    component = _resolve_path_component(document, selection_obj.Object,
                                        sub_element_name,
                                        keep_geometry_element)
    if component is not None:
        return component

    component = _get_parent_link_component(selection_obj.Object)
    if component is not None:
        return component

    component = _get_link_component_for_object(
        document, selection_obj.Object, preferred_component_names)
    if component == selection_obj.Object:
        return _get_component_from_sub_element(selection_obj, sub_element_name)
    return component


def get_freecad_objects_list(preferred_component_names=None):
    objs_sel = []
    for selection in FreeCADGui.Selection.getSelectionEx():
        sub_element_names = selection.SubElementNames or [None]
        for sub_element_name in sub_element_names:
            component = resolve_selection_component(
                selection, sub_element_name, preferred_component_names)
            if component not in objs_sel:
                objs_sel.append(component)
    return objs_sel


def get_freecad_faces_objects_list(preferred_component_names=None):
    face_obj_list = []
    for selection_obj in FreeCADGui.Selection.getSelectionEx():
        index = 0
        for face in selection_obj.SubObjects:
            sub_element_name = selection_obj.SubElementNames[index]
            component = resolve_selection_component(
                selection_obj, sub_element_name, preferred_component_names)
            local_face_name = _get_local_sub_element_name(sub_element_name)
            try:
                local_face = component.Shape.getElement(local_face_name)
            except Exception:
                local_face = face
                _debug("Using selected face for %s.%s" %
                       (component.Name, local_face_name))
            _debug("Selected face %s on component %s" %
                   (local_face_name, component.Name))
            face_obj_list.append({'freecad_object': component, 'face': local_face,
                                  'name': local_face_name})
            index += 1
    return face_obj_list
