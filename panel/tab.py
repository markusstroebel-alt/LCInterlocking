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

from PySide import QtGui

from lasercut.tabproperties import TabProperties
from panel.toolwidget import ParamWidget, WidgetValue
import copy
import FreeCAD

class BaseTabWidget(ParamWidget):

    def __init__(self, tab_properties):
        self.name = tab_properties.face_name
        self.description = tab_properties.description # a supprimer ?
        self.tab_name = tab_properties.tab_name
        self.obj_name = tab_properties.freecad_obj_name
        self.link_name = None
        ParamWidget.__init__(self, tab_properties)
        self.widget_list.extend([self._connection_type_widget(),
                     WidgetValue(type=float, name="y_length", show_name="Width", widget=None),
                                 WidgetValue(type=float, name="thickness", show_name="Thickness", widget=None),
                                 WidgetValue(type=bool, name="through_tabs", show_name="Through tabs", widget=None),
                                 WidgetValue(type=float, name="tab_length", show_name="Tab length",
                                             widget=None, interval_value=[0.01, 3000.], step=0.5, decimals=2),
                                 WidgetValue(type=float, name="tab_length_tolerance", show_name="Tab length tolerance",
                                             widget=None, interval_value=[0., 100.], step=0.1, decimals=2),
                                WidgetValue(type=float, name="tabs_number", show_name="Number of tabs",
                                            widget=None, interval_value=[1., 300.], step=1., decimals=0),
                                WidgetValue(type=float, name="tabs_width", show_name="Width of tabs", widget=None,
                                            interval_value=[1., 300.], step=1., decimals=2),
                                WidgetValue(type=float, name="tabs_shift", show_name="Shift", widget=None,
                                            interval_value=[-300, 300.], step=1., decimals=2),
                                WidgetValue(type=float, name="interval_ratio", show_name="Interval ratio",
                                            widget=None, interval_value=[0.1, 5.], step=0.1, decimals=2),
                                WidgetValue(type=bool, name="dog_bone", show_name="Dog bone hole", widget=None),
                                WidgetValue(type=bool, name="tab_dog_bone", show_name="Tab dog bone hole", widget=None)
                                 ])

    def _connection_type_widget(self):
        return WidgetValue(type=list, name="tab_type", show_name="Connection type",
                           widget=None,
                           interval_value=list(TabProperties.CONNECTION_TYPES))

    def listchangeIndex(self, index):
        ParamWidget.listchangeIndex(self, index)
        self.object_property.set_tab_type(self.object_property.tab_type)

    def get_tab_type(self):
        return self.object_property.tab_type


class TabWidget(BaseTabWidget):

    def __init__(self, tab_properties):
        BaseTabWidget.__init__(self, tab_properties)


class TongueGrooveWidget(BaseTabWidget):

    HEIGHT_MODES = ["Full material thickness", "Custom height"]
    HEIGHT_ALIGNMENTS = ["Center", "Side A", "Side B"]

    def __init__(self, tab_properties):
        tab_properties.ensure_tongue_groove_properties()
        BaseTabWidget.__init__(self, tab_properties)
        self.widget_list = [
            self._connection_type_widget(),
            WidgetValue(type=float, name="y_length", show_name="Face width", widget=None),
            WidgetValue(type=float, name="thickness", show_name="Material thickness", widget=None),
            WidgetValue(type=float, name="tongue_groove_depth", show_name="Groove depth",
                        widget=None, interval_value=[0.01, 3000.], step=0.5, decimals=2),
            WidgetValue(type=list, name="tongue_groove_height_mode", show_name="Height mode",
                        widget=None, interval_value=self.HEIGHT_MODES),
            WidgetValue(type=float, name="tongue_groove_height", show_name="Tongue height",
                        widget=None, interval_value=[0.01, 3000.], step=0.1, decimals=2,
                        parent_name="tongue_groove_height_mode", parent_value=["Custom height"]),
            WidgetValue(type=list, name="tongue_groove_alignment", show_name="Height alignment",
                        widget=None, interval_value=self.HEIGHT_ALIGNMENTS),
            WidgetValue(type=float, name="tongue_groove_bottom_clearance",
                        show_name="Groove bottom clearance", widget=None,
                        interval_value=[0.0, 300.], step=0.1, decimals=2),
            WidgetValue(type=bool, name="dog_bone", show_name="Dog bone hole", widget=None),
        ]


class WoodScrewWidget(BaseTabWidget):

    def __init__(self, tab_properties):
        BaseTabWidget.__init__(self, tab_properties)

        self.widget_list.extend([WidgetValue(type=float, name="half_tab_ratio", show_name="Half tab ratio",
                                             widget=None, interval_value=[0.1, 5.], step=0.1, decimals=2),
                                WidgetValue(type=float, name="screw_diameter", show_name="Screw diameter",
                                            widget=None, interval_value=[1., 30.], step=1., decimals=2.)])


class ScrewInNutWidget(BaseTabWidget):

    def __init__(self, tab_properties):
        BaseTabWidget.__init__(self, tab_properties)

        self.widget_list.extend([WidgetValue(type=float, name="half_tab_ratio", show_name="Half tab ratio",
                                             widget=None, interval_value=[0.1, 5.], step=0.1, decimals=2),
                                WidgetValue(type=float, name="screw_diameter", show_name="Screw diameter",
                                            widget=None, interval_value=[1., 100.], step=0.1, decimals=2),
                                WidgetValue(type=float, name="screw_length", show_name="Screw length",
                                            widget=None, interval_value=[1., 3000.], step=0.5, decimals=2),
                                WidgetValue(type=float, name="nut_flat_flat", show_name="Head pocket width",
                                            widget=None, interval_value=[1., 300.], step=0.1, decimals=2),
                                WidgetValue(type=float, name="nut_height", show_name="Head pocket length",
                                            widget=None, interval_value=[0.1, 300.], step=0.1, decimals=2),
                                WidgetValue(type=float, name="head_clearance", show_name="Head clearance",
                                            widget=None, interval_value=[0., 300.], step=0.1, decimals=2),
                                WidgetValue(type=float, name="nut_outer_diameter", show_name="Nut outer diameter",
                                            widget=None, interval_value=[1., 300.], step=0.1, decimals=2),
                                WidgetValue(type=float, name="nut_depth", show_name="Nut depth",
                                            widget=None, interval_value=[0.1, 300.], step=0.1, decimals=2),
                                WidgetValue(type=bool, name="use_nut_flange_pocket",
                                            show_name="Use nut flange pocket", widget=None),
                                WidgetValue(type=float, name="nut_flange_diameter",
                                            show_name="Flange pocket diameter", widget=None,
                                            interval_value=[1., 300.], step=0.1, decimals=2,
                                            parent_name="use_nut_flange_pocket", parent_value=[True]),
                                WidgetValue(type=float, name="nut_flange_depth",
                                            show_name="Flange pocket depth", widget=None,
                                            interval_value=[0.1, 300.], step=0.1, decimals=2,
                                            parent_name="use_nut_flange_pocket", parent_value=[True]),
                                WidgetValue(type=float, name="thread_clearance", show_name="Thread clearance",
                                            widget=None, interval_value=[0., 300.], step=0.1, decimals=2),
                                WidgetValue(type=bool, name="use_washer", show_name="Use washer", widget=None),
                                WidgetValue(type=float, name="washer_diameter", show_name="Washer diameter",
                                            widget=None, interval_value=[1., 300.], step=0.1, decimals=2,
                                            parent_name="use_washer", parent_value=[True]),
                                WidgetValue(type=float, name="washer_thickness", show_name="Washer thickness",
                                            widget=None, interval_value=[0.1, 100.], step=0.1, decimals=2,
                                            parent_name="use_washer", parent_value=[True])])


class TSlotWidget(BaseTabWidget):

    def __init__(self, tab_properties):
        BaseTabWidget.__init__(self, tab_properties)

        self.widget_list.extend([WidgetValue(type=float, name="half_tab_ratio", show_name="Half tab ratio",
                                             widget=None, interval_value=[0.1, 5.], step=0.1, decimals=2),
                                WidgetValue(type=float, name="screw_diameter", show_name="Screw diameter",
                                            widget=None, interval_value=[1., 30.], step=1., decimals=2.),
                                WidgetValue(type=float, name="screw_length", show_name="Screw length",
                                            widget=None, interval_value=[5., 300.], step=1., decimals=2.),
                                WidgetValue(type=float, name="nut_slot_overhang", show_name="Nut slot overhang",
                                            widget=None, interval_value=[0., 300.], step=0.1, decimals=2.),
                                WidgetValue(type=float, name="thread_clearance", show_name="Thread clearance",
                                            widget=None, interval_value=[0., 300.], step=0.1, decimals=2.),
                                WidgetValue(type=float, name="nut_flat_flat", show_name="Nut flat to flat",
                                            widget=None, interval_value=[1., 100.], step=0.5, decimals=2.),
                                WidgetValue(type=float, name="nut_height", show_name="Nut height",
                                            widget=None, interval_value=[1., 100.], step=0.5, decimals=2.),
                                WidgetValue(type=bool, name="use_washer", show_name="Use washer", widget=None),
                                WidgetValue(type=float, name="washer_diameter", show_name="Washer diameter",
                                            widget=None, interval_value=[1., 100.], step=0.5, decimals=2.,
                                            parent_name="use_washer", parent_value=[True]),
                                WidgetValue(type=float, name="washer_thickness", show_name="Washer thickness",
                                            widget=None, interval_value=[0.1, 20.], step=0.1, decimals=2.,
                                            parent_name="use_washer", parent_value=[True])])


class TabContinuousWidget(BaseTabWidget):

    def __init__(self, tab_properties):
        BaseTabWidget.__init__(self, tab_properties)

        self.widget_list = [self._connection_type_widget(),
                     WidgetValue(type=float, name="y_length", show_name="Width", widget=None),
                            WidgetValue(type=float, name="thickness", show_name="Thickness", widget=None),
                    WidgetValue(type=bool, name="through_tabs", show_name="Through tabs", widget=None),
                    WidgetValue(type=float, name="tab_length", show_name="Tab length", widget=None,
                                        interval_value=[0.01, 3000.], step=0.5, decimals=2),
                            WidgetValue(type=float, name="tab_length_tolerance", show_name="Tab length tolerance",
                                        widget=None, interval_value=[0., 100.], step=0.1, decimals=2),
                            WidgetValue(type=float, name="tabs_number", show_name="Number of elements",
                                            widget=None, interval_value=[2., 300.], step=1., decimals=0),
                            WidgetValue(type=bool, name="y_invert", show_name="Invert Y", widget=None),
                            WidgetValue(type=bool, name="dog_bone", show_name="Dog bone hole", widget=None),
                            WidgetValue(type=bool, name="tab_dog_bone", show_name="Tab dog bone hole", widget=None)]


class TabFlexWidget(BaseTabWidget):

    def __init__(self, tab_properties):
        BaseTabWidget.__init__(self, tab_properties)

        self.widget_list = [self._connection_type_widget(),
                     WidgetValue(type=bool, name="through_tabs", show_name="Through tabs", widget=None),
                    WidgetValue(type=float, name="tab_length", show_name="Tab length", widget=None,
                                        interval_value=[0.01, 3000.], step=0.5, decimals=2),
                            WidgetValue(type=float, name="tab_length_tolerance", show_name="Tab length tolerance",
                                        widget=None, interval_value=[0., 100.], step=0.1, decimals=2),
                    WidgetValue(type=float, name="tabs_width", show_name="Width of tabs", widget=None,
                                            interval_value=[1., 300.], step=1., decimals=2),
                            WidgetValue(type=bool, name="y_invert", show_name="Invert Y", widget=None),
                            WidgetValue(type=bool, name="dog_bone", show_name="Dog bone hole", widget=None)]


class TabLink(ParamWidget):

    def __init__(self, tab_properties):
        self.name = tab_properties.face_name
        self.description = tab_properties.description
        self.tab_name = tab_properties.tab_name
        self.obj_name = tab_properties.freecad_obj_name
        self.link_name =  tab_properties.link_name

        ParamWidget.__init__(self, tab_properties)
        self.widget_list.extend([WidgetValue(type=bool, name="y_invert", show_name="Invert Y", widget=None)])

    def get_group_box(self, widget):
        group_box = QtGui.QGroupBox(widget)
        group_box.setFlat(False)
        self.form = widget
        grid = self.get_grid()
        title = QtGui.QLabel(self.form)
        title.setText("Linked tab to : %s" % self.link_name)
        grid.addWidget(title, 1, 0, 1, 2)
        group_box.setLayout(grid)
        group_box.setTitle(self.name)
        return group_box, grid


class TabsList(object):

    def __init__(self, faces):
        self.faces = faces
        self.faces_widget_list = []
        return

    # def resumeWidget(self):
    #     for face in self.faces:
    #         if not face.link_name:
    #             self.faces_widget_list.append(self.createWidgetFromTabProperties(face))
    #         else:
    #             self.faces_widget_list.append(TabLink(face))
    #     return self.faces_widget_list

    def createWidgetFromTabProperties(self, tab_properties):
        widget = None
        tab_type = tab_properties.tab_type

        if tab_type == TabProperties.TYPE_TAB:
            widget = TabWidget(tab_properties)
        elif tab_type == TabProperties.TYPE_T_SLOT:
            widget = TSlotWidget(tab_properties)
        elif tab_type == TabProperties.TYPE_CONTINUOUS:
            widget = TabContinuousWidget(tab_properties)
        elif tab_type == TabProperties.TYPE_WOOD_SCREW:
            widget = WoodScrewWidget(tab_properties)
        elif tab_type == TabProperties.TYPE_SCREW_IN_NUT:
            widget = ScrewInNutWidget(tab_properties)
        elif tab_type == TabProperties.TYPE_TONGUE_GROOVE:
            widget = TongueGrooveWidget(tab_properties)
        #elif tab_type == TabProperties.TYPE_FLEX:
        #    widget = TabFlexWidget(tab_properties)
        else:
            raise ValueError("Unknown type of tab")

        return widget

    def append(self, face, tab_type):
        name = face["name"]
        tab_properties = TabProperties(freecad_face=face['face'],
                                       freecad_obj_name=face['freecad_object'].Name,
                                       face_name=name,
                                       tab_type=tab_type)
        self._assign_connection_id(tab_properties)

        #widget = self.createWidgetFromTabProperties(tab_properties)
        self.faces.append(tab_properties)
        #self.faces_widget_list.append(widget)
        return self.faces[-1]#, self.faces_widget_list[-1]

    def append_link(self, face, src_tab_name):
        src_tab_element, widget = self.get(src_tab_name)
        if src_tab_element is None:
            raise ValueError("No original part found (%s)" % src_tab_name)
        name = face["name"]
        tab_properties = TabProperties(freecad_face=face['face'],
                                       freecad_obj_name=face['freecad_object'].Name,
                                       face_name=name,
                                       tab_type=TabProperties.TYPE_NOT_DEFINED,
                                       link_name=src_tab_name)
        self._assign_connection_id(tab_properties)

        self.faces.append(tab_properties)
        #self.faces_widget_list.append(TabLink(tab_properties))
        return self.faces[-1]#, self.faces_widget_list[-1]

    def _assign_connection_id(self, tab_properties):
        connection_base = "%s.%s" % (tab_properties.freecad_obj_name,
                                      tab_properties.face_name)
        used_ids = set(tab.connection_id for tab in self.faces
                       if hasattr(tab, 'connection_id'))
        connection_index = 1
        connection_id = "%s#%d" % (connection_base, connection_index)
        while connection_id in used_ids:
            connection_index += 1
            connection_id = "%s#%d" % (connection_base, connection_index)
        tab_properties.connection_id = connection_id
        tab_properties.tab_name = connection_id

    def get_display_name(self, tab_properties):
        tab_type = tab_properties.tab_type
        if tab_properties.link_name:
            master_tab, unused_widget = self.get(tab_properties.link_name)
            if master_tab:
                tab_type = master_tab.tab_type

        matching_tabs = [tab for tab in self.faces
                         if tab.freecad_obj_name == tab_properties.freecad_obj_name
                         and tab.face_name == tab_properties.face_name
                         and self._get_tab_type(tab) == tab_type]
        type_label = tab_type
        if len(matching_tabs) > 1:
            type_label = "%s #%d" % (tab_type,
                                      matching_tabs.index(tab_properties) + 1)
        if tab_properties.link_name:
            type_label = "%s, linked" % type_label
        return "%s (%s)" % (tab_properties.face_name, type_label)

    def _get_tab_type(self, tab_properties):
        if tab_properties.link_name:
            master_tab, unused_widget = self.get(tab_properties.link_name)
            if master_tab:
                return master_tab.tab_type
        return tab_properties.tab_type

    def remove(self, name):
        found_index = None
        linked_tabs = self.get_linked_tabs(name)
        if len(linked_tabs) > 0:
            raise ValueError('Some tabs are linked to this part %s' % name)

        for index in range(len(self.faces)):
            if self.faces[index].tab_name == name:
                found_index = index
                break

        if found_index is not None:
            self.faces.pop(found_index)

    def exist(self, name):
        for part in self.faces:
            if part.tab_name == name:
                return True
        return False

    def get(self, name):
        #FreeCAD.Console.PrintMessage("get " + name + "\n")
        for index in range(len(self.faces)):
            if self.faces[index].tab_name == name:
                #FreeCAD.Console.PrintMessage("found " + name + "\n")
                face = self.faces[index]
                if not face.link_name:
                    widget = self.createWidgetFromTabProperties(face)
                else:
                    widget = TabLink(face)
                return face, widget


        return None, None

    def get_linked_tabs(self, name):
        return [tab for tab in self.faces if tab.link_name == name]

    def __iter__(self):
        return iter(self.faces)

    def get_tabs_properties(self):
        tabs_properties = []
        for tab in self.faces.lst:
            if tab.link_name:
                tab_link, widget = self.get(tab.link_name)
                new_tab = copy.deepcopy(tab_link)
                new_tab.link_name = tab.link_name
                new_tab.tab_name = tab.tab_name
                new_tab.connection_id = tab.connection_id
                new_tab.face_name = tab.face_name
                new_tab.freecad_obj_name = tab.freecad_obj_name
                new_tab.y_invert = tab.y_invert
                new_tab.transform_matrix = tab.transform_matrix
                new_tab.thickness = tab.thickness
                new_tab.y_length = tab.y_length
                new_tab.description = "%s.%s (%s)" % (new_tab.freecad_obj_name,
                                                        new_tab.face_name,
                                                        new_tab.tab_type)

                tabs_properties.append(new_tab)
            else:
                tabs_properties.append(copy.deepcopy(tab))

        self.faces.lst = tabs_properties

        return tabs_properties




