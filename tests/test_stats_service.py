import sqlite3
from datetime import date, datetime, timedelta
from backend.model.db import configure_db, init_db, get_connection
from backend.services.StatsService import StatsService

def populate_db_for_stats_testing(conn):

    # Insert a few entries
    cur = conn.cursor()
    
    w1 = date.fromisoformat("2025-11-03") # year 2025, week 45 
    w2 = date.fromisoformat("2024-10-11") # year 2024, week 41
    w3 = date.fromisoformat("2023-09-13") # year 2023, week 37


    rows = [
        #week 1: avg mood 4, avg temp 16.6, avg weather rating 2.67, num entries 3
        (None, w1.isoformat(),                          3, "Just okay",         16.1,   1),
        (None, (w1 + timedelta(days=1)).isoformat(),    4, "Not too bad",       17.2,   3),
        (None, (w1 + timedelta(days=2)).isoformat(),    5, "Feelin' great :)",  16.5,   4),
        #week 2: avg mood 5, avg temp 21.4, avg weather rating 3.0, num entries 2
        (None, w2.isoformat(), 5, "Life's good", 22.3, 2),
        (None, (w2 + timedelta(days=1)).isoformat(), 5, "On a good roll", 20.5, 4),
        #week 3: avg mood 3, avg temp 24.3, avg weather rating 2.0, num entries 1
        (None, w3.isoformat(), 3, "Feeling tired", 24.3, 2),
    ]

    cur.executemany(
        """
        INSERT INTO mood_entry (user_id, timestamp, mood, note, temperature, weather_rating)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    conn.commit()
    

def test_weekly_stats(tmp_path):
    # Using a dedicated test db
    test_db = tmp_path / "test.db"
    configure_db(str(test_db)) 

    # Insert test entries
    conn = get_connection()
    populate_db_for_stats_testing(conn)
    conn.close()

    stats = StatsService.get_weekly_stats()

    # Assertions
    assert len(stats) == 3
    
    # week 1: year 2025, week 45, 
    # week 1: avg mood 4, avg temp 16.6, avg weather rating 2.67, num entries 3
    stats1 = stats[0]
    assert stats1["year"] == 2025
    assert stats1["week_number"] == 45
    assert stats1["avg_mood"] == 4
    assert abs(stats1["avg_temperature"] - 16.6) < 0.01
    assert abs(stats1["avg_weather_rating"] - 2.67) < 0.01
    assert stats1["num_entries"] == 3
    
    # week 2: year 2024, week 41
    # week 2: avg mood 5, avg temp 21.4, avg weather rating 3.0, num entries 2
    stats2 = stats[1]
    assert stats2["year"] == 2024
    assert stats2["week_number"] == 41
    assert stats2["avg_mood"] == 5
    assert abs(stats2["avg_temperature"] - 21.4) < 0.01
    assert abs(stats2["avg_weather_rating"] - 3) < 0.01
    assert stats2["num_entries"] == 2

    # week 3: year 2023, week 37
    # week 3: avg mood 3, avg temp 24.3, avg weather rating 2.0, num entries 1
    stats3 = stats[2]
    assert stats3["year"] == 2023
    assert stats3["week_number"] == 37
    assert stats3["avg_mood"] == 3
    assert abs(stats3["avg_temperature"] - 24.3) < 0.01
    assert abs(stats3["avg_weather_rating"] - 2) < 0.01
    assert stats3["num_entries"] == 1