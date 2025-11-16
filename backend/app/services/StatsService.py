from backend.app.model.db import get_connection
from backend.app.domain.weather_scale import get_weather_description
    
class StatsService:

    #Compute weekly stats: average mood, average temperature, average weather

    @staticmethod
    def get_weekly_stats():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT strftime('%Y', timestamp) AS year, strftime('%W', timestamp) AS week_number, AVG(mood) AS avg_mood, AVG(temperature) AS avg_temperature, AVG(weather_rating) AS avg_weather_rating, COUNT(*) as num_entries 
            FROM mood_entry 
            GROUP BY strftime('%Y', timestamp), strftime('%W', timestamp)
            ORDER BY timestamp DESC
            """
        )
        rows = cur.fetchall()
        conn.close()

        stats = [
            {
                'year': row['year'], 
                'week_number': row['week_number'], 
                'avg_mood': row['avg_mood'], 
                'avg_temperature': row['avg_temperature'], 
                'avg_weather_rating': row['avg_weather_rating'],
                'avg_weather_description': get_weather_description(round(row['avg_weather_rating'])),
                'num_entries': row['num_entries']
            }
            for row in rows
        ]

        return stats
    