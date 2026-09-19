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

PREFERENCES_GROUP = "User parameter:BaseApp/Preferences/Mod/LCInterlocking"

DEFAULT_THICKNESS_TOLERANCE = 0.1
DEFAULT_LASER_BEAM_DIAMETER = 0.1
DEFAULT_HOLE_WIDTH_TOLERANCE = 0.0
DEFAULT_SCREW_DIAMETER = 3.0
DEFAULT_SCREW_LENGTH = 15.0
DEFAULT_NUT_FLAT_FLAT = 5.5
DEFAULT_NUT_HEIGHT = 2.4
DEFAULT_NUT_SLOT_OVERHANG = 0.5
DEFAULT_THREAD_CLEARANCE = 3.0
DEFAULT_USE_WASHER = False
DEFAULT_WASHER_DIAMETER = 7.0
DEFAULT_WASHER_THICKNESS = 0.5


def get_param_group():
    return FreeCAD.ParamGet(PREFERENCES_GROUP)


def get_default_thickness_tolerance():
    return get_param_group().GetFloat("ThicknessTolerance", DEFAULT_THICKNESS_TOLERANCE)


def get_default_laser_beam_diameter():
    return get_param_group().GetFloat("LaserBeamDiameter", DEFAULT_LASER_BEAM_DIAMETER)


def get_default_hole_width_tolerance():
    return get_param_group().GetFloat("HoleWidthTolerance", DEFAULT_HOLE_WIDTH_TOLERANCE)


def set_defaults(thickness_tolerance, laser_beam_diameter, hole_width_tolerance):
    param = get_param_group()
    param.SetFloat("ThicknessTolerance", thickness_tolerance)
    param.SetFloat("LaserBeamDiameter", laser_beam_diameter)
    param.SetFloat("HoleWidthTolerance", hole_width_tolerance)


def get_default_screw_diameter():
    return get_param_group().GetFloat("ScrewDiameter", DEFAULT_SCREW_DIAMETER)


def get_default_screw_length():
    return get_param_group().GetFloat("ScrewLength", DEFAULT_SCREW_LENGTH)


def get_default_nut_flat_flat():
    return get_param_group().GetFloat("NutFlatFlat", DEFAULT_NUT_FLAT_FLAT)


def get_default_nut_height():
    return get_param_group().GetFloat("NutHeight", DEFAULT_NUT_HEIGHT)


def get_default_nut_slot_overhang():
    return get_param_group().GetFloat("NutSlotOverhang", DEFAULT_NUT_SLOT_OVERHANG)


def get_default_thread_clearance():
    return get_param_group().GetFloat("ThreadClearance", DEFAULT_THREAD_CLEARANCE)


def get_default_use_washer():
    return get_param_group().GetBool("UseWasher", DEFAULT_USE_WASHER)


def get_default_washer_diameter():
    return get_param_group().GetFloat("WasherDiameter", DEFAULT_WASHER_DIAMETER)


def get_default_washer_thickness():
    return get_param_group().GetFloat("WasherThickness", DEFAULT_WASHER_THICKNESS)


def set_screw_defaults(screw_diameter, screw_length, nut_flat_flat, nut_height,
                       nut_slot_overhang, thread_clearance, use_washer,
                       washer_diameter, washer_thickness):
    param = get_param_group()
    param.SetFloat("ScrewDiameter", screw_diameter)
    param.SetFloat("ScrewLength", screw_length)
    param.SetFloat("NutFlatFlat", nut_flat_flat)
    param.SetFloat("NutHeight", nut_height)
    param.SetFloat("NutSlotOverhang", nut_slot_overhang)
    param.SetFloat("ThreadClearance", thread_clearance)
    param.SetBool("UseWasher", use_washer)
    param.SetFloat("WasherDiameter", washer_diameter)
    param.SetFloat("WasherThickness", washer_thickness)
