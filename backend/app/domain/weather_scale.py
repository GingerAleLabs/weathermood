# Internal weather scale
WEATHER_SCALE = {
    -1: "Unknown",
     0: "Stormy or hailing",
     1: "Raining or snowing",
     2: "Cloudy",
     3: "Partly cloudy",
     4: "Mostly sunny",
     5: "Sunny"
}

#conversion from Open-Meteo weather codes to WEATHER_SCALE
#
# Code | Description                          | Rating (0–9)
# -----------------------------------------------------------
# 0     | Clear sky                            | 5
# 1–2   | Mainly clear, partly cloudy          | 4-3
# 3     | Overcast                             | 2
# 45–48 | Fog, depositing rime fog             | 2
# 51–55 | Drizzle (light → dense)              | 1
# 56–57 | Freezing drizzle                     | 1
# 61–65 | Rain (light → heavy)                 | 1-1-1-0-0
# 66–67 | Freezing rain                        | 1-0
# 71–75 | Snowfall (light → heavy)             | 1-1-1-0-0
# 77    | Snow grains                          | 0
# 80–82 | Rain showers (light → violent)       | 1-1-0
# 85–86 | Snow showers                         | 1-0
# 95    | Thunderstorm                         | 0
# 96–99 | Thunderstorm with hail               | 0

rated0 = [64, 65, 67, 74, 75, 82, 86, 95, 96, 97, 98, 99]
rated1 = [51, 52, 53, 54, 55, 56, 57, 61, 62, 63, 66, 71, 72, 73, 80, 81, 85]
rated2 = [3, 45, 46, 47, 48]
rated3 = [2]
rated4 = [1]
rated5 = [0]

rated = [rated0, rated1, rated2, rated3, rated4, rated5]

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