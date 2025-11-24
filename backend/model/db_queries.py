from backend.model.DbException import DbException
from backend.model.db import get_connection

from datetime import datetime

# Caller takes care of validation
def add_entry(user_id, mood, note, temperature, weather_rating):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            timestamp = datetime.now().isoformat()
            cur.execute(
                    """
                    INSERT INTO mood_entry (user_id, timestamp, mood, note, temperature, weather_rating)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (user_id, timestamp, mood, note, temperature, weather_rating)
                )
            conn.commit()
    except Exception:
        raise DbException
    

def get_entries(year=None, month=None):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            query = """
                SELECT timestamp, mood, note, temperature, weather_rating 
                FROM mood_entry 
                """

            filters = []
            params = []

            if year is not None:
                filters.append("strftime('%Y', timestamp) = ?")
                params.append(str(year))

            if month is not None:
                filters.append("strftime('%m', timestamp) = ?")
                params.append(str(month))

            if filters:
                query += " WHERE " + " AND ".join(filters)

            query += " ORDER BY timestamp DESC"

            cur.execute(query, params)
            return cur.fetchall()
        
    except Exception:
        raise DbException
    

def get_weekly_stats(year, month):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            query = """
                SELECT timestamp, AVG(mood) AS avg_mood, AVG(temperature) AS avg_temperature, AVG(weather_rating) AS avg_weather_rating, COUNT(*) as num_entries 
                FROM mood_entry 
            """

            filters = []
            params = []

            if year is not None:
                filters.append("strftime('%Y', timestamp) = ?")
                params.append(str(year))

            if month is not None:
                filters.append("strftime('%m', timestamp) = ?")
                params.append(str(month))

            if filters:
                query += " WHERE " + " AND ".join(filters)

            query += """
                GROUP BY strftime('%Y', timestamp), strftime('%W', timestamp)
                ORDER BY timestamp DESC
            """

            cur.execute(query, params)
            return cur.fetchall()
        
    except Exception:
        raise DbException
    

def get_mood_per_weather_ranking():
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            
            cur.execute(
                """
                SELECT weather_rating, AVG(mood) AS avg_mood, COUNT(*) as num_entries
                FROM mood_entry
                GROUP BY weather_rating
                ORDER BY weather_rating ASC
                """
            )
            rows = cur.fetchall()
            return rows

    except Exception:
        raise DbException