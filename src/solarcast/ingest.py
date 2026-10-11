import pandas as pd
import requests

from solarcast.config import (
    END, POINTS, RAW, REGION, RTE_URL, START, WEATHER_URL, WEATHER_VARS,
)


def fetch_rte() -> None:
    #Download Grand Ets data eCO2mix data in one export call
    params = {"where": f'libelle_region="{REGION}"'}
    r = requests.get(RTE_URL, params=params, timeout=600)
    r.raise_for_status()

    out = RAW/"rte_grand_est.parquet"
    out.write_bytes(r.content)

    df = pd.read_parquet(out)
    print(f"RTE: {len(df):,} rows -> {out}")
    print("Columns:", list(df.columns))

def fetch_weather() -> None:
    """Download historical forecasts for each weather point, stacked into one table."""
    frames = []
    for name, (lat, lon) in POINTS.items():
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": START,
            "end_date": END,
            "hourly": ",".join(WEATHER_VARS),
            "timezone": "UTC",
        }
        r = requests.get(WEATHER_URL, params=params, timeout=300)
        r.raise_for_status()

        h = pd.DataFrame(r.json()["hourly"])
        h["time"] = pd.to_datetime(h["time"], utc=True)
        h["point"] = name
        frames.append(h)
        print(f"Weather {name}: {len(h):,} rows")

    out = RAW / "weather_grand_est.parquet"
    pd.concat(frames, ignore_index=True).to_parquet(out, index=False)
    print(f"Weather total -> {out}")


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    fetch_rte()
    fetch_weather()

if __name__ == "__main__":
    main()