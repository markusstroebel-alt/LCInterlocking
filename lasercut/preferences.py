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
