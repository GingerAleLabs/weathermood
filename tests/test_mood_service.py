import sqlite3
from backend.model.db import configure_db, init_db, get_connection
from backend.services.MoodEntryService import MoodEntryService

def test_add_entry(tmp_path):
    # Using a dedicated test db
    test_db = tmp_path / "test.db"
    configure_db(str(test_db)) 

    MoodEntryService.add_entry(
        user_id=None,
        mood=4,
        note="Feeling good today",
        temperature=22.5,
        weather_rating=3,
    )

    # Check the entry was correctly inserted
    conn = get_connection()
    cur = conn.execute("SELECT * FROM mood_entry")
    rows = cur.fetchall()
    conn.close()

    # 5. Assertions
    assert len(rows) == 1
    row = rows[0]

    assert row["mood"] == 4
    assert row["note"] == "Feeling good today"
    assert abs(row["temperature"] - 22.5) < 0.001
    assert row["weather_rating"] == 3
    assert row["user_id"] is None
    assert row["timestamp"] is not None
