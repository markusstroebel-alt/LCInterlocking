import unittest

from lasercut.holetemplate import cut_target_shape, cut_targets, validate_roles


class FakeShape:
    def __init__(self, name, volume=1.0, intersections=None):
        self.name = name
        self.Volume = volume
        self.intersections = intersections or {}
        self.cut_by = None

    def isNull(self):
        return False

    def common(self, other):
        return self.intersections.get(other.name, NullShape())

    def fuse(self, other):
        return FakeShape("%s+%s" % (self.name, other.name), self.Volume + other.Volume)

    def removeSplitter(self):
        return self

    def cut(self, other):
        result = FakeShape("%s-%s" % (self.name, other.name), self.Volume)
        result.cut_by = other.name
        return result

    def copy(self):
        return FakeShape(self.name, self.Volume, self.intersections)


class NullShape(FakeShape):
    def __init__(self):
        super(NullShape, self).__init__("null", 0.0)

    def isNull(self):
        return True


class FakeObject:
    def __init__(self, name, shape):
        self.Name = name
        self.Label = name
        self.Shape = shape


class HoleTemplateTests(unittest.TestCase):
    def test_cut_target_uses_all_intersecting_templates(self):
        first_template = FakeObject("Screw", FakeShape("screw"))
        second_template = FakeObject("Hinge", FakeShape("hinge"))
        target = FakeObject("Plate", FakeShape(
            "plate", intersections={
                "screw": FakeShape("screw_intersection", 1.0),
                "hinge": FakeShape("hinge_intersection", 2.0),
            }))

        shape, changed = cut_target_shape(target, [first_template, second_template])

        self.assertTrue(changed)
        self.assertEqual("plate-screw_intersection+hinge_intersection", shape.name)

    def test_non_intersecting_template_keeps_target_out_of_results(self):
        template = FakeObject("Screw", FakeShape("screw"))
        target = FakeObject("Plate", FakeShape("plate"))

        self.assertEqual([], cut_targets([template], [target]))

    def test_same_body_cannot_have_both_roles(self):
        body = FakeObject("Body", FakeShape("body"))

        with self.assertRaisesRegex(ValueError, "both template and target"):
            validate_roles([body], [body])


if __name__ == '__main__':
    unittest.main()