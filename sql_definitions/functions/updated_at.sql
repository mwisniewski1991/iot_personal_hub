CREATE FUNCTION set_current_timestampz_updated_at()
    RETURNS TRIGGER AS $$
DECLARE
_new record;
BEGIN
  _new := NEW;
  _new."updated_at" = now();
RETURN _new;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER TEMPLATE
CREATE TRIGGER {{trigger_name}}
    BEFORE UPDATE ON {{schema}}.{{table_name}}
    FOR EACH ROW
    EXECUTE PROCEDURE set_current_timestampz_updated_at();

-- TRIGGER FOR TABLES
CREATE TRIGGER trg_dim_devices_updated_at
    BEFORE UPDATE ON iot_personal_hub.dim_devices
    FOR EACH ROW
    EXECUTE PROCEDURE set_current_timestampz_updated_at();

CREATE TRIGGER trg_dim_blocked_areas_updated_at
    BEFORE UPDATE ON iot_personal_hub.dim_blocked_areas
    FOR EACH ROW
    EXECUTE PROCEDURE set_current_timestampz_updated_at();

CREATE TRIGGER trg_agg_hourly_devices_smartphone_battery_details_updated_at
    BEFORE UPDATE ON iot_personal_hub.agg_hourly_devices_smartphone_battery_details
    FOR EACH ROW
    EXECUTE PROCEDURE set_current_timestampz_updated_at();

CREATE TRIGGER trg_agg_hourly_devices_smartphone_location_details_updated_at
    BEFORE UPDATE ON iot_personal_hub.agg_hourly_devices_smartphone_location_details
    FOR EACH ROW
    EXECUTE PROCEDURE set_current_timestampz_updated_at();

CREATE TRIGGER trg_agg_hourly_devices_smartphone_events_counter_updated_at
    BEFORE UPDATE ON iot_personal_hub.agg_hourly_devices_smartphone_events_counter
    FOR EACH ROW
    EXECUTE PROCEDURE set_current_timestampz_updated_at();

