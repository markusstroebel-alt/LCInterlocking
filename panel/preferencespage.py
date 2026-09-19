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
from lasercut import preferences


class LCInterlockingPreferencesPage(QtGui.QWidget):

    def __init__(self, parent=None):
        super(LCInterlockingPreferencesPage, self).__init__(parent)
        self.setWindowTitle("LCInterlocking")

        self.thickness_tolerance_spin = QtGui.QDoubleSpinBox(self)
        self.thickness_tolerance_spin.setDecimals(3)
        self.thickness_tolerance_spin.setSingleStep(0.01)
        self.thickness_tolerance_spin.setRange(0., 100.)

        self.laser_beam_diameter_spin = QtGui.QDoubleSpinBox(self)
        self.laser_beam_diameter_spin.setDecimals(3)
        self.laser_beam_diameter_spin.setSingleStep(0.01)
        self.laser_beam_diameter_spin.setRange(0., 100.)

        self.hole_width_tolerance_spin = QtGui.QDoubleSpinBox(self)
        self.hole_width_tolerance_spin.setDecimals(3)
        self.hole_width_tolerance_spin.setSingleStep(0.01)
        self.hole_width_tolerance_spin.setRange(0., 100.)

        self.screw_diameter_spin = self._create_spin(0., 100.)
        self.screw_length_spin = self._create_spin(0., 3000.)
        self.nut_flat_flat_spin = self._create_spin(0., 300.)
        self.nut_height_spin = self._create_spin(0., 300.)
        self.nut_slot_overhang_spin = self._create_spin(0., 300.)
        self.thread_clearance_spin = self._create_spin(0., 300.)
        self.use_washer_check = QtGui.QCheckBox("", self)
        self.washer_diameter_spin = self._create_spin(0., 300.)
        self.washer_thickness_spin = self._create_spin(0., 100.)

        layout = QtGui.QFormLayout(self)
        layout.addRow("Thickness tolerance (mm)", self.thickness_tolerance_spin)
        layout.addRow("Laser beam diameter (mm)", self.laser_beam_diameter_spin)
        layout.addRow("Slot width tolerance (mm)", self.hole_width_tolerance_spin)
        layout.addRow("Screw diameter (mm)", self.screw_diameter_spin)
        layout.addRow("Screw length (mm)", self.screw_length_spin)
        layout.addRow("Nut flat to flat (mm)", self.nut_flat_flat_spin)
        layout.addRow("Nut height (mm)", self.nut_height_spin)
        layout.addRow("Nut slot overhang (mm)", self.nut_slot_overhang_spin)
        layout.addRow("Thread clearance (mm)", self.thread_clearance_spin)
        layout.addRow("Use washer", self.use_washer_check)
        layout.addRow("Washer diameter (mm)", self.washer_diameter_spin)
        layout.addRow("Washer thickness (mm)", self.washer_thickness_spin)

    def _create_spin(self, minimum, maximum):
        spin = QtGui.QDoubleSpinBox(self)
        spin.setDecimals(3)
        spin.setSingleStep(0.1)
        spin.setRange(minimum, maximum)
        return spin

    def loadSettings(self):
        self.thickness_tolerance_spin.setValue(preferences.get_default_thickness_tolerance())
        self.laser_beam_diameter_spin.setValue(preferences.get_default_laser_beam_diameter())
        self.hole_width_tolerance_spin.setValue(preferences.get_default_hole_width_tolerance())
        self.screw_diameter_spin.setValue(preferences.get_default_screw_diameter())
        self.screw_length_spin.setValue(preferences.get_default_screw_length())
        self.nut_flat_flat_spin.setValue(preferences.get_default_nut_flat_flat())
        self.nut_height_spin.setValue(preferences.get_default_nut_height())
        self.nut_slot_overhang_spin.setValue(preferences.get_default_nut_slot_overhang())
        self.thread_clearance_spin.setValue(preferences.get_default_thread_clearance())
        self.use_washer_check.setChecked(preferences.get_default_use_washer())
        self.washer_diameter_spin.setValue(preferences.get_default_washer_diameter())
        self.washer_thickness_spin.setValue(preferences.get_default_washer_thickness())

    def saveSettings(self):
        preferences.set_defaults(self.thickness_tolerance_spin.value(),
                                 self.laser_beam_diameter_spin.value(),
                                 self.hole_width_tolerance_spin.value())
        preferences.set_screw_defaults(
            self.screw_diameter_spin.value(), self.screw_length_spin.value(),
            self.nut_flat_flat_spin.value(), self.nut_height_spin.value(),
            self.nut_slot_overhang_spin.value(), self.thread_clearance_spin.value(),
            self.use_washer_check.isChecked(), self.washer_diameter_spin.value(),
            self.washer_thickness_spin.value())
