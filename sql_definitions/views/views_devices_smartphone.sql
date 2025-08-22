-- LOCATION - GIS STRICTED
create view iot_personal_hub.view_devices_smartphone_location_gis_stricted as 
with locations as (
	SELECT id,
	    device_id,
	    device_timestamp,
	    ST_SetSRID(st_point((properties #> '{location,longitude}'::text[])::double precision, (properties #> '{location,latitude}'::text[])::double precision), 4326) AS location
	FROM iot_personal_hub.raw_devices_properties dl
	where device_id = 1
	and to_timestamp(device_timestamp) >= (CURRENT_TIMESTAMP - interval '30 days')
)
select id, device_id, device_timestamp, location 
from locations
WHERE NOT EXISTS (
    SELECT 1 
    FROM iot_personal_hub.dim_blocked_areas p 
    WHERE ST_Within(locations.location, p.polygon)
);

-- BATTERY
create or replace view iot_personal_hub.view_devices_smartphone_battery_temperature as 
select
	device_id,
	to_char(agg.date_hour, 'YYYY-MM-DD HH24:00') as device_timestamp,
	agg.temperature_min, agg.temperature_avg, agg.temperature_max
from iot_personal_hub.agg_hourly_devices_smartphone_battery_details agg
where agg.date_hour >= (CURRENT_TIMESTAMP - interval '7 days');


create or replace view iot_personal_hub.view_devices_smartphone_battery_usage_current_mA as 
select
	device_id,
	to_char(agg.date_hour, 'YYYY-MM-DD HH24:00') as device_timestamp,
	agg.usage_current_mA_min, agg.usage_current_mA_avg, agg.usage_current_mA_max
from iot_personal_hub.agg_hourly_devices_smartphone_battery_details agg
where agg.date_hour >= (CURRENT_TIMESTAMP - interval '7 days');


create or replace view iot_personal_hub.view_devices_smartphone_battery_level as 
select
	device_id,
	to_char(agg.date_hour, 'YYYY-MM-DD HH24:00') as device_timestamp,
	agg.level_min, agg.level_avg, agg.level_max
from iot_personal_hub.agg_hourly_devices_smartphone_battery_details agg
where agg.date_hour >= (CURRENT_TIMESTAMP - interval '7 days');


-- LOCATION
create or replace view iot_personal_hub.view_devices_smartphone_location_altitude as 
select
	device_id,
	to_char(agg.date_hour, 'YYYY-MM-DD HH24:00') as device_timestamp,
	agg.altitude_min, agg.altitude_avg, agg.altitude_max
from iot_personal_hub.agg_hourly_devices_smartphone_location_details agg
where agg.date_hour >= (CURRENT_TIMESTAMP - interval '7 days');


-- EVENTS
create or replace view iot_personal_hub.view_devices_smartphone_events_counter as 
select
	device_id,
	to_char(agg.date_hour, 'YYYY-MM-DD HH24:00') as device_timestamp,
	agg.count_events
from iot_personal_hub.agg_hourly_devices_smartphone_events_counter agg
where agg.date_hour >= (CURRENT_TIMESTAMP - interval '7 days');