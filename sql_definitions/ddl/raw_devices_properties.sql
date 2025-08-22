CREATE TABLE iot_personal_hub.raw_devices_properties (
    id SERIAL PRIMARY KEY,             
    device_id INT NOT NULL,
    device_timestamp BIGINT NOT NULL,
    properties JSONB,
    created_at_cest timestamptz not null default now()
);