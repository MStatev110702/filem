import sqlite3
from pathlib import Path
from typing import Tuple

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data"
DATA_PATH.mkdir(exist_ok=True)

class Database:
    def __init__(self, name: str,conn: sqlite3.Connection|None=None):
        self._conn = conn or sqlite3.connect(DATA_PATH / name)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()
        self.create_default_tables()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.connection.rollback()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit: bool=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql: str, params: Tuple=()):
        self.cursor.execute(sql, params)

    def executemany(self, sql, params: list):
        self.cursor.executemany(sql, params)

    def fetchall(self) -> list:
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql: str, params: Tuple=()) -> list:
        self.execute(sql, params)
        return self.fetchall()
    
    def getlastrowid(self):
        return self.cursor.lastrowid
    
    def create_default_tables(self):
        statements = [
            """CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                type TEXT NOT NULL,
                interval_type TEXT NOT NULL,
                schedule_type TEXT,
                schedule_value INT,
                originpath TEXT NOT NULL,
                destpath TEXT,
                include_dir TEXT NOT NULL,
                include_files TEXT NOT NULL,
                last_run DATE,
                state INTEGER
            );""",
            """CREATE TABLE IF NOT EXISTS file_types (
                entry_id INTEGER,
                file_type TEXT
            );"""
        ]

        for sql in statements:
            self.execute(sql)
            self.commit()
