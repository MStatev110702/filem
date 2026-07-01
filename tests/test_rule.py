import unittest
from pathlib import Path
import tempfile
from src.rules.file_rules import AllFiles, IncludeTypes, ExcludeTypes

class TestRule(unittest.TestCase):
    def test_all_files_is_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")

            rule = AllFiles()
            self.assertTrue(rule.match(test_file))

    def test_all_files_is_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp)

            rule = AllFiles()
            self.assertFalse(rule.match(test_file))

    def test_include_types_in_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            include_types = [".txt", ".sh"]

            rule = IncludeTypes(include_types)
            self.assertTrue(rule.match(test_file))

    def test_include_types_not_in_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            include_types = [".php", ".sh"]

            rule = IncludeTypes(include_types)
            self.assertFalse(rule.match(test_file))
    
    def test_include_types_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp)
            include_types = [".txt", ".sh"]

            rule = IncludeTypes(include_types)
            self.assertFalse(rule.match(test_file))

    def test_include_types_no_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "README"
            test_file.write_text("Hello")
            include_types = [".txt", ".sh", ""]

            rule = IncludeTypes(include_types)
            self.assertTrue(rule.match(test_file))

    def test_include_types_hidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / ".hidden.txt"
            test_file.write_text("Hello")
            include_types = [".txt", ".sh", ""]

            rule = IncludeTypes(include_types)
            self.assertTrue(rule.match(test_file))

    def test_include_types_no_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            include_types = []

            rule = IncludeTypes(include_types)
            self.assertFalse(rule.match(test_file))

    def test_include_types_diffrent_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "TeSt.tXt"
            test_file.write_text("Hello")
            include_types = [".TXT", ".sh", ""]

            rule = IncludeTypes(include_types)
            self.assertTrue(rule.match(test_file))

    def test_exclude_types_in_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            include_types = [".txt", ".sh"]

            rule = ExcludeTypes(include_types)
            self.assertFalse(rule.match(test_file))

    def test_exclude_types_not_in_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.c"
            test_file.write_text("Hello")
            include_types = [".php", ".sh"]

            rule = ExcludeTypes(include_types)
            self.assertTrue(rule.match(test_file))
    
    def test_exclude_types_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp)
            include_types = [".txt", ".sh"]

            rule = ExcludeTypes(include_types)
            self.assertFalse(rule.match(test_file))

    def test_exclude_types_no_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "README"
            test_file.write_text("Hello")
            include_types = [".txt", ".sh", ""]

            rule = ExcludeTypes(include_types)
            self.assertFalse(rule.match(test_file))

    def test_exclude_types_hidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / ".hidden.txt"
            test_file.write_text("Hello")
            include_types = [".txt", ".sh", ""]

            rule = ExcludeTypes(include_types)
            self.assertFalse(rule.match(test_file))

    def test_exclude_types_no_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            include_types = []

            rule = ExcludeTypes(include_types)
            self.assertTrue(rule.match(test_file))

    def test_exclude_types_hidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "TesT.TxT"
            test_file.write_text("Hello")
            include_types = [".tXT", ".sh", ""]

            rule = ExcludeTypes(include_types)
            self.assertFalse(rule.match(test_file))

if __name__ == "__main__":
    unittest.main()