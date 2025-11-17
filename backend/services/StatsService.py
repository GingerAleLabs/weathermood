from backend.model.db import get_connection
from backend.domain.weather_scale import get_weather_description, WEATHER_SCALE
    
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
    

    # Retrieves average mood for each weather ranking
    # If there are no entries for a spefic weather ranking,
    # The retrieved data will be 0 and num_entries will be 0
    @staticmethod
    def get_mood_per_weather_ranking():
        conn = get_connection()
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
        conn.close()

        stats = {
            row['weather_rating']:
            {
                'weather_description': get_weather_description(row['weather_rating']),
                'avg_mood': row['avg_mood'],
                'num_entries': row['num_entries']
            }
            for row in rows
            if row['weather_rating'] in WEATHER_SCALE and row['weather_rating'] != -1
        }

        # adding the stats for those weather rankings for which I have no data 
        # (cannot be retrieved from the db)
        stats = stats | {
            rating: {
                'weather_description': get_weather_description(rating),
                'avg_mood': 0,
                'num_entries': 0
            }
            for rating in WEATHER_SCALE.keys()
            if rating not in stats.keys() and rating != -1
        }

        return dict(sorted(stats.items()))