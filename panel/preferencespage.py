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

        layout = QtGui.QFormLayout(self)
        layout.addRow("Thickness tolerance (mm)", self.thickness_tolerance_spin)
        layout.addRow("Laser beam diameter (mm)", self.laser_beam_diameter_spin)
        layout.addRow("Slot width tolerance (mm)", self.hole_width_tolerance_spin)

    def loadSettings(self):
        self.thickness_tolerance_spin.setValue(preferences.get_default_thickness_tolerance())
        self.laser_beam_diameter_spin.setValue(preferences.get_default_laser_beam_diameter())
        self.hole_width_tolerance_spin.setValue(preferences.get_default_hole_width_tolerance())

    def saveSettings(self):
        preferences.set_defaults(self.thickness_tolerance_spin.value(),
                                 self.laser_beam_diameter_spin.value(),
                                 self.hole_width_tolerance_spin.value())
