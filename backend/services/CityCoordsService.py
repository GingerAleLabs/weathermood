from backend.domain.city_coords import CITY_COORDS

class CityCoordsService:

    @staticmethod
    def get_supported_cities_coords():
        return CITY_COORDS