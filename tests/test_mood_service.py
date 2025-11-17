import sqlite3
from datetime import datetime
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

    # Assertions
    assert len(rows) == 1
    row = rows[0]

    assert row["mood"] == 4
    assert row["note"] == "Feeling good today"
    assert abs(row["temperature"] - 22.5) < 0.01
    assert row["weather_rating"] == 3
    assert row["user_id"] is None
    assert row["timestamp"] is not None


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

    # Assertions
    assert len(rows) == 1
    row = rows[0]

    assert row["mood"] == 4
    assert row["note"] == "Feeling good today"
    assert abs(row["temperature"] - 22.5) < 0.01
    assert row["weather_rating"] == 3
    assert row["user_id"] is None
    assert row["timestamp"] is not None



def test_get_entries(tmp_path):
    # Using a dedicated test db
    test_db = tmp_path / "test.db"
    configure_db(str(test_db)) 

    # Insert 3 entries
    conn = get_connection()
    cur = conn.cursor()

    timestamp1 = datetime.now().isoformat()
    timestamp2 = datetime.now().isoformat()
    timestamp3 = datetime.now().isoformat()

    rows = [
        (None, timestamp1, 3, "Just okay", 16.1, 2),
        (None, timestamp2, 1, "Less than ideal", 5.7, 0),
        (None, timestamp3, 5, "Feelin' great :)", 22.3, 4),
    ]

    cur.executemany(
        """
        INSERT INTO mood_entry (user_id, timestamp, mood, note, temperature, weather_rating)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    conn.commit()
    conn.close()

    entries = MoodEntryService.get_entries()

    # Assertions
    assert len(entries) == 3
    
    #The entries will be returned in reverse chronological order, by design
    entry1 = entries[2]
    assert entry1["mood"] == 3
    assert entry1["note"] == "Just okay"
    assert abs(entry1["temperature"] - 16.1) < 0.01
    assert entry1["weather_rating"] == 2
    assert entry1["timestamp"] == timestamp1

    entry1 = entries[1]
    assert entry1["mood"] == 1
    assert entry1["note"] == "Less than ideal"
    assert abs(entry1["temperature"] - 5.7) < 0.01
    assert entry1["weather_rating"] == 0
    assert entry1["timestamp"] == timestamp2

    entry1 = entries[0]
    assert entry1["mood"] == 5
    assert entry1["note"] == "Feelin' great :)"
    assert abs(entry1["temperature"] - 22.3) < 0.01
    assert entry1["weather_rating"] == 4
    assert entry1["timestamp"] == timestamp3