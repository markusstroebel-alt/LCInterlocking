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

import json
import os
import FreeCAD

PRESETS_FILE_NAME = "LCInterlocking_presets.json"
KNOWN_PRESET_PROPERTIES = (
    "y_length", "thickness", "through_tabs", "tab_length", "tab_length_tolerance",
    "tabs_number", "tabs_width", "tabs_shift", "interval_ratio", "dog_bone",
    "tab_dog_bone", "y_invert", "half_tab_ratio", "screw_diameter", "screw_length",
    "screw_length_tol", "nut_flat_flat", "nut_height", "nut_slot_overhang",
    "thread_clearance", "use_washer", "washer_diameter", "washer_thickness")


def get_presets_file_path():
    return os.path.join(FreeCAD.getUserAppDataDir(), PRESETS_FILE_NAME)


def load_presets():
    path = get_presets_file_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r") as presets_file:
            return json.load(presets_file)
    except (ValueError, IOError) as e:
        FreeCAD.Console.PrintError("Could not read presets file: %s\n" % e)
        return {}


def save_presets(presets):
    path = get_presets_file_path()
    with open(path, "w") as presets_file:
        json.dump(presets, presets_file, indent=2)


def get_presets_for_type(tab_type):
    presets = load_presets()
    return presets.get(tab_type, [])


def add_or_update_preset(tab_type, name, values):
    presets = load_presets()
    type_presets = presets.setdefault(tab_type, [])
    for preset in type_presets:
        if preset["name"] == name:
            preset["values"] = values
            save_presets(presets)
            return
    type_presets.append({"name": name, "values": values})
    save_presets(presets)


def delete_preset(tab_type, name):
    presets = load_presets()
    type_presets = presets.get(tab_type, [])
    presets[tab_type] = [preset for preset in type_presets if preset["name"] != name]
    save_presets(presets)


def get_preset_rows():
    rows = []
    for tab_type, type_presets in load_presets().items():
        for preset in type_presets:
            rows.append({"tab_type": tab_type,
                         "name": preset.get("name", ""),
                         "values": dict(preset.get("values", {}))})
    return rows


def get_preset_property_names(rows=None):
    if rows is None:
        rows = get_preset_rows()
    names = set(KNOWN_PRESET_PROPERTIES)
    names.update(name for row in rows for name in row["values"])
    return sorted(names)


def save_preset_rows(rows):
    grouped = {}
    for row in rows:
        tab_type = str(row.get("tab_type", "")).strip()
        name = str(row.get("name", "")).strip()
        if not tab_type or not name:
            raise ValueError("Preset type and name are required")
        grouped.setdefault(tab_type, [])
        if any(item["name"] == name for item in grouped[tab_type]):
            raise ValueError("Duplicate preset name: %s" % name)
        grouped[tab_type].append({"name": name, "values": dict(row.get("values", {}))})
    save_presets(grouped)
