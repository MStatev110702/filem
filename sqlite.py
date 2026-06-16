import sqlite3
import os.path

database = "schema.db"
create_table_statements = [
    """CREATE TABLE IF NOT EXISTS scripts (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        type TEXT NOT NULL,
        interval_type TEXT NOT NULL,
        amount INT,
        repeat_type TEXT,
        day INT,
        time TEXT,
        originpath TEXT NOT NULL,
        destpath TEXT,
        include_dir TEXT NOT NULL,
        include_filies TEXT NOT NULL,
        file_types TEXT
    );"""
]

def database_exists():
    if not os.path.exists(database):
        open(database, "x")
        create_tables()

def create_tables():
    try:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()

            for statement in create_table_statements:
                cursor.execute(statement)

            conn.commit()

    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)