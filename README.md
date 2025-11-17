WEATHERMOOD
-- an app that lets you track / investigate the correlation between the weather and your mood

Provides a simple CLI (future extension > REST API) to:
    - log an entry (mood, weather info and optional notes)
    - retrieve all entries
    - get weekly stats (average mood vs weather)
    - get mood stats for weather rating (how well do you feel when the weather is ..?)

Tech stack:
    - Live weather data for a specific location (lat/lon or predefined city) is fetched through OpenMeteo API
    - Data stored locally (SQLite)
    - Pytest for testing

Important:
Commands must be given from the project root weathermood

Loading mock db (erases all data):
    python .\backend\mock.py 

Running tests:
    pytest

CLI commands:
    python -m cli <command>
    python -m cli --help => shows supported commands
    python -m cli <command> --help => shows command info and params