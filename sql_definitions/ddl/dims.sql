create table iot_personal_hub.dim_devices (
    id int not null primary key,
    name varchar(255) not null,
    type varchar(255) not null references iot_personal_hub.enum_device_type(value) on update restrict on delete restrict,
    status varchar(255) not null,
    details jsonb not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);


CREATE TABLE iot_personal_hub.dim_blocked_areas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    polygon GEOMETRY(POLYGON, 4326),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);
