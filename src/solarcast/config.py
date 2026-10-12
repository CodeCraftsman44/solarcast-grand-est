from datetime import date, timedelta
from pathlib import Path

#setting file paths to where the data should be stored
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

#setting date limits
START = "2022-01-01"
END = (date.today() - timedelta(days=2)).isoformat()

#Grand est Data API
RTE_URL = (
    "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
    "eco2mix-regional-cons-def/exports/parquet"
)
REGION = "Grand Est"

#Wheather data
WEATHER_URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"
WEATHER_VARS = [
    "shortwave_radiation",
    "direct_radiation",
    "diffuse_radiation",
    "cloud_cover",
    "temperature_2m",
]
POINTS = {
    "strasbourg": (48.58, 7.75),
    "colmar": (48.08, 7.36),
    "mulhouse": (47.75, 7.34),
    "nancy": (48.69, 6.18),
    "metz": (49.12, 6.18),
    "epinal": (48.17, 6.45),
    "reims": (49.26, 4.03),
    "troyes": (48.30, 4.08),
}