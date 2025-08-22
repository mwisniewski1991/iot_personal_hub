
-- Parametryzowane zapytanie agregacji danych battery dla określonego przedziału czasowego
WITH bounds as (
  SELECT
    --  '2025-08-01 11:00:00'::timestamp AS hour_start,
    --  '2025-08-01 13:00:00'::timestamp AS hour_end
   '{{ data_interval_start }}'::timestamp AS hour_start,
   '{{ data_interval_end }}'::timestamp AS hour_end
)
,hour_series AS (
  SELECT generate_series(
    date_trunc('hour', b.hour_start),
    date_trunc('hour', b.hour_end) - interval '1 hour',
    interval '1 hour'
  ) AS hour_start
  FROM bounds b
)
,devices AS (
  SELECT DISTINCT device_id
  FROM iot_personal_hub.raw_devices_properties dl
  JOIN bounds b ON TRUE
  WHERE (to_timestamp(dl.device_timestamp)) >= b.hour_start
    AND (to_timestamp(dl.device_timestamp)) < b.hour_end
)
,agg AS (
  SELECT
    dl.device_id,
    date_trunc('hour', (to_timestamp(dl.device_timestamp))) AS hour_start,
    round(min((dl.properties #> '{location, altitude_m}')::INTEGER),2) as altitude_min,
    round(avg((dl.properties #> '{location, altitude_m}')::INTEGER),2) as altitude_avg,
    round(max((dl.properties #> '{location, altitude_m}')::INTEGER),2) as altitude_max,
    round(min((dl.properties #> '{location, latitude}')::INTEGER),2) as latitude_min,
    round(avg((dl.properties #> '{location, latitude}')::INTEGER),2) as latitude_avg,
    round(max((dl.properties #> '{location, latitude}')::INTEGER),2) as latitude_max,
    round(min((dl.properties #> '{location, longitude}')::INTEGER),2) as longitude_min,
    round(avg((dl.properties #> '{location, longitude}')::INTEGER),2) as longitude_avg,
    round(max((dl.properties #> '{location, longitude}')::INTEGER),2) as longitude_max 
  FROM iot_personal_hub.raw_devices_properties dl
  INNER JOIN iot_personal_hub.dim_devices dd
  	on dl.device_id = dd.id
  WHERE dd.type = 'smartphone'
  	-- AND (to_timestamp(dl.device_timestamp)) >= '2025-08-01 11:00:00'::timestamp
    -- AND (to_timestamp(dl.device_timestamp)) < '2025-08-01 13:00:00'::timestamp
    AND (to_timestamp(dl.device_timestamp)) >= '{{ data_interval_start }}'::timestamp 
    AND (to_timestamp(dl.device_timestamp)) < '{{ data_interval_end }}'::timestamp 
  GROUP BY dl.device_id, date_trunc('hour', (to_timestamp(dl.device_timestamp)))
)
,grid AS (
  SELECT d.device_id, h.hour_start
  FROM devices d CROSS JOIN hour_series h
)
,final_rows AS (
  SELECT
    g.device_id,
    g.hour_start AS date_hour,
    COALESCE(a.altitude_min, 0) AS altitude_min,
    COALESCE(a.altitude_avg, 0) AS altitude_avg,
    COALESCE(a.altitude_max, 0) AS altitude_max,
    COALESCE(a.latitude_min, 0) AS latitude_min,
    COALESCE(a.latitude_avg, 0) AS latitude_avg,
    COALESCE(a.latitude_max, 0) AS latitude_max,
    COALESCE(a.longitude_min, 0) AS longitude_min,
    COALESCE(a.longitude_avg, 0) AS longitude_avg,
    COALESCE(a.longitude_max, 0) AS longitude_max
  FROM grid g
  LEFT JOIN agg a ON a.device_id = g.device_id
                 AND a.hour_start = g.hour_start
)
INSERT INTO iot_personal_hub.agg_hourly_devices_smartphone_location_details (
  device_id, date_hour, 
  altitude_min, altitude_avg, altitude_max,
  latitude_min, latitude_avg, latitude_max,
  longitude_min, longitude_avg, longitude_max
)
SELECT 
  device_id, date_hour,
  altitude_min, altitude_avg, altitude_max,
  latitude_min, latitude_avg, latitude_max,
  longitude_min, longitude_avg, longitude_max
FROM final_rows
ON CONFLICT (device_id, date_hour) DO UPDATE
SET 
  altitude_min = EXCLUDED.altitude_min,
  altitude_avg = EXCLUDED.altitude_avg,
  altitude_max = EXCLUDED.altitude_max,
  latitude_min = EXCLUDED.latitude_min,
  latitude_avg = EXCLUDED.latitude_avg,
  latitude_max = EXCLUDED.latitude_max,
  longitude_min = EXCLUDED.longitude_min,
  longitude_avg = EXCLUDED.longitude_avg,
  longitude_max = EXCLUDED.longitude_max,
  updated_at = now();


