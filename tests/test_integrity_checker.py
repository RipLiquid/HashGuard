import hashlib
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

from src.integrity_checker import (
    calculate_hash,
    check_integrity,
    load_baseline,
    save_baseline,
    scan_directory,
)


class TestHashGuard(unittest.TestCase):

    def test_calculate_hash(self):
        with tempfile.NamedTemporaryFile(delete=False) as file:
            file.write(b"hello")
            file_path = file.name

        try:
            result = calculate_hash(file_path)

            expected = (
                "2cf24dba5fb0a30e26e83b2ac5b9e29e"
                "1b161e5c1fa7425e73043362938b9824"
            )

            self.assertEqual(result, expected)

        finally:
            os.remove(file_path)

    def test_save_and_load_baseline(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            baseline_file = os.path.join(temp_dir, "baseline.json")

            original = {
                "example.txt": "abc123"
            }

            save_baseline(original, baseline_file)

            loaded = load_baseline(baseline_file)

            self.assertEqual(original, loaded)

    def test_scan_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "sample.txt")

            with open(test_file, "w") as file:
                file.write("HashGuard test")

            results = scan_directory(temp_dir)

            self.assertIn(test_file, results)
            self.assertEqual(len(results), 1)

    def test_integrity_detection(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config = os.path.join(temp_dir, "config.txt")
            notes = os.path.join(temp_dir, "notes.txt")
            unchanged = os.path.join(temp_dir, "test.txt")

            with open(config, "w") as file:
                file.write("original config")

            with open(notes, "w") as file:
                file.write("notes")

            with open(unchanged, "w") as file:
                file.write("unchanged")

            baseline_file = os.path.join(temp_dir, "baseline.json")

            baseline = scan_directory(temp_dir)

            # Do not include the baseline itself.
            baseline.pop(baseline_file, None)

            save_baseline(baseline, baseline_file)

            # Modify one file.
            with open(config, "w") as file:
                file.write("modified config")

            # Delete one file.
            os.remove(notes)

            # Add one file.
            new_file = os.path.join(temp_dir, "newfile.txt")

            with open(new_file, "w") as file:
                file.write("new file")

            output = StringIO()

            with redirect_stdout(output):
                check_integrity(temp_dir, baseline_file)

            result = output.getvalue()

            self.assertIn("[MODIFIED] config.txt", result)
            self.assertIn("[NEW] newfile.txt", result)
            self.assertIn("[OK] test.txt", result)
            self.assertIn("[DELETED] notes.txt", result)


if __name__ == "__main__":
    unittest.main()