from backend.model.DbException import DbException
from backend.domain.weather_scale import get_weather_description, WEATHER_SCALE

from backend.model.db_queries import get_weekly_stats as db_queries_get_weekly_stats
from backend.model.db_queries import get_mood_per_weather_ranking as db_queries_get_mood_per_weather_ranking

from datetime import datetime

from backend.services.ServiceUnavailableException import ServiceUnavailableException
    
class StatsService:

    #Compute weekly stats: average mood, average temperature, average weather

    @staticmethod
    def get_weekly_stats():
        try:
            stats = db_queries_get_weekly_stats()

            return [
                {
                    **stat,
                    'year': datetime.fromisoformat(stat['timestamp']).isocalendar().year,
                    'week_number': datetime.fromisoformat(stat['timestamp']).isocalendar().week,
                }
                for stat in stats
            ]
        
        except (DbException, KeyError, ValueError) as e:
            raise ServiceUnavailableException("Could not retrieve the stats") from e


    # Retrieves average mood for each weather ranking
    # If there are no entries for a spefic weather ranking,
    # The retrieved data will be 0 and num_entries will be 0
    @staticmethod
    def get_mood_per_weather_ranking():
        try:
            raw_stats = db_queries_get_mood_per_weather_ranking()
            stats = {
                stat['weather_rating']: {
                    'weather_description': get_weather_description(stat['weather_rating']),
                    'avg_mood': stat['avg_mood'],
                    'num_entries': stat['num_entries']
                }
                for stat in raw_stats
                if stat['weather_rating'] in WEATHER_SCALE and stat['weather_rating'] != -1
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
        except (DbException, KeyError, ValueError) as e:
            raise ServiceUnavailableException("Could not retrieve the stats") from e
