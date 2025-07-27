CREATE TABLE device_locations (
    id SERIAL PRIMARY KEY,             
    device_id INT NOT NULL,
    device_timestamp BIGINT NOT NULL,
    properties JSONB,
    created_at_cest timestamp with time zone DEFAULT (current_timestamp AT TIME ZONE 'CEST')
);