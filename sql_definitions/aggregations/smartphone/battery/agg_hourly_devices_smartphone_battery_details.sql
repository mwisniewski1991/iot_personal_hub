
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
    round(min((dl.properties #> '{battery, temperature_C}')::INTEGER),2) as temperature_min,
    round(avg((dl.properties #> '{battery, temperature_C}')::INTEGER),2) as temperature_avg,
    round(max((dl.properties #> '{battery, temperature_C}')::INTEGER),2) as temperature_max,
    round(min((dl.properties #> '{battery, remaining_percent}')::INTEGER),2) as level_min,
    round(avg((dl.properties #> '{battery, remaining_percent}')::INTEGER),2) as level_avg,
    round(max((dl.properties #> '{battery, remaining_percent}')::INTEGER),2) as level_max,
    round(min((dl.properties #> '{battery, usage_current_mA}')::INTEGER),2) as usage_current_mA_min,
    round(avg((dl.properties #> '{battery, usage_current_mA}')::INTEGER),2) as usage_current_mA_avg,
    round(max((dl.properties #> '{battery, usage_current_mA}')::INTEGER),2) as usage_current_mA_max 
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
    COALESCE(a.temperature_min, 0) AS temperature_min,
    COALESCE(a.temperature_avg, 0) AS temperature_avg,
    COALESCE(a.temperature_max, 0) AS temperature_max,
    COALESCE(a.level_min, 0) AS level_min,
    COALESCE(a.level_avg, 0) AS level_avg,
    COALESCE(a.level_max, 0) AS level_max,
    COALESCE(a.usage_current_mA_min, 0) AS usage_current_mA_min,
    COALESCE(a.usage_current_mA_avg, 0) AS usage_current_mA_avg,
    COALESCE(a.usage_current_mA_max, 0) AS usage_current_mA_max
  FROM grid g
  LEFT JOIN agg a ON a.device_id = g.device_id
                 AND a.hour_start = g.hour_start
)
INSERT INTO iot_personal_hub.agg_hourly_devices_smartphone_battery_details (
  device_id, date_hour, 
  temperature_min, temperature_avg, temperature_max,
  level_min, level_avg, level_max,
  usage_current_mA_min, usage_current_mA_avg, usage_current_mA_max
)
SELECT 
  device_id, date_hour,
  temperature_min, temperature_avg, temperature_max,
  level_min, level_avg, level_max,
  usage_current_mA_min, usage_current_mA_avg, usage_current_mA_max
FROM final_rows
ON CONFLICT (device_id, date_hour) DO UPDATE
SET 
  temperature_min = EXCLUDED.temperature_min,
  temperature_avg = EXCLUDED.temperature_avg,
  temperature_max = EXCLUDED.temperature_max,
  level_min = EXCLUDED.level_min,
  level_avg = EXCLUDED.level_avg,
  level_max = EXCLUDED.level_max,
  usage_current_mA_min = EXCLUDED.usage_current_mA_min,
  usage_current_mA_avg = EXCLUDED.usage_current_mA_avg,
  usage_current_mA_max = EXCLUDED.usage_current_mA_max,
  updated_at = now();


