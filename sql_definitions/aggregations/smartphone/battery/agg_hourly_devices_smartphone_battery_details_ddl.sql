CREATE TABLE iot_personal_hub.agg_hourly_devices_smartphone_battery_details (
    device_id INT NOT NULL,
    date_hour timestamptz  NOT NULL,
    temperature_min FLOAT NOT NULL,
	temperature_avg FLOAT NOT NULL,
	temperature_max FLOAT NOT NULL,
	level_min FLOAT NOT NULL,
	level_avg FLOAT NOT NULL,
	level_max FLOAT NOT NULL,
	usage_current_mA_min FLOAT NOT NULL,
	usage_current_mA_avg FLOAT NOT NULL,
	usage_current_mA_max FLOAT NOT NULL,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    PRIMARY KEY (device_id, date_hour)
);


