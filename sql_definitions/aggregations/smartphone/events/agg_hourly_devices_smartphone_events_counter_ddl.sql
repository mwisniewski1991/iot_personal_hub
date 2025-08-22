CREATE TABLE iot_personal_hub.agg_hourly_devices_smartphone_events_counter (
    device_id INT NOT NULL,
    date_hour timestamptz  NOT NULL,
    count_events INT NOT NULL,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    PRIMARY KEY (device_id, date_hour)
);


