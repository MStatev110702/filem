import unittest
from unittest.mock import MagicMock
import sqlite3
import uuid
from dataclasses import astuple, replace
from base_test import BaseTest
from src.entry import Entry
from src.database.db import Database
from src.database.queries import *

class TestQueries(BaseTest):
    @classmethod
    def setUp(self):
        self.db_uri = f"file:testdb_{uuid.uuid4().hex}?mode=memory&cache=shared"

        self.anchor_conn = sqlite3.connect(self.db_uri, uri=True)
        self.anchor_db = Database(conn=self.anchor_conn)

        self.test_db = Database(conn=sqlite3.connect(self.db_uri, uri=True))
        self.verify_db = Database(conn=sqlite3.connect(self.db_uri, uri=True))

    @classmethod
    def tearDown(self):
        for db_name in ("test_db", "verify_db", "anchor_db"):
            db = getattr(self, db_name, None)
            if db is not None:
                try:
                    db.close()
                except Exception:
                    pass

    def get_entry_by_id(self, id: int):
        sql = """
            SELECT id, name, description, type, interval_type, schedule_type, schedule_value, 
                originpath, destpath, include_dir, include_files, state
            FROM ENTRIES
            WHERE id = ?
        """
        self.verify_db.execute(sql, (id,))
        return self.verify_db.fetchone()
    
    def get_file_types_by_id(self, id: int):
        sql = """
            SELECT id, file_type, entry_id
            FROM file_types
            WHERE entry_id = ?
        """
        return self.verify_db.query(sql, (id,))
    
    def get_all_file_types(self):
        sql = """
            SELECT id, file_type, entry_id
            FROM file_types
        """
        return self.verify_db.query(sql)

    def create_sql_entry(self, entry: Entry):
        sql = """
            INSERT INTO entries(
                name, description, type, interval_type, schedule_type, schedule_value,
                originpath, destpath, include_dir, include_files
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.verify_db.execute(sql, (
            entry.name,
            entry.description,
            entry.type,
            entry.interval_type,
            entry.schedule_type,
            entry.schedule_value,
            entry.originpath,
            entry.destpath,
            entry.include_dir,
            entry.include_files,
        ))
        self.verify_db.commit()

    def create_file_type(self, id: int, file_types: list[str]):
        sql = """
            INSERT INTO file_types (entry_id, file_type)
            VALUES (?, ?)
        """
        self.verify_db.executemany(sql, [(id, ft) for ft in file_types])
        self.verify_db.commit()

    def get_entries(self):
        sql = """
            SELECT e.id, e.name, e.description, e.type, e.interval_type, e.schedule_type, e.schedule_value, e.originpath, 
                   e.destpath, e.include_dir, e.include_files, GROUP_CONCAT(ft.file_type, ', ') as file_types, e.state
            FROM entries e
            LEFT JOIN file_types ft ON e.id = ft.entry_id
            GROUP BY e.id 
        """
        return self.verify_db.query(sql)

    def test_db_call_database_error(self):
        mock_db = MagicMock() 
        mock_db.__enter__.return_value = mock_db
        mock_db.__exit__.return_value = None
        mock_db.query.side_effect = sqlite3.DatabaseError()

        result = db_call(get_all_entries, "",mock_db)
        self.assertFalse(result.get("success"))
        self.assertStartsWith(result.get("error"), "Database error:")

    def test_db_call_exception(self):
        mock_db = MagicMock() 
        mock_db.__enter__.return_value = mock_db
        mock_db.__exit__.return_value = None
        mock_db.query.side_effect = Exception()

        result = db_call(get_all_entries, "",mock_db)
        self.assertFalse(result.get("success"))
        self.assertStartsWith(result.get("error"), "Unexpected error:")

    def test_get_db_with_db(self):
        self.assertEqual(get_db(self.test_db), self.test_db)

    def test_get_db_with_none(self):
        self.assertIsInstance(get_db(None), Database)

    def test_create_entry_valid_entry(self):
        test_entry = self.create_test_entry()
        result = db_call(create_entry, test_entry, self.test_db)
        
        self.assertTrue(result.get("success"))
        self.assertEqual(result.get("data"), 1)
        
        actual = self.get_entry_by_id(result.get("data"))
        expected = astuple(
            replace(test_entry, id=result.get("data"))
        )
        expected += (0,)

        self.assertEqual(tuple(actual), expected)

    def test_create_entry_invalid_entry(self):
        test_entry = self.create_test_entry(name=None)
        result = db_call(create_entry, test_entry, self.test_db)
        
        self.assertFalse(result.get("success"))
        self.assertStartsWith(result.get("error"), "Database error:") 

    def test_create_file_types_valid_input(self):
        result = db_call(create_file_types, 1, [".txt", ".php"], self.test_db)

        self.assertTrue(result.get("success"))

        actual = self.get_file_types_by_id(1)

        self.assertEqual(len(actual), 2)

    def test_create_file_no_id(self):
        result = db_call(create_file_types, None, [".txt", ".php"], self.test_db)

        self.assertFalse(result.get("success"))
        self.assertStartsWith(result.get("error"), "Database error:")

    def test_create_file_empyt_list(self):
        result = db_call(create_file_types, 1, [], self.test_db)

        self.assertTrue(result.get("success"))

        actual = self.get_file_types_by_id(1)

        self.assertEqual(len(actual), 0)

    def test_get_all_entries_no_file_types(self):
        n = 6
        for i in range(n):
            test_entry = self.create_test_entry()
            self.create_sql_entry(test_entry)

        result = db_call(get_all_entries, "", self.verify_db)
        
        self.assertTrue(result.get("success"))
        self.assertEqual(len(result.get("data")), n)

        for row in result.get("data"):
            self.assertIsNone(row["file_types"])

    def test_get_all_entries_with_file_types(self):
        n = 3

        for i in range(n):
            test_entry = self.create_test_entry()
            self.create_sql_entry(test_entry)
            self.create_file_type(self.verify_db.getlastrowid(), [".txt", ".php", ".sh"])

        result = db_call(get_all_entries, "", self.verify_db)
        
        self.assertTrue(result.get("success"))
        self.assertEqual(len(result.get("data")), n)        

        for row in result.get("data"):
            self.assertEqual(row["file_types"], ".php, .sh, .txt")

    def test_get_all_entries_only_file_types(self):
        n = 3

        for i in range(n):
            self.create_file_type(i, [".txt", ".php", ".sh"])

        result = db_call(get_all_entries, "", self.verify_db)
        
        self.assertTrue(result.get("success"))
        self.assertEqual(len(result.get("data")), 0)

    def test_get_all_entries_filter_multiple_similar_names(self):
        n = 3

        for i in range(n):
            test_entry = self.create_test_entry(name=f"test{i}")
            self.create_sql_entry(test_entry)

        result = db_call(get_all_entries, "test", self.verify_db)
        
        self.assertTrue(result.get("success"))
        self.assertEqual(len(result.get("data")), n) 

    def test_get_all_entries_filter_one_name(self):
        n = 3

        for i in range(n):
            test_entry = self.create_test_entry(name=f"test{i}")
            self.create_sql_entry(test_entry)

        result = db_call(get_all_entries, "test1", self.verify_db)
        
        self.assertTrue(result.get("success"))
        self.assertEqual(len(result.get("data")), 1) 

    def test_get_all_entries_filter_name_not_exists(self):
        n = 3

        for i in range(n):
            test_entry = self.create_test_entry(name=f"abc{i}")
            self.create_sql_entry(test_entry)

        result = db_call(get_all_entries, "test", self.verify_db)
        
        self.assertTrue(result.get("success"))
        self.assertEqual(len(result.get("data")), 0) 

    def test_get_selected_entry_one_entry(self):
        test_entry = self.create_test_entry()
        self.create_sql_entry(test_entry)

        result = db_call(get_selected_entry, 1, self.test_db)
        actual = astuple(
            replace(test_entry, id=1)
        )

        self.assertTrue(result.get("success"))
        self.assertEqual(tuple(result.get("data")), actual)

    def test_get_selected_entry_multiple_entries(self):
        test_entry = self.create_test_entry()
        self.create_sql_entry(test_entry)
        n = 3

        for i in range(n):
            new_entry = self.create_test_entry(name=f"abc{i}")
            self.create_sql_entry(new_entry)

        result = db_call(get_selected_entry, 1, self.test_db)
        actual = astuple(
            replace(test_entry, id=1)
        )

        self.assertTrue(result.get("success"))
        self.assertEqual(tuple(result.get("data")), actual)

    def test_get_selected_entry_entry_not_exists(self):
        result = db_call(get_selected_entry, 1, self.test_db)

        self.assertTrue(result.get("success"))
        self.assertIsNone(result.get("data"))
        
    def test_get_file_types_single_type(self):
        self.create_file_type(1, [".txt"])

        result = db_call(get_file_types, 1, self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(len(result.get("data")), 1)
        self.assertEqual(result.get("data")[0][0],".txt")

    def test_get_file_types_multiple_types(self):
        file_types = [".c", ".php", ".txt"] 
        self.create_file_type(1, file_types)

        result = db_call(get_file_types, 1, self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(len(result.get("data")), 3)

        for i in range(len(result.get("data"))):
            self.assertEqual(result.get("data")[i][0], file_types[i])

    def test_get_file_types_no_types(self):
        result = db_call(get_file_types, 1, self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(len(result.get("data")), 0)

    def test_delete_entries_one_entry(self):
        test_entry = self.create_test_entry()
        self.create_sql_entry(test_entry)

        result = db_call(delete_entry, self.verify_db.getlastrowid(), self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(len(self.get_entries()), 0)

    def test_delete_entries_multiple_entries(self):
        n = 5
        
        for i in range(n):
            test_entry = self.create_test_entry()
            self.create_sql_entry(test_entry)

        result = db_call(delete_entry, self.verify_db.getlastrowid(), self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(len(self.get_entries()), n-1)

    def test_delete_entries_entry_not_exists(self):
        n = 5
        
        for i in range(n):
            test_entry = self.create_test_entry()
            self.create_sql_entry(test_entry)

        result = db_call(delete_entry, 999, self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(len(self.get_entries()), n)

    def test_delete_file_types_one_type(self):
        self.create_file_type(1, [".c", ".php", ".txt"])

        result = db_call(delete_file_types, 1, self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(len(self.get_file_types_by_id(1)), 0)

    def test_delete_file_types_multiple_types(self):
        n = 5
        
        for i in range(5):
            self.create_file_type(i, [".c", ".php", ".txt"])

        result = db_call(delete_file_types, 1, self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(len(self.get_file_types_by_id(1)), 0)
        self.assertEqual(len(self.get_all_file_types()), (n-1)*3)

    def test_delete_file_types_id_not_exists(self):
        n = 5
        
        for i in range(5):
            self.create_file_type(i, [".c", ".php", ".txt"])

        result = db_call(delete_file_types, 999, self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(len(self.get_file_types_by_id(999)), 0)
        self.assertEqual(len(self.get_all_file_types()), n*3)

    def test_edit_entry_valid_entry(self):
        test_entry = self.create_test_entry()
        self.create_sql_entry(test_entry)

        new_entry = replace(test_entry, id=self.verify_db.getlastrowid(), name="changed entry")
        result = db_call(edit_entry, new_entry, self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(self.get_entry_by_id(self.verify_db.getlastrowid())["name"], "changed entry")

    def test_edit_entry_invalid_entry(self):
        test_entry = self.create_test_entry()
        self.create_sql_entry(test_entry)

        new_entry = replace(test_entry, id=self.verify_db.getlastrowid(), name=None)
        result = db_call(edit_entry, new_entry, self.test_db)

        self.assertFalse(result.get("success"))
        self.assertStartsWith(result.get("error"), "Database error:")

    def test_edit_entry_multiple_entries(self):
        test_entry = self.create_test_entry()
        self.create_sql_entry(test_entry)
        entry_id = self.verify_db.getlastrowid()
        new_entry = replace(test_entry, id=entry_id, name="Testchangedabc")
        
        n = 5

        for i in range(n):
            new_test = self.create_test_entry(name=f"test{i}")
            self.create_sql_entry(new_test)

        result = db_call(edit_entry, new_entry, self.test_db)

        self.assertTrue(result.get("success"))
        self.assertEqual(self.get_entry_by_id(entry_id)["name"], "Testchangedabc")

if __name__ == "__main__":
    unittest.main()