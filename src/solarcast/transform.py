from pathlib import Path

import duckdb

from solarcast.config import PROCESSED, RAW

SQL_FILE = Path(__file__).parent / "sql" / "build_dataset.sql"



def build_dataset() -> None:
    """Run the SQL on the raw files and save the result as Parquet."""
    sql = SQL_FILE.read_text(encoding="utf-8").format(
        rte=(RAW / "rte_grand_est.parquet").as_posix(),
        weather=(RAW / "weather_grand_est.parquet").as_posix(),
    )
    out = PROCESSED / "dataset_hourly.parquet"

    con = duckdb.connect()
    con.sql("SET TimeZone = 'UTC'")
    con.sql(f"COPY ({sql}) TO '{out.as_posix()}' (FORMAT parquet)")

    rows, first, last = con.sql(
        f"SELECT COUNT(*), MIN(hour), MAX(hour) FROM '{out.as_posix()}'"
    ).fetchone()
    print(f"Dataset: {rows:,} hourly rows, {first} -> {last}")
    print(f"Saved -> {out}")



def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    build_dataset()


if __name__ == "__main__":
    main()