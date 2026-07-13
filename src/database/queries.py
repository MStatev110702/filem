import sqlite3
from datetime import datetime
from .db import Database
from .query_response import QueryResponse
from ..entities.entry import Entry

def db_call(fn, *args, **kwargs) -> QueryResponse:
    try:
        return {
            "success": True,
            "data": fn(*args, **kwargs),
        }
    except sqlite3.DatabaseError as e:
        return {
            "success": False,
            "error": f"Database error:\n{e}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error:\n{e}",
        }
    
def get_db(db: Database|None) -> Database:
    return db or Database("filemanager.db")

def create_entry(entry: Entry, next_run: datetime, db: Database|None = None) -> int:
    db = get_db(db)

    with db:
        sql = """
            INSERT INTO entries(
                name, description, type, interval_type, schedule_type, schedule_value,
                originpath, destpath, include_dir, include_files, state, next_run
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        db.execute(sql, (
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
            entry.state,
            next_run
        ))

        return db.getlastrowid()

def create_file_types(id: int, file_types: list[str], db: Database|None = None) -> None:
    db = get_db(db)

    with db:
        sql = """
            INSERT INTO file_types (entry_id, file_type)
            VALUES (?, ?)
        """
            
        db.executemany(sql, [(id, ft) for ft in file_types])
    
def get_all_entries(name: str = "", db: Database|None = None) -> list:
    db = get_db(db)

    with db:
        where_part = ""
        params = ()
        if name.strip() != "":
            where_part += "and e.name like ?"
            params = (f"%{name.strip()}%",)

        sql = f"""
            SELECT e.id, e.name, e.description, e.type, e.interval_type, e.schedule_type, e.schedule_value,
                    e.originpath, e.destpath, e.include_dir, e.include_files, 
                    GROUP_CONCAT(ft.file_type, ', ' ORDER BY ft.file_type) as file_types, e.state,
                    strftime('%d.%m.%Y %H:%M:%S', last_run) as last_run, strftime('%d.%m.%Y %H:%M:%S', next_run) as next_run
            FROM entries e
            LEFT JOIN file_types ft ON e.id = ft.entry_id
            WHERE 1=1 {where_part}
            GROUP BY e.id
        """

        return db.query(sql, params)

def get_selected_entry(id: int, db: Database|None = None):
    db = get_db(db)

    with db:
        sql = """
            SELECT id, name, description, type, interval_type, schedule_type, schedule_value,
                    originpath, destpath, include_dir, include_files, state, strftime('%d.%m.%Y %H:%M:%S', next_run) as next_run
            FROM entries 
            Where id = ?
        """

        db.execute(sql, (id,))

        return db.fetchone()

def get_active_entries(db: Database|None = None) -> list:
    db = get_db(db)

    with db:
        sql = """
            SELECT id
            FROM entries
            WHERE STATE = 1 and INTERVAL_TYPE != 'manually'
        """

        db.execute(sql)

        return db.fetchall()

    
def get_file_types(id: int, db: Database|None = None) -> list:
    db = get_db(db)
    
    with db:
        sql = """
            SELECT file_type
            FROM file_types
            WHERE entry_id = ?
            ORDER BY file_type
        """

        return db.query(sql, (id,))
    
def delete_entry(id: int, db: Database|None = None) -> None:
    db = get_db(db)
    
    with db:
        sql = """
            DELETE FROM entries
            WHERE id = ?
        """
        db.execute(sql, (id,))

def delete_file_types(id: int, db: Database|None = None) -> None:
    db = get_db(db)
    with db:
        sql = """
            DELETE FROM file_types
            WHERE entry_id = ?
        """
        
        db.execute(sql, (id,))

def edit_entry(entry:Entry, next_run: datetime, db: Database|None = None) -> None:
    db = get_db(db)

    with db:
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
                include_files = ?,
                state = ?,
                next_run = ?
            WHERE
                id = ?
        """

        db.execute(sql, (
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
            entry.state,
            next_run,
            entry.id
        ))

def edit_file_types(id: int, file_types: list) -> None:
    delete_file_types(id)
    create_file_types(id, file_types)


def change_entry_state(id: int, state: int, db: Database|None = None) -> None:
    db = get_db(db)

    with db:
        sql = """
            UPDATE entries
            SET
                state = ?
            WHERE
                id = ?
        """

        db.execute(sql, (state, id))

def update_last_run(id: int, db: Database|None = None) -> None:
    db = get_db(db)

    with db:
        sql = """
            UPDATE entries
            SET
                last_run = ?
            WHERE 
                id = ?
        """
        
        db.execute(sql, (datetime.now(), id))

def update_next_run(id: int, next_run: datetime, db: Database|None = None) -> None:
    db = get_db(db)

    with db:
        sql = """
            UPDATE entries
            SET
                next_run = ?
            WHERE
                id = ?
        """

        db.execute(sql, (next_run, id))