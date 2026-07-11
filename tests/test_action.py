import unittest
import tempfile
import random
import string
from pathlib import Path
from base_test import BaseTest
from src.action.file_actions import CopyFile, MoveFile, DeleteFile
from src.action.dir_actions import CopyDir, MoveDir, DeleteDir
from src.action.action_factory import FileActionFactory, DirActionFactory

class TestAction(BaseTest):
    #--- factory tests---
    def test_action_factory_copy_file(self):
       with tempfile.TemporaryDirectory() as tmp:
            dest_dir = Path(tmp) / "destination"

            test_entry = self.create_test_entry(
                type="COPY",
                destpath=str(dest_dir)
            )

            action = FileActionFactory().create(test_entry)
            self.assertIsInstance(action, CopyFile) 

    def test_action_factory_move_file(self):
       with tempfile.TemporaryDirectory() as tmp:
            dest_dir = Path(tmp) / "destination"

            test_entry = self.create_test_entry(
                type="MOVE",
                destpath=str(dest_dir)
            )

            action = FileActionFactory().create(test_entry)
            self.assertIsInstance(action, MoveFile)

    def test_action_factory_delete_file(self):
       with tempfile.TemporaryDirectory() as tmp:
            test_entry = self.create_test_entry(
                type="DELETE"
            )

            action = FileActionFactory().create(test_entry)
            self.assertIsInstance(action, DeleteFile)

    def test_action_factory_file_unknown_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_entry = self.create_test_entry(
                type="WHAT_IS_THIS",
            )

            with self.assertRaises(ValueError):
                FileActionFactory().create(test_entry)

    def test_action_factory_copy_dir(self):
       with tempfile.TemporaryDirectory() as tmp:
            dest_dir = Path(tmp) / "destination"

            test_entry = self.create_test_entry(
                type="COPY",
                destpath=str(dest_dir)
            )

            action = DirActionFactory().create(test_entry)
            self.assertIsInstance(action, CopyDir) 

    def test_action_factory_move_dir(self):
       with tempfile.TemporaryDirectory() as tmp:
            dest_dir = Path(tmp) / "destination"

            test_entry = self.create_test_entry(
                type="MOVE",
                destpath=str(dest_dir)
            )

            action = DirActionFactory().create(test_entry)
            self.assertIsInstance(action, MoveDir)

    def test_action_factory_delete_dir(self):
       with tempfile.TemporaryDirectory() as tmp:
            test_entry = self.create_test_entry(
                type="DELETE"
            )

            action = DirActionFactory().create(test_entry)
            self.assertIsInstance(action, DeleteDir)

    def test_action_factory_dir_unknown_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_entry = self.create_test_entry(
                type="WHAT_IS_THIS",
            )

            with self.assertRaises(ValueError):
                DirActionFactory().create(test_entry)

    #--- file actions ---
    #--- copy file action ---
    def test_copy_file_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            CopyFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_copy_file_dest_not_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"

            CopyFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_copy_file_auto_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()
            existsing_file = dest_dir / "test.txt"
            existsing_file.write_text("test123")         

            CopyFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test (1).txt"

            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())
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

            CopyFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test (3).txt"

            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_copy_file_deep_nest(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_src_dir = Path(tmp) / "a" / "b" / "c"
            test_src_dir.mkdir(parents=True, exist_ok=True)
            test_file = test_src_dir / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            CopyFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_copy_file_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            CopyFile(dest_dir).execute(test_file)

            dest_file = dest_dir / "test.txt"

            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "")

    def test_copy_file_byte_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_bytes(b"\x00\x01\x02")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            CopyFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "\x00\x01\x02")

    def test_copy_file_large_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            large_string = ''.join(random.choice(string.ascii_lowercase) for i in range(10**7))
            test_file.write_text(large_string)
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            CopyFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), large_string)      
    
    #--- move file action ---
    def test_move_file_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            MoveFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_move_file_dest_not_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"

            MoveFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_move_file_auto_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()
            existsing_file = dest_dir / "test.txt"
            existsing_file.write_text("test123")         

            MoveFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test (1).txt"
            
            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())
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

            MoveFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test (3).txt"
            
            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_move_file_deep_nest(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_src_dir = Path(tmp) / "a" / "b" / "c"
            test_src_dir.mkdir(parents=True, exist_ok=True)
            test_file = test_src_dir / "test.txt"
            test_file.write_text("Hello")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            MoveFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "Hello")

    def test_move_file_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            MoveFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "")

    def test_move_file_byte_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_bytes(b"\x00\x01\x02")
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            MoveFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), "\x00\x01\x02")

    def test_move_file_large_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            large_string = ''.join(random.choice(string.ascii_lowercase) for i in range(10**7))
            test_file.write_text(large_string)
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()      

            MoveFile(dest_dir).execute(test_file)
            
            dest_file = dest_dir / "test.txt"

            self.assertTrue(not test_file.exists())
            self.assertTrue(dest_file.exists())
            self.assertEqual(dest_file.read_text().rstrip(), large_string)

    #--- delete file action ---
    def test_delete_file_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / "test.txt"
            test_file.write_text("test123")    

            DeleteFile().execute(test_file)
            
            self.assertTrue(not test_file.exists())

    #--- dir actions ---
    #--- copy dir action ---
    def test_copy_dir_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            CopyDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test"

            self.assertTrue(dest_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_copy_dir_dest_not_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"

            CopyDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test"

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

            CopyDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test (1)"

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

            CopyDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test (3)"

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

            CopyDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test"

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

            CopyDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test"

            self.assertTrue(test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

            expected = {"test1.txt", "test2.txt", "test3.txt", "test4.txt"}
            actual = {p.name for p in new_dest_dir.iterdir()}

            self.assertEqual(actual, expected)
    
    #--- move dir action ---
    def test_move_dir_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"
            dest_dir.mkdir()

            MoveDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test"

            self.assertTrue(not test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

    def test_move_dir_dest_not_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()
            dest_dir = Path(tmp) / "destination"

            MoveDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test"

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

            MoveDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test (1)"

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

            MoveDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test (3)"

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

            MoveDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test"

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

            MoveDir(dest_dir).execute(test_dir)
            
            new_dest_dir = dest_dir / "test"
            
            self.assertTrue(not test_dir.exists())
            self.assertTrue(new_dest_dir.exists())

            
            expected = {"test1.txt", "test2.txt", "test3.txt", "test4.txt"}
            actual = {p.name for p in new_dest_dir.iterdir()}

            self.assertEqual(actual, expected)
    
    #--- delete dir action ---
    def test_delete_dir_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test"
            test_dir.mkdir()

            DeleteDir().execute(test_dir)
            
            self.assertTrue(not test_dir.exists())


if __name__ == "__main__":
    unittest.main()