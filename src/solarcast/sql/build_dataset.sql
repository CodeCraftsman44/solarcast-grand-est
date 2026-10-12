WITH rte_hourly AS (
    -- Half-hourly -> hourly. AVG also merges the March DST duplicates.
    SELECT
        date_trunc('hour', date_heure) AS hour,
        AVG(solaire)      AS solar_mw,
        AVG(consommation) AS consumption_mw,
        AVG(tch_solaire)  AS solar_load_factor_pct
    FROM read_parquet('{rte}')
    WHERE date_heure >= TIMESTAMPTZ '2022-01-01 00:00:00+00'
    GROUP BY hour
),


weather_hourly AS (
    -- Average the 8 weather points into one regional value per hour.
    SELECT
        time AS hour,
        AVG(shortwave_radiation) AS ghi_wm2,
        AVG(direct_radiation)    AS direct_wm2,
        AVG(diffuse_radiation)   AS diffuse_wm2,
        AVG(cloud_cover)         AS cloud_cover_pct,
        AVG(temperature_2m)      AS temp_c
    FROM read_parquet('{weather}')
    GROUP BY time
)


SELECT
    r.hour,
    r.solar_mw,
    r.consumption_mw,
    r.solar_load_factor_pct,
    100 * r.solar_mw / NULLIF(r.consumption_mw, 0) AS solar_share_pct,
    w.ghi_wm2,
    w.direct_wm2,
    w.diffuse_wm2,
    w.cloud_cover_pct,
    w.temp_c
FROM rte_hourly AS r
INNER JOIN weather_hourly AS w
    ON r.hour = w.hour
ORDER BY r.hour