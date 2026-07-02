import unittest
from pathlib import Path
import tempfile
from src.rules.file_rules import AllFiles, IncludeTypes, ExcludeTypes
from src.rules.dir_rules import AllDirs, EmptyDirs, FilledDirs
from src.rules.factory import RuleFactory
from src.entry import Entry

class TestRule(unittest.TestCase):
    #--- file rules test ---
    #--- all files ---
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

    #--- include types ---
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

    #--- exclude types ---
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

    #--- dir rules ---
    #--- all dirs ---
    def test_all_dirs_is_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp)

            rule = AllDirs()
            self.assertTrue(rule.match(test_dir))

    def test_all_dirs_is_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test.txt"
            test_dir.write_text("test")

            rule = AllDirs()
            self.assertFalse(rule.match(test_dir))

    #--- empty dirs ---
    def test_empty_dirs_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp)

            rule = EmptyDirs()
            self.assertTrue(rule.match(test_dir))

    def test_empty_dirs_is_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test.txt"
            test_dir.write_text("test")

            rule = EmptyDirs()
            self.assertFalse(rule.match(test_dir))

    def test_empty_dirs_filled(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp)
            (test_dir / "test.txt").write_text("test")

            rule = EmptyDirs()
            self.assertFalse(rule.match(test_dir))

    #--- filled dirs
    def test_filled_dirs_filled(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp)
            (test_dir / "test.txt").write_text("test")

            rule = FilledDirs()
            self.assertTrue(rule.match(test_dir))

    def test_filled_dirs_is_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test.txt"
            test_dir.write_text("test")

            rule = FilledDirs()
            self.assertFalse(rule.match(test_dir))

    def test_filled_dirs_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp)

            rule = FilledDirs()
            self.assertFalse(rule.match(test_dir))


    #--- factory ---
    def test_rule_factory_no_dir_rule(self):
        entry = Entry(
            id=1,
            name="test",
            description="test",
            type="COPY",
            interval_type="newest",
            schedule_type="",
            schedule_value=0,
            originpath="/tmp",
            destpath="/tmp2",
            include_dir="none",
            include_files="selected types"
        )
        file_types = [".txt", ".pdf"]
        rule = RuleFactory().create(entry, file_types)

        self.assertIsNone(rule.dir_rule)
        self.assertIsInstance(rule.file_rule, IncludeTypes)

    def test_rule_factory_no_file_rule(self):
        entry = Entry(
            id=1,
            name="test",
            description="test",
            type="COPY",
            interval_type="newest",
            schedule_type="",
            schedule_value=0,
            originpath="/tmp",
            destpath="/tmp2",
            include_dir="all",
            include_files="none"
        )
        rule = RuleFactory().create(entry, [])

        self.assertIsNone(rule.file_rule)
        self.assertIsInstance(rule.dir_rule, AllDirs)

    def test_rule_factory_both(self):
        entry = Entry(
            id=1,
            name="test",
            description="test",
            type="COPY",
            interval_type="newest",
            schedule_type="",
            schedule_value=0,
            originpath="/tmp",
            destpath="/tmp2",
            include_dir="empty",
            include_files="exclude types"
        )
        file_types = [".txt", ".pdf"]
        rule = RuleFactory().create(entry, file_types)

        self.assertIsInstance(rule.dir_rule, EmptyDirs)
        self.assertIsInstance(rule.file_rule, ExcludeTypes)

    def test_rule_factory_both_none(self):
        entry = Entry(
            id=1,
            name="test",
            description="test",
            type="COPY",
            interval_type="newest",
            schedule_type="",
            schedule_value=0,
            originpath="/tmp",
            destpath="/tmp2",
            include_dir="none",
            include_files="none"
        )
        file_types = [".txt", ".pdf"]
        rule = RuleFactory().create(entry, file_types)

        self.assertIsNone(rule.dir_rule)
        self.assertIsNone(rule.file_rule)

if __name__ == "__main__":
    unittest.main()