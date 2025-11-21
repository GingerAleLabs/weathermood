from pathlib import Path
import sqlite3

from backend.model.DbException import DbException

DEFAULT_DB_PATH = Path(__file__).parent / "weathermood.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

DB_PATH: Path | None = None


# if called before get_connection(), allows to change the path of the DB
# Useful to run tests with a separate db file 
def configure_db(path):
    global DB_PATH
    DB_PATH = Path(path)

# Returns a connection to the db
# If the db file does not exist yet,
# this function creates and initializes it
def get_connection():

    global DB_PATH
    if DB_PATH is None:
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
    except DbException, FileNotFoundError, PermissionError:
        raise DbException("Could not insert mock data into the database")
