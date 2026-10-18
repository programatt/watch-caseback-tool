from pathlib import Path
import tempfile
import unittest

from caseback_tool.geometry import DiskSpec, HandleSpec, disk_scad, handle_scad


class DiskTests(unittest.TestCase):
    def test_default_disk_diameter_covers_teeth(self):
        spec = DiskSpec(31.0, 6, 1.2, 1.6, 2.4)
        self.assertEqual(spec.resolved_disk_diameter, 34.6)
        spec.validate()

    def test_disk_source_contains_requested_count(self):
        source = disk_scad(DiskSpec(31.0, 6, 1.2, 1.6, 2.4))
        self.assertIn("360/6", source)
        self.assertIn("caseback_disk();", source)

    def test_rejects_overlapping_teeth(self):
        with self.assertRaises(ValueError):
            DiskSpec(10.0, 12, 1.0, 1.0, 5.0).validate()


class HandleTests(unittest.TestCase):
    def test_handle_source_has_locking_features(self):
        source = handle_scad(HandleSpec())
        self.assertIn("Female hex socket", source)
        self.assertIn("M4 retaining screw", source)
        self.assertIn("caseback_handle();", source)


if __name__ == "__main__":
    unittest.main()

