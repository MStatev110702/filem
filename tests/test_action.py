import unittest
import tempfile
import random
import string
from pathlib import Path
from src.entry import Entry
from src.action.file_actions import CopyFile, MoveFile, DeleteFile
from src.action.dir_actions import CopyDir, MoveDir, DeleteDir
from src.action.action_factory import ActionFactory

class TestAction(unittest.TestCase):
    #--- factory errors ---
    def test_action_factory_dest_empty_spaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(Path(tmp)),
                destpath="   ",
                include_dir="none",
                include_files="none"
            )

            with self.assertRaises(ValueError):
                ActionFactory().create(test_entry, test_file)

    def test_action_factory_dest_path_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath="",
                include_dir="none",
                include_files="none"
            )

            with self.assertRaises(ValueError):
                ActionFactory().create(test_entry, test_file)
 
    def test_action_factory_src_path_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest_dir = Path(tmp) / "destination"

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath="",
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            with self.assertRaises(ValueError):
                ActionFactory().create(test_entry, Path(""))

    def test_action_factoyr_src_path_not_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest_dir = Path(tmp) / "destination"

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(Path(tmp)),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            with self.assertRaises(FileExistsError):
                ActionFactory().create(test_entry, (Path(tmp) / "test.txt"))

    def test_action_factory_file_unknown_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="WHAT_IS_THIS",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            with self.assertRaises(ValueError):
                ActionFactory().create(test_entry, test_file)

    def test_action_factory_dir_unknown_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="WHAT_IS_THIS",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            with self.assertRaises(ValueError):
                ActionFactory().create(test_entry, test_dir)

    #--- file actions ---
    #--- copy file action ---
    def test_copy_file_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, CopyFile)
            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())
            
            if dest_file.exists:
                self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_copy_file_dest_not_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, CopyFile)
            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())
            

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_copy_file_auto_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()
            existsing_file = dest_dir / "test.txt"
            existsing_file.write_text("test123")         

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test (1).txt"
            self.assertIsInstance(action, CopyFile)
            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_copy_file_auto_rename_multiple(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()
            existsing_file = dest_dir / "test.txt"
            existsing_file.write_text("test123")     
            existsing_file_1 = dest_dir / "test (1).txt"
            existsing_file_1.write_text("test123")     
            existsing_file_2 = dest_dir / "test (2).txt"
            existsing_file_2.write_text("test123")         

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test (3).txt"
            self.assertIsInstance(action, CopyFile)
            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_copy_file_deep_nest(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_src_dir = Path(tmp) / "a" / "b" / "c"
            test_src_dir.mkdir(parents=True, exist_ok=True)
            test_file = test_src_dir / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(test_src_dir),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, CopyFile)
            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_copy_file_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(Path(tmp)),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, CopyFile)
            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "")

    def test_copy_file_byte_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_bytes(b"\x00\x01\x02")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(Path(tmp)),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, CopyFile)
            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "\x00\x01\x02")

    def test_copy_file_large_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            large_string = ''.join(random.choice(string.ascii_lowercase) for i in range(10**7))
            test_file.write_text(large_string)
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(Path(tmp)),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, CopyFile)
            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), large_string)      
    
    #--- move file action ---
    def test_move_file_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, MoveFile)
            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())
            
            if dest_file.exists:
                self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_move_file_dest_not_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, MoveFile)
            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_move_file_auto_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()
            existsing_file = dest_dir / "test.txt"
            existsing_file.write_text("test123")         

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test (1).txt"
            self.assertIsInstance(action, MoveFile)
            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_move_file_auto_rename_multiple(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()
            existsing_file = dest_dir / "test.txt"
            existsing_file.write_text("test123")     
            existsing_file_1 = dest_dir / "test (1).txt"
            existsing_file_1.write_text("test123")     
            existsing_file_2 = dest_dir / "test (2).txt"
            existsing_file_2.write_text("test123")         

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test (3).txt"
            self.assertIsInstance(action, MoveFile)
            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_move_file_deep_nest(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_src_dir = Path(tmp) / "a" / "b" / "c"
            test_src_dir.mkdir(parents=True, exist_ok=True)
            test_file = test_src_dir / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(test_src_dir),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, MoveFile)
            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_move_file_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(Path(tmp)),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, MoveFile)
            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "")

    def test_move_file_byte_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_bytes(b"\x00\x01\x02")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(Path(tmp)),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, MoveFile)
            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), "\x00\x01\x02")

    def test_move_file_large_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            large_string = ''.join(random.choice(string.ascii_lowercase) for i in range(10**7))
            test_file.write_text(large_string)
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(Path(tmp)),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            dest_file = dest_dir / "test.txt"
            self.assertIsInstance(action, MoveFile)
            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())

            if dest_file.exists():
                self.assertEqual(dest_file.read_text().rstrip(), large_string)

    #--- delete file action ---
    def test_delete_file_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("test123")    

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="DELETE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(Path(tmp)),
                destpath="",
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_file)
            action.execute()
            
            self.assertIsInstance(action, DeleteFile)
            self.assertTrue(not test_file.exists())

    #--- dir actions ---
    #--- copy dir action ---
    def test_copy_dir_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test"
            self.assertIsInstance(action, CopyDir)
            self.assertTrue(dest_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_copy_dir_dest_not_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test"
            self.assertIsInstance(action, CopyDir)
            self.assertTrue(test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_copy_dir_auto_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()
            existsing_dir = dest_dir / "test"
            existsing_dir.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test (1)"
            self.assertIsInstance(action, CopyDir)
            self.assertTrue(test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_copy_dir_auto_rename_multiple(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()
            existsing_dir = dest_dir / "test"
            existsing_dir.mkdir()
            existsing_dir_1 = dest_dir / "test (1)"
            existsing_dir_1.mkdir()
            existsing_dir_2 = dest_dir / "test (2)"
            existsing_dir_2.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test (3)"
            self.assertIsInstance(action, CopyDir)
            self.assertTrue(test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_copy_dir_deep_nest(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_src_dir = Path(tmp) / "a" / "b" / "c"
            test_src_dir.mkdir(parents=True, exist_ok=True)
            test_dir = test_src_dir / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(test_src_dir),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test"
            self.assertIsInstance(action, CopyDir)
            self.assertTrue(test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_copy_dir_filled_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            test_file_1 = test_dir / "test1.txt"
            test_file_1.write_text("Test1")
            test_file_2 = test_dir / "test2.txt"
            test_file_2.write_text("Test2") 
            test_file_3 = test_dir / "test3.txt"
            test_file_3.write_text("Test3")
            test_file_4 = test_dir / "test4.txt"
            test_file_4.write_text("Test4")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="COPY",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(test_dir),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test"
            self.assertIsInstance(action, CopyDir)
            self.assertTrue(test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

            if new_dest_dir.exists():
                self.assertTrue((new_dest_dir / "test1.txt").exists())
                self.assertTrue((new_dest_dir / "test2.txt").exists())
                self.assertTrue((new_dest_dir / "test3.txt").exists())
                self.assertTrue((new_dest_dir / "test4.txt").exists())
    
    #--- move dir action ---
    def test_move_dir_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test"
            self.assertIsInstance(action, MoveDir)
            self.assertTrue(not test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_move_dir_dest_not_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test"
            self.assertIsInstance(action, MoveDir)
            self.assertTrue(not test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_move_dir_auto_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()
            existsing_dir = dest_dir / "test"
            existsing_dir.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test (1)"
            self.assertIsInstance(action, MoveDir)
            self.assertTrue(not test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_move_dir_auto_rename_multiple(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()
            existsing_dir = dest_dir / "test"
            existsing_dir.mkdir()
            existsing_dir_1 = dest_dir / "test (1)"
            existsing_dir_1.mkdir()
            existsing_dir_2 = dest_dir / "test (2)"
            existsing_dir_2.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(tmp),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test (3)"
            self.assertIsInstance(action, MoveDir)
            self.assertTrue(not test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_move_dir_deep_nest(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_src_dir = Path(tmp) / "a" / "b" / "c"
            test_src_dir.mkdir(parents=True, exist_ok=True)
            test_dir = test_src_dir / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(test_src_dir),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test"
            self.assertIsInstance(action, MoveDir)
            self.assertTrue(not test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_move_dir_filled_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            test_file_1 = test_dir / "test1.txt"
            test_file_1.write_text("Test1")
            test_file_2 = test_dir / "test2.txt"
            test_file_2.write_text("Test2") 
            test_file_3 = test_dir / "test3.txt"
            test_file_3.write_text("Test3")
            test_file_4 = test_dir / "test4.txt"
            test_file_4.write_text("Test4")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="MOVE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(test_dir),
                destpath=str(dest_dir),
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            new_dest_dir = dest_dir / "test"
            self.assertIsInstance(action, MoveDir)
            self.assertTrue(not test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

            if new_dest_dir.exists():
                self.assertTrue((new_dest_dir / "test1.txt").exists())
                self.assertTrue((new_dest_dir / "test2.txt").exists())
                self.assertTrue((new_dest_dir / "test3.txt").exists())
                self.assertTrue((new_dest_dir / "test4.txt").exists())
    
    #--- delete dir action ---
    def test_delete_dir_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()

            test_entry = Entry(
                id=1,
                name="test",
                description="test",
                type="DELETE",
                interval_type="newest",
                schedule_type="",
                schedule_value=0,
                originpath=str(Path(tmp)),
                destpath="",
                include_dir="none",
                include_files="none"
            )

            action = ActionFactory().create(test_entry, test_dir)
            action.execute()
            
            self.assertIsInstance(action, DeleteDir)
            self.assertTrue(not test_dir.exists())


if __name__ == "__main__":
    unittest.main()