import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from src.entry import Entry
from src.sqlite import create_entry

class TestSqlite(unittest.TestCase):
    def test_create_entry_success(self):
        test_entry = Entry(
            id=None,
            name="Unittest create entry success copy",
            description="Unittest can be deleted",
            type="COPY",
            interval_type="newest",
            schedule_type="",
            schedule_value=0,
            originpath="/filemanager",
            destpath="/filemanager/ui",
            include_dir="none",
            include_files="none"
        )
        file_types=["png", "pdf"]
        result = create_entry(test_entry, file_types)

        self.assertTrue(result)

    @patch("src.sqlite.sqlite3.connect")
    def test_create_entry_connection_failure(self, mock_connect):
        mock_connect.side_effect = sqlite3.OperationalError("DB unavailable")
        test_entry = Entry(
            id=None,
            name="Unittest create entry success copy",
            description="Unittest can be deleted",
            type="COPY",
            interval_type="newest",
            schedule_type="",
            schedule_value=0,
            originpath="/filemanager",
            destpath="/filemanager/ui",
            include_dir="none",
            include_files="none",
        )
        result = create_entry(test_entry, [])

        self.assertFalse(result)

    @patch("src.sqlite.sqlite3.connect")
    def test_create_entry_execute_failure(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.execute.side_effect = sqlite3.OperationalError("Bad SQL")

        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None      
        mock_connect.return_value = mock_conn

        test_entry = Entry(
            id=None,
            name="Unittest create entry success copy",
            description="Unittest can be deleted",
            type="COPY",
            interval_type="newest",
            schedule_type="",
            schedule_value=0,
            originpath="/filemanager",
            destpath="/filemanager/ui",
            include_dir="none",
            include_files="none",
        )

        result = create_entry(test_entry, [])

        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()