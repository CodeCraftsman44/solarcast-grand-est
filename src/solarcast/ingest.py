import pandas as pd
import requests

from solarcast.config import RAW, REGION, RTE_URL

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

def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    fetch_rte()

if __name__ == "__main__":
    main()