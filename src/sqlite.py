import sqlite3
from pathlib import Path
from typing import List, Tuple
from .entry import Entry

DB_FILE = Path(__file__).resolve().parent.parent / "data" / "schema.db"

def create_tables(cursor: sqlite3.Cursor, conn: sqlite3.Connection) -> None:
    try:
        create_table_statements = [
            """CREATE TABLE IF NOT EXISTS scripts (
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
                file_types TEXT,
                last_run DATE,
                state TEXT
            );"""
        ]
        for statement in create_table_statements:
            cursor.execute(statement)

        conn.commit()

    except sqlite3.DatabaseError as e:
        print("Failed to open database:", e)

def tables_exist(cursor: sqlite3.Cursor) -> bool:
    tables = ["scripts"]
    tables = list(set(tables))
    placeholders = ",".join("?" for _ in tables)

    cursor.execute(f"""
        SELECT count(*) AS rows
        FROM sqlite_master
        WHERE type='table' AND name in ({placeholders})
    """, tables)
    
    return cursor.fetchone()[0] == len(tables)

def create_entry(entry: Entry) -> bool:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            if not tables_exist(cursor):
                create_tables(cursor, conn)

            sql = """
                INSERT INTO scripts(
                    name, description, type, interval_type, schedule_type, schedule_value,
                    originpath, destpath, include_dir, include_files, file_types, state
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                entry.file_types,
                "off"
            ))
            conn.commit()
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return False
    
    return True

def get_all_entries(name: str = "") -> List[Tuple]:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            if not tables_exist(cursor):
                create_tables(cursor, conn)

            sql = """
                SELECT id, name, description, type, interval_type, schedule_type, schedule_value,
                       originpath, destpath, include_dir, include_files, file_types, state
                FROM scripts
            """

            params = ()

            if name:
                sql += "Where name like ?"
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
                       originpath, destpath, include_dir, include_files, file_types
                FROM scripts
                Where id = ?
            """

            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            return Entry(*row)
        
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return None

def delete_entry(id: int) -> bool:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            if not tables_exist(cursor):
                create_tables(cursor, conn)
                return False

            sql = """
                DELETE FROM scripts
                WHERE id = ?
            """
            cursor.execute(sql, (id,))
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
                UPDATE scripts
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
                    include_files = ?,
                    file_types = ?
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
                entry.file_types,
                entry.id
            ))
            conn.commit()
    except sqlite3.DatabaseError as e:
        print("Failed to execute query:", e)
        return False
    
    return True