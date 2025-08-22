
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
    count(dl.id) as count_events
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
    COALESCE(a.count_events, 0) AS count_events
  FROM grid g
  LEFT JOIN agg a ON a.device_id = g.device_id
                 AND a.hour_start = g.hour_start
)
INSERT INTO iot_personal_hub.agg_hourly_devices_smartphone_events_counter (
  device_id, date_hour, 
  count_events
)
SELECT 
  device_id, date_hour,
  count_events
FROM final_rows
ON CONFLICT (device_id, date_hour) DO UPDATE
SET 
  count_events = EXCLUDED.count_events,
  updated_at = now();


