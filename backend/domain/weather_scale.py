# Internal weather scale
WEATHER_SCALE = {
    -1: "Unknown",
     1: "Stormy or hailing",
     2: "Raining or snowing",
     3: "Cloudy",
     4: "Partly cloudy",
     5: "Sunny"
}

#conversion from Open-Meteo weather codes to WEATHER_SCALE
#
# Code | Description                          | Rating (1–5)
# -----------------------------------------------------------
# 0–1   | Clear sky / Mainly clear             | 5
# 2     | Partly cloudy                        | 4
# 3     | Overcast                             | 3
# 45–48 | Fog, depositing rime fog             | 3
# 51–57 | Drizzle / Freezing drizzle           | 2
# 61–63 | Rain (light → moderate)              | 2
# 64–65 | Rain (heavy)                         | 1
# 66–67 | Freezing rain                        | 1
# 71–73 | Snowfall (light → moderate)          | 2
# 74–75 | Snowfall (heavy)                     | 1
# 80–81 | Rain showers (light → moderate)      | 2
# 82    | Rain showers (violent)               | 1
# 85    | Snow showers (light)                 | 2
# 86    | Snow showers (heavy)                 | 1
# 95    | Thunderstorm                         | 1
# 96–99 | Thunderstorm with hail               | 1

rated1 = [64, 65, 67, 74, 75, 82, 86, 95, 96, 97, 98, 99]
rated2 = [51, 52, 53, 54, 55, 56, 57, 61, 62, 63, 66, 71, 72, 73, 80, 81, 85]
rated3 = [3, 45, 46, 47, 48]
rated4 = [2]
rated5 = [0,1]

rated = [rated1, rated2, rated3, rated4, rated5]

WEATHER_CODE_TO_RATING =  {x: idx for idx, r in enumerate(rated) for x in r}

# from the internal weather scale, returns a weather description
def get_weather_description(rating:int) -> str:
    if (rating in WEATHER_SCALE):
        return WEATHER_SCALE[rating]
    else:
        return ""
    
#converts the OpenMeteo weather rating to the internal weather scale
def convert_openmeteo_rating(openmeteorating:int) -> int:
    if (openmeteorating in WEATHER_CODE_TO_RATING.keys()):
        return WEATHER_CODE_TO_RATING[openmeteorating]
    return -1