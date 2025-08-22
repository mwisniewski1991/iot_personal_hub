CREATE TABLE iot_personal_hub.agg_hourly_devices_smartphone_location_details (
    device_id INT NOT NULL,
    date_hour timestamptz  NOT NULL,
    altitude_min FLOAT NOT NULL,
	altitude_avg FLOAT NOT NULL,
	altitude_max FLOAT NOT NULL,
	latitude_min FLOAT NOT NULL,
	latitude_avg FLOAT NOT NULL,
	latitude_max FLOAT NOT NULL,
	longitude_min FLOAT NOT NULL,
	longitude_avg FLOAT NOT NULL,
	longitude_max FLOAT NOT NULL,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    PRIMARY KEY (device_id, date_hour)
);


