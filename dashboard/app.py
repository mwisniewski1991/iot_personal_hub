import streamlit as st
import pandas as pd
import src.charts as charts 
from db_managment.DB_Client import DB_Client

st.set_page_config(layout="wide", page_title="IoT Personal Hub", page_icon="src/static/favicon.ico")

st.title("IoT Dashboard")
st.caption("System monitorowania urządzeń IoT - dane w czasie rzeczywistym")

db_client = DB_Client()
devices_events_counter = db_client.get_devices_events_counter()
devices_locations = db_client.get_devices_locations()
devices_location_altitude_m = db_client.get_devices_location_altitude_m()
devices_battery_level = db_client.get_devices_battery_level()
devices_battery_temperature = db_client.get_devices_battery_temperature()
devices_battery_usage_current_mA = db_client.get_devices_battery_usage_current_mA()
devices_battery_usage_current_average_mA = db_client.get_devices_battery_usage_current_average_mA()
db_client.close_db_client()


if devices_events_counter:
    df_devices_events_counter = pd.DataFrame(devices_events_counter, columns=['date', 'count_events'])
    df_devices_events_counter['date'] = pd.to_datetime(df_devices_events_counter['date'])
    charts.create_chart_devices_events_counter(df_devices_events_counter)

col5, col6 = st.columns(2)
with col5:
    if devices_locations:
        df_devices_locations = pd.DataFrame(devices_locations, columns=['latitude', 'longitude'])
        charts.create_chart_devices_location_latitude_longitude_osm(df_devices_locations)

with col6:
    if devices_location_altitude_m:
        df_devices_location_altitude_m = pd.DataFrame(devices_location_altitude_m, columns=['device_timestamp', 'altitude_m'])
        df_devices_location_altitude_m['device_timestamp'] = pd.to_datetime(df_devices_location_altitude_m['device_timestamp'])
        charts.create_chart_devices_location_altitude_m(df_devices_location_altitude_m)

col1, col2 = st.columns(2)
with col1:
    if devices_battery_level:
        df_devices_battery_level = pd.DataFrame(devices_battery_level, columns=['device_timestamp', 'level_min', 'level_avg', 'level_max'])
        df_devices_battery_level['device_timestamp'] = pd.to_datetime(df_devices_battery_level['device_timestamp'])
        charts.create_chart_devices_battery_level(df_devices_battery_level)

with col2:  
    if devices_battery_temperature:
        df_devices_battery_temperature = pd.DataFrame(devices_battery_temperature, columns=['device_timestamp', 'temperature_min', 'temperature_avg', 'temperature_max'])
        df_devices_battery_temperature['device_timestamp'] = pd.to_datetime(df_devices_battery_temperature['device_timestamp'])
        charts.create_chart_devices_battery_temperature(df_devices_battery_temperature)

col3, col4 = st.columns(2)
with col3:
    if devices_battery_usage_current_mA:
        df_devices_battery_usage_current_mA = pd.DataFrame(devices_battery_usage_current_mA, columns=['device_timestamp', 'usage_current_mA_min', 'usage_current_mA_avg', 'usage_current_mA_max'])
        df_devices_battery_usage_current_mA['device_timestamp'] = pd.to_datetime(df_devices_battery_usage_current_mA['device_timestamp'])
        charts.create_chart_devices_battery_usage_current_mA(df_devices_battery_usage_current_mA)

with col4:
    pass
