import sqlite3
from pathlib import Path
from typing import List, Tuple
from .entry import Entry

DB_FILE = Path(__file__).resolve().parent.parent / "data" / "schema.db"

def create_tables(cursor: sqlite3.Cursor, conn: sqlite3.Connection) -> None:
    try:
        create_table_statements = [
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
        for statement in create_table_statements:
            cursor.execute(statement)

        conn.commit()

    except sqlite3.DatabaseError as e:
        print("Failed to open database:", e)

def tables_exist(cursor: sqlite3.Cursor) -> bool:
    tables = ["entries", "file_types"]
    tables = list(set(tables))
    placeholders = ",".join("?" for _ in tables)

    cursor.execute(f"""
        SELECT count(*) AS rows
        FROM sqlite_master
        WHERE type='table' AND name in ({placeholders})
    """, tables)
    
    return cursor.fetchone()[0] == len(tables)

def create_entry(entry: Entry, file_types: list[str]) -> bool:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            if not tables_exist(cursor):
                create_tables(cursor, conn)

            entry_sql = """
                INSERT INTO entries(
                    name, description, type, interval_type, schedule_type, schedule_value,
                    originpath, destpath, include_dir, include_files, state
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(entry_sql, (
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
                0
            ))

            if not create_file_type(cursor, cursor.lastrowid, file_types):
                print("Failed to create file_types")
                return False

            conn.commit()
            return True
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return False
    
def get_all_entries(name: str = "") -> List[Tuple]:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            if not tables_exist(cursor):
                create_tables(cursor, conn)

            sql = """
                SELECT e.id, e.name, e.description, e.type, e.interval_type, e.schedule_type, e.schedule_value,
                       e.originpath, e.destpath, e.include_dir, e.include_files, GROUP_CONCAT(ft.file_type, ', ') as file_types, e.state
                FROM entries e
                INNER JOIN file_types ft ON e.id = ft.entry_id
                GROUP BY e.id
            """
            params = ()

            if name:
                sql += "WHERE e.name like ?"
                params = (f"%{name}%",)

            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return rows
        
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return []
    
def get_selected_entry(id: int) -> Entry|None:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            if not tables_exist(cursor):
                create_tables(cursor, conn)

            sql = """
                SELECT id, name, description, type, interval_type, schedule_type, schedule_value,
                       originpath, destpath, include_dir, include_files
                FROM entries 
                Where id = ?
            """

            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            return Entry(*row)
        
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return None
    
def get_file_types(id: int) -> List[str]:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            if not tables_exist(cursor):
                create_tables(cursor, conn)

            sql = """
                SELECT file_type
                FROM file_types
                WHERE entry_id = ?
            """

            cursor.execute(sql, (id,))

            return [r[0] for r in cursor.fetchall()]
        
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return []

def delete_entry(id: int) -> bool:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            if not tables_exist(cursor):
                create_tables(cursor, conn)
                return False

            sql = """
                DELETE FROM entries
                WHERE id = ?
            """
            cursor.execute(sql, (id,))

            if not delete_file_types(cursor, id):
                print("Failed to delete file types")
                return False

            return True
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return False
    
def edit_entry(entry:Entry) -> bool:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            if not tables_exist(cursor):
                create_tables(cursor, conn)
            sql = """
                UPDATE entries
                SET
                    name = ?, 
                    description = ?, 
                    type = ?,
                    interval_type = ?, 
                    schedule_type = ?,
                    schedule_value = ?,
                    originpath = ?, 
                    destpath = ?, 
                    include_dir = ?, 
                    include_files = ?
                WHERE
                    id = ?
            """
            cursor.execute(sql, (
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
                entry.id
            ))
            conn.commit()
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return False
    
    return True

def create_file_type(cursor: sqlite3.Cursor, id: int, file_types: list[str]) -> bool:
    try:
        file_types_sql = """
            INSERT INTO file_types (entry_id, file_type)
            VALUES (?, ?)
        """
            
        cursor.executemany(file_types_sql, [(id, ft) for ft in file_types])
        return True
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return False

def delete_file_types(cursor: sqlite3.Cursor, id: int) -> bool:
    try:
        sql = """
            DELETE FROM file_types
            WHERE entry_id = ?
        """
        
        cursor.execute(sql, (id,))
        return True
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return False 

def edit_file_types(id: int, file_types: list[str]) -> bool:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            if not tables_exist(cursor):
                create_tables(cursor, conn)
                return False
            
            if not delete_file_types(cursor, id):
                print("Failed to delete file types")
                return False

            if not create_file_type(cursor, id, file_types):
                print("Failed to create file types")
                return False

            conn.commit()
            return True
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return False