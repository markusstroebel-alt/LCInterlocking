#!/usr/bin/env python

"""Geometry helpers for creating holes from connection template bodies."""


def _object_name(obj):
    return getattr(obj, 'Label', None) or getattr(obj, 'Name', None) or str(obj)


def _shape_for(obj):
    shape = getattr(obj, 'Shape', None)
    if shape is None:
        raise ValueError("%s has no Shape" % _object_name(obj))
    if shape.isNull():
        raise ValueError("%s has an empty Shape" % _object_name(obj))
    return shape


def validate_roles(template_objects, target_objects):
    """Validate the two explicit roles used by a hole-template operation."""
    if not template_objects:
        raise ValueError("Select at least one template body")
    if not target_objects:
        raise ValueError("Select at least one target body")

    template_ids = {id(obj) for obj in template_objects}
    target_ids = {id(obj) for obj in target_objects}
    if template_ids.intersection(target_ids):
        raise ValueError("A body cannot be both template and target")

    for obj in template_objects + target_objects:
        _shape_for(obj)


def intersecting_template_shape(target_shape, template_shapes):
    """Return the union of template volumes that actually intersect a target."""
    intersections = []
    for template_shape in template_shapes:
        if template_shape.isNull():
            continue
        intersection = target_shape.common(template_shape)
        if not intersection.isNull() and intersection.Volume > 0.0:
            intersections.append(intersection)

    if not intersections:
        return None

    cutter = intersections[0]
    for intersection in intersections[1:]:
        cutter = cutter.fuse(intersection)
    return cutter.removeSplitter()


def cut_target_shape(target_object, template_objects):
    """Cut all intersecting template volumes from one target object.

    Returns ``(shape, changed)``. The unchanged original shape is returned when
    none of the templates overlaps the target.
    """
    target_shape = _shape_for(target_object)
    template_shapes = [_shape_for(obj) for obj in template_objects]
    cutter = intersecting_template_shape(target_shape, template_shapes)
    if cutter is None:
        return target_shape.copy(), False
    return target_shape.cut(cutter).removeSplitter(), True


def cut_targets(template_objects, target_objects):
    """Return generated shapes for every target that intersects a template."""
    validate_roles(template_objects, target_objects)
    generated = []
    for target_object in target_objects:
        shape, changed = cut_target_shape(target_object, template_objects)
        if changed:
            generated.append((target_object, shape))
    return generated