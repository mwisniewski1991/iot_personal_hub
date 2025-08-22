create view iot_personal_hub.view_device_locations_gis_stricted as 
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