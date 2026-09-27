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

import Part
import FreeCAD
from panel.tab import TabProperties
import lasercut.flextab as flextab
import lasercut.helper as helper


def _debug(message):
    FreeCAD.Console.PrintMessage("[LCInterlocking] %s\n" % message)


class JoinContext(object):
    def __init__(self):
        self.screw_clearances = []
        self.tongue_targets = []

    def register_screw_clearance(self, tab, counter_part, clearance):
        self.screw_clearances.append((tab.freecad_object.Name, tab.face_name,
                                      counter_part.get_name(), clearance))

    def register_tongue_target(self, tab, tab_part, counter_part):
        self.tongue_targets.append((tab.freecad_object.Name, tab.face_name,
                                    counter_part.get_name(), tab_part))

    def apply_screw_clearances_to_tongues(self):
        clearance_count = 0
        for source_name, face_name, counter_name, tab_part in self.tongue_targets:
            for screw_source, screw_face, screw_counter, clearance in self.screw_clearances:
                if (source_name == screw_source and face_name == screw_face
                        and counter_name == screw_counter):
                    tab_part.toRemove.append(clearance)
                    clearance_count += 1
        if clearance_count:
            _debug("Removed %d Screw clearance volumes from TongueGroove additions" %
                   clearance_count)


def get_slot_positions(tab_properties):
    slots_list = []
    interval_length = tab_properties.y_length / float(tab_properties.tabs_number)
    half_tab_number = int(float(tab_properties.tabs_number) / 2.0)
    if tab_properties.tabs_number % 2 == 1:
        slots_list.append(0.0 + tab_properties.tabs_shift)
        for i in range(half_tab_number):
            left = float(i+1) * interval_length * tab_properties.interval_ratio
            right = float(-i-1) * interval_length * tab_properties.interval_ratio
            if tab_properties.interval_ratio != 1.0:
                left *= tab_properties.interval_ratio
                right *= tab_properties.interval_ratio
                right *= tab_properties.interval_ratio
            slots_list.append(left + tab_properties.tabs_shift)
            slots_list.append(right + tab_properties.tabs_shift)
    else:
        for i in range(half_tab_number):
            left = float(i) * interval_length + interval_length / 2.0
            right = float(-i) * interval_length - interval_length / 2.0
            if tab_properties.interval_ratio != 1.0:
                left *= tab_properties.interval_ratio
                right *= tab_properties.interval_ratio
            slots_list.append(left + tab_properties.tabs_shift)
            slots_list.append(right + tab_properties.tabs_shift)

    # if tab_properties.y_invert:
    #     invert_list = []
    #     for slot in slots_list:
    #         invert_list.append(-slot)
    #     slots_list = invert_list

    return slots_list


def screw_way_on_plane(material_plane, screw_nut_spec, pos_y):
    # horizontal hole
    radius = (screw_nut_spec.screw_diameter - material_plane.laser_beam_diameter) / 2.0
    cylinder = Part.makeCylinder(radius, material_plane.thickness, FreeCAD.Vector(0, 0, -material_plane.thickness / 2.))
    cylinder.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
    cylinder.translate(FreeCAD.Vector(material_plane.thickness / 2.0, pos_y, 0.))
    return cylinder


def screw_way_on_face(material_face, material_plane, screw_nut_spec, tab, pos_y, dog_bone=False):
    # horizontal hole
    if getattr(tab, 'tab_type', None) == TabProperties.TYPE_SCREW_IN_NUT:
        washer_thickness = tab.washer_thickness if tab.use_washer else 0.0
        vert_corrected_length = screw_nut_spec.screw_length - washer_thickness - tab.nut_depth
    else:
        vert_corrected_length = screw_nut_spec.screw_length - material_plane.thickness \
                                + material_plane.thickness_tolerance
    corrected_width = screw_nut_spec.screw_diameter - material_face.laser_beam_diameter
    screw_corrected_width = corrected_width
    corrected_height = material_face.thickness  # + materialFace.tolerance
    screw_hole = Part.makeBox(vert_corrected_length, corrected_width, corrected_height,
                              FreeCAD.Vector(0.,
                                             -corrected_width / 2.0, -corrected_height / 2.0))
    if dog_bone:
        screw_hole = helper.make_dog_bone_on_limits_on_xy(screw_hole, corrected_height, True)
    x_pos = -vert_corrected_length
    screw_hole.translate(FreeCAD.Vector(x_pos, pos_y, 0))
    hole = screw_hole

    if getattr(tab, 'tab_type', None) == TabProperties.TYPE_SCREW_IN_NUT:
        # The washer and head pocket follow the channel, away from the plate.
        # Their position must not change the channel reference or its length.
        pocket_x_pos = -vert_corrected_length
    else:
        # The normal Screw connection positions its nut/washer stack at the
        # far end of the channel.
        nut_depth_offset = tab.nut_height + tab.nut_slot_overhang \
                           + getattr(tab, 'screw_length_tol', 0.5)
        if tab.use_washer:
            nut_depth_offset += tab.washer_thickness
        pocket_x_pos = -vert_corrected_length + nut_depth_offset

    # Washer hole comes directly after the screw channel.
    if tab.use_washer:
        washer_length = tab.washer_thickness - material_face.laser_beam_diameter
        washer_width = tab.washer_diameter - material_face.laser_beam_diameter
        washer_hole = Part.makeBox(washer_length, washer_width, corrected_height,
                                   FreeCAD.Vector(0,
                                                  -washer_width / 2.0, -corrected_height / 2.0))
        washer_hole.translate(FreeCAD.Vector(pocket_x_pos - washer_length, pos_y, 0))
        if dog_bone:
            washer_hole = helper.make_dog_bone_on_limits_on_xy(washer_hole, corrected_height)
        hole = hole.fuse(washer_hole)
        pocket_x_pos -= washer_length

    # Nut hole follows the washer and keeps the actual nut dimensions only.
    corrected_length = tab.nut_height - material_face.laser_beam_diameter
    corrected_width = tab.nut_flat_flat - material_face.laser_beam_diameter
    nut_x_pos = pocket_x_pos - corrected_length
    nut_hole = Part.makeBox(corrected_length, corrected_width, corrected_height,
                            FreeCAD.Vector(0,
                                           -corrected_width / 2.0, -corrected_height / 2.0))
    nut_hole.translate(FreeCAD.Vector(nut_x_pos, pos_y, 0))
    if dog_bone:
        nut_hole = helper.make_dog_bone_on_limits_on_xy(nut_hole, corrected_height)
    hole = hole.fuse(nut_hole)

    if getattr(tab, 'tab_type', None) == TabProperties.TYPE_SCREW_IN_NUT:
        head_clearance_length = getattr(tab, 'head_clearance', 0.0)
        if head_clearance_length > 0.0:
            # Continue past the head pocket in screw width for Allen-key access.
            head_clearance_hole = Part.makeBox(
                head_clearance_length, screw_corrected_width, corrected_height,
                FreeCAD.Vector(nut_x_pos - head_clearance_length,
                               -screw_corrected_width / 2.0,
                               -corrected_height / 2.0))
            head_clearance_hole.translate(FreeCAD.Vector(0, pos_y, 0))
            hole = hole.fuse(head_clearance_hole)

    # Screw-width channel for the thread passing through and beyond the nut.
    overhang_length = tab.nut_slot_overhang - material_face.laser_beam_diameter
    effective_overhang_length = max(overhang_length, 0.0)
    if overhang_length > 0.0:
        overhang_x_pos = nut_x_pos - overhang_length
        overhang_hole = Part.makeBox(
            overhang_length, screw_corrected_width, corrected_height,
            FreeCAD.Vector(overhang_x_pos, -screw_corrected_width / 2.0,
                           -corrected_height / 2.0))
        overhang_hole.translate(FreeCAD.Vector(0, pos_y, 0))
        hole = hole.fuse(overhang_hole)

    # Thread clearance continues directly behind the nut/washer pockets.
    clearance_length = tab.thread_clearance - material_face.laser_beam_diameter
    if clearance_length > 0.0:
        clearance_x_pos = nut_x_pos - effective_overhang_length - clearance_length
        thread_clearance_hole = Part.makeBox(
            clearance_length, screw_corrected_width, corrected_height,
            FreeCAD.Vector(clearance_x_pos, -screw_corrected_width / 2.0,
                           -corrected_height / 2.0))
        thread_clearance_hole.translate(FreeCAD.Vector(0, pos_y, 0))
        hole = hole.fuse(thread_clearance_hole)
    return hole


def screw_in_nut_way_on_face(material_face, material_plane, tab, pos_y, dog_bone=False):
    washer_thickness = tab.washer_thickness if tab.use_washer else 0.0
    channel_length = tab.screw_length - washer_thickness - tab.nut_depth
    corrected_height = material_face.thickness
    screw_width = tab.screw_diameter - material_face.laser_beam_diameter
    if channel_length <= 0.0 or screw_width <= 0.0:
        raise ValueError("ScrewInNut dimensions leave no positive screw channel")

    pocket_x_pos = -channel_length
    hole = Part.makeBox(channel_length, screw_width, corrected_height,
                        FreeCAD.Vector(pocket_x_pos, -screw_width / 2.0,
                                       -corrected_height / 2.0))
    hole.translate(FreeCAD.Vector(0, pos_y, 0))

    if tab.use_washer:
        washer_length = tab.washer_thickness - material_face.laser_beam_diameter
        washer_width = tab.washer_diameter - material_face.laser_beam_diameter
        washer_hole = Part.makeBox(washer_length, washer_width, corrected_height,
                       FreeCAD.Vector(-washer_length,
                                                  -washer_width / 2.0,
                                                  -corrected_height / 2.0))
        washer_hole.translate(FreeCAD.Vector(0, pos_y, 0))
        hole = hole.fuse(washer_hole)
        pocket_x_pos = -washer_length

    nut_depth = tab.nut_depth - material_face.laser_beam_diameter
    nut_radius = (tab.nut_outer_diameter - material_face.laser_beam_diameter) / 2.0
    nut_x_pos = pocket_x_pos - nut_depth
    nut_hole = Part.makeCylinder(nut_radius, nut_depth,
                                 FreeCAD.Vector(nut_x_pos, pos_y, 0),
                                 FreeCAD.Vector(1, 0, 0))
    hole = hole.fuse(nut_hole)

    clearance_length = tab.thread_clearance - material_face.laser_beam_diameter
    if clearance_length > 0.0:
        clearance_hole = Part.makeBox(clearance_length, screw_width, corrected_height,
                          FreeCAD.Vector(nut_x_pos - clearance_length,
                                                     -screw_width / 2.0,
                                                     -corrected_height / 2.0))
        clearance_hole.translate(FreeCAD.Vector(0, pos_y, 0))
        hole = hole.fuse(clearance_hole)
    return hole


#            X (Length)
#            |
#            |
#            |
#            |Z (Height)
#            ---------------------------> Y (Width)
# X est vers le haut
# Y est aligné sur la face
# Z est devant la camera
def tab_join_create_tab_on_face(material_face, material_plane, width, pos_y, tab_face, dog_bone=False):

    y_plus_inside, y_minus_inside = helper.check_limit_y_on_for_tab(tab_face, material_face.thickness, pos_y, width,
                                                                    material_plane.thickness, material_face)
    # X Rien pr l'instant, mais on peut prendre en compte l'epaiseur variante de la piece opposé => length
    # Y Ajout d'un Kerf => width
    # Z Rien => height
    corrected_length = material_plane.thickness
    if not getattr(tab_face, 'through_tabs', True):
        corrected_length = tab_face.tab_length
    # corrected_width = width + materialFace.laser_beam_diameter
    corrected_height = material_face.thickness

    corrected_width = width  # - materialPlane.laser_beam_diameter
    corrected_width_center = corrected_width / 2.0
    if y_minus_inside and y_plus_inside:
        corrected_width += material_face.laser_beam_diameter
        corrected_width_center = corrected_width / 2.0
    elif y_minus_inside:
        corrected_width += material_face.laser_beam_diameter / 2.0
        corrected_width_center = (corrected_width + material_face.laser_beam_diameter / 2.0) / 2.0
    elif y_plus_inside:
        corrected_width += material_face.laser_beam_diameter / 2.0
        corrected_width_center = (corrected_width - material_face.laser_beam_diameter / 2.0) / 2.0

    #origin = FreeCAD.Vector(-corrected_length / 2.0, -corrected_width_center, -corrected_height / 2.0)
    origin = FreeCAD.Vector(0., -corrected_width_center, -corrected_height / 2.0)
    tab = Part.makeBox(corrected_length, corrected_width, corrected_height, origin)
    tab.translate(FreeCAD.Vector(0, pos_y, 0))

    hole = None
    left_hole = None
    right_hole = None

    if dog_bone:
        radius = min(corrected_width, corrected_length) * 2 / 30.
        if y_minus_inside:
            left_hole = Part.makeCylinder(radius, corrected_height,
                                          FreeCAD.Vector(0, -corrected_width_center + pos_y, -corrected_height / 2.0),
                                          FreeCAD.Vector(0, 0, 1.))
        if y_plus_inside:
            right_hole = Part.makeCylinder(radius, corrected_height,
                                           FreeCAD.Vector(0, -corrected_width_center + corrected_width + pos_y,
                                           -corrected_height / 2.0),
                                           FreeCAD.Vector(0, 0, 1.))
        hole = left_hole
        if hole and right_hole:
            hole = hole.fuse(right_hole)
        elif right_hole:
            hole = right_hole

    return tab, hole


def make_tab_join(tab, tab_part, other_parts):
    slots_pos = get_slot_positions(tab)
    for i, y in enumerate(slots_pos):
        for part_interactor in other_parts:
            tab_to_add, tab_dog_bone = tab_join_create_tab_on_face(tab_part.properties, part_interactor.properties,
                                                                   tab.tabs_width, y, tab, tab.tab_dog_bone)
            intersect_test, tab_to_add_transformed = helper.check_intersect(tab_to_add, tab,
                                                                            part_interactor.properties)

            if intersect_test:
                tab_part.toAdd.append(tab_to_add_transformed)
                if tab_dog_bone:
                    tab_part.toRemove.append(helper.transform_part(tab_dog_bone, tab))
                hole = helper.tab_join_create_hole_on_plane(tab, tab.tabs_width, y, tab_part.properties,
                                                            part_interactor.properties, tab.dog_bone)
                part_interactor.toRemove.append(helper.transform_part(hole, tab))
                break
    return


def _get_tongue_groove_height(tab, material_face):
    if tab.tongue_groove_height_mode == "Full material thickness":
        tongue_height = material_face.thickness
    else:
        tongue_height = tab.tongue_groove_height
    if tongue_height <= 0.0:
        raise ValueError("TongueGroove height must be positive")
    if tongue_height > material_face.thickness:
        raise ValueError("TongueGroove height cannot exceed the material thickness")
    return tongue_height


def _get_tongue_groove_z_origin(material_thickness, tongue_height, alignment):
    if alignment == "Center":
        return -tongue_height / 2.0
    if alignment == "Side A":
        return material_thickness / 2.0 - tongue_height
    if alignment == "Side B":
        return -material_thickness / 2.0
    raise ValueError("Unknown TongueGroove height alignment %s" % alignment)


def _get_tongue_groove_groove_z_origin(material_thickness, tongue_height,
                                       alignment, clearance):
    return _get_tongue_groove_z_origin(material_thickness, tongue_height,
                                       alignment) - clearance / 2.0


def _make_tongue_groove_box(depth, width, height, z_origin, direction):
    x_origin = 0.0 if direction > 0 else -depth
    return Part.makeBox(depth, width, height,
                        FreeCAD.Vector(x_origin, -width / 2.0, z_origin))


def make_tongue_groove_join(tab, tab_part, other_parts, join_context=None):
    tongue_depth = tab.tongue_groove_depth
    if tongue_depth <= 0.0:
        raise ValueError("TongueGroove depth must be positive")
    if tab.tongue_groove_bottom_clearance < 0.0:
        raise ValueError("TongueGroove bottom clearance cannot be negative")

    tongue_height = _get_tongue_groove_height(tab, tab_part.properties)
    tongue_width = tab.y_length
    probe_z_origin = _get_tongue_groove_z_origin(
        tab_part.properties.thickness, tongue_height, tab.tongue_groove_alignment)

    _debug("TongueGroove %s.%s: checking %d counter parts" %
           (tab.freecad_object.Name, tab.face_name, len(other_parts)))
    for part_interactor in other_parts:
        direction = None
        for candidate_direction in (1, -1):
            tongue_probe = _make_tongue_groove_box(
                tongue_depth, tongue_width, tongue_height, probe_z_origin,
                candidate_direction)
            tongue_probe_transformed = helper.transform_part(tongue_probe, tab)
            if part_interactor.properties.freecad_object.Shape.common(
                    tongue_probe_transformed).Volume > 0.001:
                direction = candidate_direction
                break
        if direction is None:
            _debug("TongueGroove %s.%s: no overlap with %s" %
                   (tab.freecad_object.Name, tab.face_name,
                    part_interactor.properties.freecad_object.Name))
            continue

        if direction < 0:
            _debug("TongueGroove %s.%s: using opposite face direction for %s" %
                   (tab.freecad_object.Name, tab.face_name,
                    part_interactor.properties.freecad_object.Name))

        groove_cross_section_clearance = part_interactor.properties.hole_width_tolerance
        tongue = _make_tongue_groove_box(tongue_depth, tongue_width, tongue_height,
                                         probe_z_origin, direction)
        tongue_transformed = helper.transform_part(tongue, tab)
        intersecting_tongue = part_interactor.properties.freecad_object.Shape.common(
            tongue_transformed)
        # Limit the tongue to the counter part's actual overlap. This keeps a longer
        # selected face from creating a tongue outside a shorter groove side.
        tab_part.toAdd.append(intersecting_tongue)
        groove_width = tongue_width + groove_cross_section_clearance
        groove_height = tongue_height + groove_cross_section_clearance
        groove_depth = tongue_depth + tab.tongue_groove_bottom_clearance
        groove_z_origin = _get_tongue_groove_groove_z_origin(
            tab_part.properties.thickness, tongue_height,
            tab.tongue_groove_alignment, groove_cross_section_clearance)
        groove = _make_tongue_groove_box(groove_depth, groove_width, groove_height,
                         groove_z_origin, direction)
        if tab.dog_bone:
            groove = helper.make_dog_bone_on_limits_on_yz(groove, groove_depth)
        groove_transformed = helper.transform_part(groove, tab)
        intersecting_groove = part_interactor.properties.freecad_object.Shape.common(
            groove_transformed)
        part_interactor.toRemove.append(intersecting_groove)
        if join_context:
            join_context.register_tongue_target(tab, tab_part, part_interactor)
        _debug("TongueGroove %s.%s: joined to %s" %
               (tab.freecad_object.Name, tab.face_name,
                part_interactor.properties.freecad_object.Name))
        break
    else:
        _debug("TongueGroove %s.%s: no counter part found" %
               (tab.freecad_object.Name, tab.face_name))
    return


def make_continuous_tab_joins(tab, tab_part, other_parts):
    tabs_number = int(tab.tabs_number - 1)
    virtual_tab_length = float(tab.y_length / float(int(tabs_number + 1)))
    y_pos = - tab.y_length / 2.0
    for tab_id in range(int(tabs_number + 1)):
        y_pos_center = y_pos + virtual_tab_length / 2.0
        # if tab.y_invert:
        #     y_pos_center = - y_pos_center
        left_kerf = False if tab_id == 0 else True
        right_kerf = False if tab_id == tabs_number else True
        if tab_id % 2 == 0:
            for part_interactor in other_parts:
                tab_to_add, tab_dog_bone = tab_join_create_tab_on_face(tab_part.properties, part_interactor.properties,
                                                                       virtual_tab_length, y_pos_center, tab,
                                                                       tab.tab_dog_bone)
                intersect_test, tab_to_add_transformed = helper.check_intersect(tab_to_add, tab,
                                                                                part_interactor.properties)
                if intersect_test:
                    tab_part.toAdd.append(tab_to_add_transformed)
                    if tab_dog_bone:
                        tab_part.toRemove.append(helper.transform_part(tab_dog_bone, tab))
                    hole = helper.tab_join_create_hole_on_plane(tab, virtual_tab_length, y_pos_center,
                                                                tab_part.properties, part_interactor.properties,
                                                                tab.dog_bone)
                    part_interactor.toRemove.append(helper.transform_part(hole, tab))
                    break
        y_pos += virtual_tab_length
    return


def create_tab_pairs_with_holes(tab, tab_part, other_parts, half_tab_distance,
                                join_context=None):
    # Shared by all screw-like tab types: creates the tabs (tenons) and their matching
    # holes, yielding (y, part_interactor) for each successfully matched slot position.
    slots_pos = get_slot_positions(tab)
    for i, y in enumerate(slots_pos):
        for part_interactor in other_parts:
            left_tab_to_add, left_tab_dog_bone = tab_join_create_tab_on_face(tab_part.properties,
                                                                             part_interactor.properties,
                                                                             tab.tabs_width, y - half_tab_distance,
                                                                             tab, tab.tab_dog_bone)
            right_tab_to_add, right_tab_dog_bone = tab_join_create_tab_on_face(tab_part.properties,
                                                                               part_interactor.properties,
                                                                               tab.tabs_width, y + half_tab_distance,
                                                                               tab, tab.tab_dog_bone)

            right_intersect_test, right_tab_to_add_transformed = helper.check_intersect(right_tab_to_add, tab,
                                                                                 part_interactor.properties)
            left_intersect_test, left_tab_to_add_transformed = helper.check_intersect(left_tab_to_add, tab,
                                                                               part_interactor.properties)

            if right_intersect_test or left_intersect_test:
                tab_part.toAdd.append(left_tab_to_add_transformed)
                tab_part.toAdd.append(right_tab_to_add_transformed)
                if left_tab_dog_bone:
                    tab_part.toRemove.append(helper.transform_part(left_tab_dog_bone, tab))
                if right_tab_dog_bone:
                    tab_part.toRemove.append(helper.transform_part(right_tab_dog_bone, tab))

                left_hole = helper.tab_join_create_hole_on_plane(tab, tab.tabs_width, y - half_tab_distance,
                                                                 tab_part.properties, part_interactor.properties,
                                                                 tab.dog_bone)
                right_hole = helper.tab_join_create_hole_on_plane(tab, tab.tabs_width, y + half_tab_distance,
                                                                  tab_part.properties, part_interactor.properties,
                                                                  tab.dog_bone)

                left_hole_transformed = helper.transform_part(left_hole, tab)
                right_hole_transformed = helper.transform_part(right_hole, tab)
                part_interactor.toRemove.append(left_hole_transformed)
                part_interactor.toRemove.append(right_hole_transformed)
                if join_context:
                    join_context.register_screw_clearance(tab, part_interactor,
                                                          left_hole_transformed)
                    join_context.register_screw_clearance(tab, part_interactor,
                                                          right_hole_transformed)

                yield y, part_interactor
                break


def make_tslot_tab_join(tab, tab_part, other_parts, join_context=None):
    half_tab_distance = (tab.screw_diameter * tab.half_tab_ratio) + tab.tabs_width / 2.0
    screw_nut_spec = helper.ObjectProperties(screw_diameter=tab.screw_diameter,
                                              screw_length=tab.screw_length)
    for y, part_interactor in create_tab_pairs_with_holes(tab, tab_part, other_parts,
                                                           half_tab_distance, join_context):
        screw_way_hole_face = screw_way_on_face(tab_part.properties, part_interactor.properties,
                                                screw_nut_spec, tab, y, tab.dog_bone)
        screw_way_hole_plane = screw_way_on_plane(part_interactor.properties, screw_nut_spec, y)

        tab_part.toRemove.append(helper.transform_part(screw_way_hole_face, tab))
        screw_way_hole_plane_transformed = helper.transform_part(screw_way_hole_plane, tab)
        part_interactor.toRemove.append(screw_way_hole_plane_transformed)
        if join_context:
            join_context.register_screw_clearance(tab, part_interactor,
                                                  screw_way_hole_plane_transformed)
    return


def make_wood_screw_tab_join(tab, tab_part, other_parts):
    # Only the tabs and a round hole for the screw shaft, no pocket for a nut/washer.
    half_tab_distance = (tab.screw_diameter * tab.half_tab_ratio) + tab.tabs_width / 2.0
    for y, part_interactor in create_tab_pairs_with_holes(tab, tab_part, other_parts, half_tab_distance):
        screw_way_hole_plane = screw_way_on_plane(part_interactor.properties, tab, y)
        part_interactor.toRemove.append(helper.transform_part(screw_way_hole_plane, tab))
    return


def make_screw_in_nut_join(tab, tab_part, other_parts):
    half_tab_distance = (tab.screw_diameter * tab.half_tab_ratio) + tab.tabs_width / 2.0
    screw_spec = helper.ObjectProperties(screw_diameter=tab.screw_diameter,
                                         screw_length=tab.screw_length)
    for y, part_interactor in create_tab_pairs_with_holes(tab, tab_part, other_parts, half_tab_distance):
        # The head side uses the same pocket geometry as a normal Screw connection.
        head_tab = helper.ObjectProperties(**tab.__dict__)
        head_tab.thread_clearance = 0.0
        head_tab.screw_length_tol = 0.0
        head_tab.nut_slot_overhang = 0.0
        head_pocket = screw_way_on_face(tab_part.properties, part_interactor.properties,
                                        screw_spec, head_tab, y, tab.dog_bone)
        tab_part.toRemove.append(helper.transform_part(head_pocket, tab))

        insert_radius = (tab.nut_outer_diameter - part_interactor.properties.laser_beam_diameter) / 2.0
        insert_depth = tab.nut_depth + tab.thread_clearance
        insert_hole = Part.makeCylinder(insert_radius, insert_depth,
                                        FreeCAD.Vector(0,
                                                       y, 0),
                                        FreeCAD.Vector(1, 0, 0))
        part_interactor.toRemove.append(helper.transform_part(insert_hole, tab))

        if tab.use_nut_flange_pocket:
            flange_radius = (tab.nut_flange_diameter
                             - part_interactor.properties.laser_beam_diameter) / 2.0
            if flange_radius <= insert_radius or tab.nut_flange_depth <= 0.0:
                raise ValueError("ScrewInNut flange pocket must be wider than the insert pocket and positive")
            flange_hole = Part.makeCylinder(flange_radius, tab.nut_flange_depth,
                                            FreeCAD.Vector(0, y, 0),
                                            FreeCAD.Vector(1, 0, 0))
            part_interactor.toRemove.append(helper.transform_part(flange_hole, tab))
    return


def make_tabs_joins(parts, tabs):
    parts_element = []
    for part in parts:
        mat_element = helper.MaterialElement(part)
        parts_element.append(mat_element)

    join_context = JoinContext()
    removeParts = {}
    #test to improve speed
    for tab in tabs:
        keyid = str(tab.group_id)
        if keyid not in removeParts:
            removeParts[keyid] = []
        removeParts[keyid].append(tab.freecad_object.Name)

    for tab in tabs:
        tab_part = None
        other_parts = []
        keyid = str(tab.group_id)
        for part in parts_element:
            if part.get_name() == tab.freecad_object.Name:
                tab_part = part
#            else:
            elif part.get_name() not in removeParts[keyid]:
                other_parts.append(part)
        if tab.tab_type == TabProperties.TYPE_TAB:
            make_tab_join(tab, tab_part, other_parts)
        elif tab.tab_type == TabProperties.TYPE_T_SLOT:
            make_tslot_tab_join(tab, tab_part, other_parts, join_context)
        elif tab.tab_type == TabProperties.TYPE_CONTINUOUS:
            make_continuous_tab_joins(tab, tab_part, other_parts)
        elif tab.tab_type == TabProperties.TYPE_FLEX:
            flextab.make_flex_tab_join(tab, tab_part, other_parts)
        elif tab.tab_type == TabProperties.TYPE_WOOD_SCREW:
            make_wood_screw_tab_join(tab, tab_part, other_parts)
        elif tab.tab_type == TabProperties.TYPE_SCREW_IN_NUT:
            make_screw_in_nut_join(tab, tab_part, other_parts)
        elif tab.tab_type == TabProperties.TYPE_TONGUE_GROOVE:
            make_tongue_groove_join(tab, tab_part, other_parts, join_context)
        else:
            raise ValueError("Unknown tab type")
    join_context.apply_screw_clearances_to_tongues()
    return parts_element