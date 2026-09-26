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


def _get_component_from_sub_element(selection_obj, sub_element_name):
    if not sub_element_name or '.' not in sub_element_name:
        return selection_obj.Object

    component_name = sub_element_name.split('.', 1)[0]
    component = selection_obj.Object.Document.getObject(component_name)
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


def _get_link_component_for_object(document, selected_object):
    for document_object in document.Objects:
        linked_object = getattr(document_object, 'LinkedObject', None)
        if linked_object and _contains_object(linked_object, selected_object):
            return document_object
    return selected_object


def get_freecad_objects_list():
    objs_sel = []
    for selection in FreeCADGui.Selection.getSelectionEx():
        sub_element_names = selection.SubElementNames or [None]
        for sub_element_name in sub_element_names:
            component = _get_component_from_sub_element(selection, sub_element_name)
            if component not in objs_sel:
                objs_sel.append(component)
    return objs_sel


def get_freecad_faces_objects_list():
    face_obj_list = []
    for selection_obj in FreeCADGui.Selection.getSelectionEx():
        index = 0
        for face in selection_obj.SubObjects:
            sub_element_name = selection_obj.SubElementNames[index]
            component = _get_link_component_for_object(FreeCAD.ActiveDocument,
                                                       selection_obj.Object)
            if component == selection_obj.Object:
                component = _get_component_from_sub_element(selection_obj, sub_element_name)
            local_face_name = _get_local_sub_element_name(sub_element_name)
            try:
                local_face = component.Shape.getElement(local_face_name)
            except Exception:
                local_face = face
            face_obj_list.append({'freecad_object': component, 'face': local_face,
                                  'name': local_face_name})
            index += 1
    return face_obj_list
