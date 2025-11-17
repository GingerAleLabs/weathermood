from backend.app.model.db import get_connection
from backend.app.domain.weather_scale import get_weather_description, WEATHER_SCALE
from datetime import datetime
    
class StatsService:

    #Compute weekly stats: average mood, average temperature, average weather

    @staticmethod
    def get_weekly_stats():
        # Fetch raw entries and group by ISO year/week in Python to get correct ISO week numbers
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT timestamp, mood, temperature, weather_rating
            FROM mood_entry
            ORDER BY timestamp DESC
            """
        )
        rows = cur.fetchall()
        conn.close()

        groups = {}
        for row in rows:
            # timestamp stored as ISO-8601 string
            ts = datetime.fromisoformat(row['timestamp'])
            iso_year, iso_week, _ = ts.isocalendar()
            key = (iso_year, iso_week)
            if key not in groups:
                groups[key] = {
                    'sum_mood': 0.0,
                    'sum_temp': 0.0,
                    'sum_weather': 0.0,
                    'count': 0,
                    'latest_ts': ts
                }

            g = groups[key]
            g['sum_mood'] += row['mood']
            g['sum_temp'] += row['temperature']
            g['sum_weather'] += row['weather_rating']
            g['count'] += 1
            if ts > g['latest_ts']:
                g['latest_ts'] = ts

        # Sort groups by the latest timestamp in each group (descending) to keep recent weeks first
        sorted_groups = sorted(groups.items(), key=lambda kv: kv[1]['latest_ts'], reverse=True)

        stats = []
        for (year, week), g in sorted_groups:
            avg_mood = g['sum_mood'] / g['count']
            avg_temp = g['sum_temp'] / g['count']
            avg_weather = g['sum_weather'] / g['count']
            stats.append(
                {
                    'year': year,
                    'week_number': week,
                    'avg_mood': avg_mood,
                    'avg_temperature': avg_temp,
                    'avg_weather_rating': avg_weather,
                    'avg_weather_description': get_weather_description(round(avg_weather)),
                    'num_entries': g['count']
                }
            )

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