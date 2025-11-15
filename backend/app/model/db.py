from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).parent / "weathermood.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

_initialized = False


def get_connection():
    global _initialized
    if not _initialized:
        init_db()
        _initialized = True
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    global _initialized
    if _initialized:
        return

    if not DB_PATH.exists():
        with sqlite3.connect(DB_PATH) as conn:
            with open(SCHEMA_PATH) as f:
                conn.executescript(f.read())

    _initialized = True

def insert_mock_data():
    conn = get_connection()

    mock_path = Path(__file__).parent / "mockdata.sql"

    with sqlite3.connect(DB_PATH) as conn:
            with open(mock_path) as f:
                conn.executescript(f.read())
