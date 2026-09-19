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
from lasercut import helper
from lasercut import preferences


class TabProperties(helper.ObjectProperties):

    TYPE_TAB = 'Tab'
    TYPE_T_SLOT = 'Screw'
    TYPE_CONTINUOUS = 'Continuous'
    TYPE_FLEX = 'Flexible'
    TYPE_WOOD_SCREW = 'WoodScrew'
    TYPE_SCREW_IN_NUT = 'ScrewInNut'
    TYPE_NOT_DEFINED = 'Not Defined'

    _allowed = ('face_name', 'y_length', 'thickness', 'tabs_width', 'tabs_number', 'tabs_shift',
                'dog_bone', 'tab_dog_bone', 'screw_diameter', 'screw_length', 'screw_length_tol', 'makeScrew',
                'y_invert', 'half_tab_ratio', 'interval_ratio', 'freecad_obj_name',
                'tab_type', 'group_id', 'description', 'link_name', 'tab_name', 'transform_matrix',
                'through_tabs', 'tab_length', 'tab_length_tolerance',
                'nut_flat_flat', 'nut_height', 'nut_slot_overhang', 'thread_clearance',
                'use_washer', 'washer_diameter', 'washer_thickness',
                'nut_outer_diameter', 'nut_depth', 'head_clearance')

    __count = 0

    # Suggested defaults for new connections, updated with the last values used by the user.
    _last_nut_washer_values = {}

    @classmethod
    def _count(cls):
        TabProperties.__count += 1
        return TabProperties.__count

    def __init__(self, **kwargs):
        super(TabProperties, self).__init__(**kwargs)
        self.freecad_object = None
        self.freecad_face = None
        self.transform_matrix = None
        if not kwargs['freecad_face']:
            raise ValueError("Must init with freecad face")
        if not hasattr(self, 'freecad_obj_name') :#or not hasattr(self, 'freecad_face'):
            raise ValueError("Must defined freecad face/object")
        if not hasattr(self, 'tab_type'):
            raise ValueError("no type of tab defined")
        if not hasattr(self, 'face_name'):
            #self.face_name = self.freecad_face['name']
            raise ValueError("name not defined")
        if not hasattr(self, 'tab_name'):
            self.tab_name = "%s.%s" % (self.freecad_obj_name, self.face_name)
        if not hasattr(self, 'description'):
            self.description = "%s.%s (%s)" % (self.freecad_obj_name, self.face_name, self.tab_type)
        if not hasattr(self, 'y_length') or not hasattr(self, 'thickness') or not hasattr(self, 'transform_matrix'):
            try:
                x_local, y_length, thickness = helper.get_local_axis(kwargs['freecad_face'])
                self.thickness = thickness.Length
                self.y_length = y_length.Length
            except ValueError as e:
                FreeCAD.Console.PrintError(e)
        if not hasattr(self, 'tabs_number'):
            self.tabs_number = 1
        if not hasattr(self, 'tabs_width'):
            self.tabs_width = 10
        if not hasattr(self, 'tabs_shift'):
            self.tabs_shift = 0.
        if not hasattr(self, 'interval_ratio'):
            self.interval_ratio = 1.
        if not hasattr(self, 'half_tab_ratio'):
            self.half_tab_ratio = 1.
        if not hasattr(self, 'screw_diameter'):
            self.screw_diameter = preferences.get_default_screw_diameter()
        if not hasattr(self, 'screw_length'):
            self.screw_length = preferences.get_default_screw_length()
        legacy_screw_length_tol = getattr(self, 'screw_length_tol', None)
        if not hasattr(self, 'screw_length_tol'):
            self.screw_length_tol = 0.5
        if not hasattr(self, 'nut_slot_overhang'):
            self.nut_slot_overhang = (legacy_screw_length_tol
                                      if legacy_screw_length_tol is not None
                                      else preferences.get_default_nut_slot_overhang())
        if not hasattr(self, 'thread_clearance'):
            self.thread_clearance = preferences.get_default_thread_clearance()
        if not hasattr(self, 'nut_outer_diameter'):
            self.nut_outer_diameter = preferences.get_default_nut_outer_diameter()
        if not hasattr(self, 'nut_depth'):
            self.nut_depth = preferences.get_default_nut_depth()
        if not hasattr(self, 'head_clearance'):
            self.head_clearance = 0.0
        if not hasattr(self, 'through_tabs'):
            self.through_tabs = True
        if not hasattr(self, 'tab_length'):
            self.tab_length = 0.0
        if not hasattr(self, 'tab_length_tolerance'):
            self.tab_length_tolerance = 0.5
        if not hasattr(self, 'nut_flat_flat'):
            self.nut_flat_flat = self._last_nut_washer_values.get(
                'nut_flat_flat', preferences.get_default_nut_flat_flat())
        if not hasattr(self, 'nut_height'):
            self.nut_height = self._last_nut_washer_values.get(
                'nut_height', preferences.get_default_nut_height())
        if not hasattr(self, 'use_washer'):
            self.use_washer = self._last_nut_washer_values.get(
                'use_washer', preferences.get_default_use_washer())
        if not hasattr(self, 'washer_diameter'):
            self.washer_diameter = self._last_nut_washer_values.get(
                'washer_diameter', preferences.get_default_washer_diameter())
        if not hasattr(self, 'washer_thickness'):
            self.washer_thickness = self._last_nut_washer_values.get(
                'washer_thickness', preferences.get_default_washer_thickness())
        TabProperties._last_nut_washer_values = {
            'nut_flat_flat': self.nut_flat_flat,
            'nut_height': self.nut_height,
            'use_washer': self.use_washer,
            'washer_diameter': self.washer_diameter,
            'washer_thickness': self.washer_thickness,
        }
        if not hasattr(self, 'dog_bone'):
            self.dog_bone = True
        if not hasattr(self, 'tab_dog_bone'):
            self.tab_dog_bone = False
        if not hasattr(self, 'y_invert'):
            self.y_invert = False
        self.group_id = self._count()
        if not hasattr(self, 'link_name'):
            self.link_name = ""

    def recomputeInit(self, freecad_obj, freecad_face):
        self.freecad_object = freecad_obj
        self.freecad_face = freecad_face
        x_local, y_length, thickness = helper.get_local_axis(freecad_face)
        self.thickness = thickness.Length
        self.y_length = y_length.Length
        self.transform_matrix = helper.get_matrix_transform(freecad_face)