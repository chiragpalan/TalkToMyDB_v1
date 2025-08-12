import sqlite3

def get_connection(db_path: str):
    """Return a SQLite connection."""
    return sqlite3.connect(db_path)

def get_schema_as_text(db_path: str):
    """Return schema of all tables as a text string."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    schema_text = ""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for (table_name,) in tables:
        schema_text += f"\nTable: {table_name}\n"
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = cursor.fetchall()
        for col in cols:
            schema_text += f" - {col[1]} ({col[2]})\n"

    conn.close()
    return schema_text
