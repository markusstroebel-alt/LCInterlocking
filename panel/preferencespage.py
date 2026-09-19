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
import FreeCAD
from lasercut import preferences
from lasercut import presets


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
        self.nut_outer_diameter_spin = self._create_spin(0., 300.)
        self.nut_depth_spin = self._create_spin(0., 300.)

        self.presets_table = QtGui.QTableWidget(self)
        self.presets_table.setSortingEnabled(False)
        self.presets_table.setMinimumHeight(180)
        self.add_preset_button = QtGui.QPushButton("Add preset", self)
        self.delete_preset_button = QtGui.QPushButton("Delete selected", self)
        self.save_presets_button = QtGui.QPushButton("Save presets", self)
        self.add_preset_button.clicked.connect(self.add_preset_row)
        self.delete_preset_button.clicked.connect(self.delete_selected_preset_rows)
        self.save_presets_button.clicked.connect(self.save_preset_table)

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
        layout.addRow("ScrewInNut outer diameter (mm)", self.nut_outer_diameter_spin)
        layout.addRow("ScrewInNut depth (mm)", self.nut_depth_spin)
        layout.addRow("Global connection presets", self.presets_table)
        preset_buttons = QtGui.QHBoxLayout()
        preset_buttons.addWidget(self.add_preset_button)
        preset_buttons.addWidget(self.delete_preset_button)
        preset_buttons.addWidget(self.save_presets_button)
        layout.addRow("", preset_buttons)

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
        self.nut_outer_diameter_spin.setValue(preferences.get_default_nut_outer_diameter())
        self.nut_depth_spin.setValue(preferences.get_default_nut_depth())
        self.load_preset_table()

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
        preferences.set_screw_in_nut_defaults(self.nut_outer_diameter_spin.value(),
                                              self.nut_depth_spin.value())
        self.save_preset_table()

    def load_preset_table(self):
        rows = presets.get_preset_rows()
        property_names = presets.get_preset_property_names(rows)
        headers = ["Connection type", "Preset name"] + property_names
        self.presets_table.clear()
        self.presets_table.setColumnCount(len(headers))
        self.presets_table.setHorizontalHeaderLabels(headers)
        self.presets_table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            self._set_table_value(row_index, 0, row["tab_type"])
            self._set_table_value(row_index, 1, row["name"])
            for column_index, property_name in enumerate(property_names, 2):
                if property_name in row["values"]:
                    self._set_table_value(row_index, column_index,
                                          self._format_preset_value(row["values"][property_name]))
        self.presets_table.resizeColumnsToContents()

    def _set_table_value(self, row, column, value):
        self.presets_table.setItem(row, column, QtGui.QTableWidgetItem(str(value)))

    def _format_preset_value(self, value):
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    def add_preset_row(self):
        row = self.presets_table.rowCount()
        self.presets_table.insertRow(row)
        self._set_table_value(row, 0, "Screw")
        self._set_table_value(row, 1, "New preset")
        self.presets_table.selectRow(row)

    def delete_selected_preset_rows(self):
        rows = sorted({index.row() for index in self.presets_table.selectedIndexes()}, reverse=True)
        for row in rows:
            self.presets_table.removeRow(row)

    def save_preset_table(self):
        headers = [self.presets_table.horizontalHeaderItem(index).text()
                   for index in range(self.presets_table.columnCount())]
        rows = []
        for row_index in range(self.presets_table.rowCount()):
            tab_type = self._table_text(row_index, 0)
            name = self._table_text(row_index, 1)
            values = {}
            for column_index, property_name in enumerate(headers[2:], 2):
                text = self._table_text(row_index, column_index)
                if text:
                    values[property_name] = self._parse_preset_value(text)
            rows.append({"tab_type": tab_type, "name": name, "values": values})
        try:
            presets.save_preset_rows(rows)
        except ValueError as error:
            FreeCAD.Console.PrintError("Could not save presets: %s\n" % error)

    def _table_text(self, row, column):
        item = self.presets_table.item(row, column)
        return item.text().strip() if item else ""

    def _parse_preset_value(self, text):
        if text.lower() in ("true", "false"):
            return text.lower() == "true"
        try:
            return float(text)
        except ValueError:
            return text
