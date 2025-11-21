import os
from pathlib import Path
import sqlite3

from backend.model.DbException import DbException

DEFAULT_DB_PATH = Path(__file__).parent / "weathermood.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

DB_PATH: Path | None = None


# Returns a connection to the db
# If the db file does not exist yet,
# this function creates and initializes it
def get_connection():

    # When testing, I set the env variable WM_DB_PATH to 
    # a temp db path dedicated to that single test
    # if env_path == True, then I'm testing and I should use that db
    # Otherwise, I'll just use the default db
    global DB_PATH
    env_path = os.environ.get("WM_DB_PATH")
    if env_path:
        DB_PATH = Path(env_path)
    else:
        DB_PATH = DEFAULT_DB_PATH

    try:
        if not DB_PATH.exists():
            _init_db()

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        return conn
    
    except sqlite3.Error as e:
        raise DbException ("Could not connect to the database") from e
    
    

# Creates the db and initializes it using the SCHEMA_PATH script
def _init_db():
    global DB_PATH
    if DB_PATH is None:
        DB_PATH = DEFAULT_DB_PATH

    try:
        db_file = Path(DB_PATH)
        with sqlite3.connect(db_file) as conn:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
    except (DbException, FileNotFoundError, PermissionError) as e:
        raise DbException("Could not initialize the database")


def insert_mock_data():
    try:
        with get_connection() as conn:

            mock_path = Path(__file__).parent / "mockdata.sql"

            with open(mock_path) as f:
                conn.executescript(f.read())
    except (DbException, FileNotFoundError, PermissionError):
        raise DbException("Could not insert mock data into the database")
