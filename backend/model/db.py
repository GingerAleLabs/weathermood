from pathlib import Path
import sqlite3

DEFAULT_DB_PATH = Path(__file__).parent / "weathermood.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

DB_PATH = None

_initialized = False

# if called before get_connection(), allows to change the path of the DB
# Useful to run tests with a separate db file 
def configure_db(path):
    global DB_PATH
    DB_PATH = path


def get_connection():

    global DB_PATH
    if DB_PATH is None:
        DB_PATH = DEFAULT_DB_PATH

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
    
    global DB_PATH
    db_file = Path(DB_PATH)
    if not db_file.exists():
        with sqlite3.connect(db_file) as conn:
            with open(SCHEMA_PATH) as f:
                conn.executescript(f.read())

    _initialized = True

def insert_mock_data():
    conn = get_connection()

    mock_path = Path(__file__).parent / "mockdata.sql"

    with sqlite3.connect(DB_PATH) as conn:
            with open(mock_path) as f:
                conn.executescript(f.read())
