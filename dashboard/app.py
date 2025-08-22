import streamlit as st
import pandas as pd
import src.charts as charts 
import src.maps as maps
from db_managment.DB_Client import DB_Client

st.set_page_config(layout="wide", page_title="IoT Personal Hub", page_icon="src/static/favicon.ico")

st.title("IoT Dashboard")
st.caption("System monitorowania urządzeń IoT - dane w czasie rzeczywistym")

db_client = DB_Client()
devices_locations = db_client.get_devices_locations()
devices_smartphone_events_counter = db_client.get_devices_smartphone_events_counter()   
devices_location_altitude_m = db_client.get_devices_location_altitude_m()
devices_smartphone_battery_level = db_client.get_devices_smartphone_battery_level()
devices_smartphone_battery_temperature = db_client.get_devices_smartphone_battery_temperature()
devices_smartphone_battery_usage_current_mA = db_client.get_devices_smartphone_battery_usage_current_mA()
db_client.close_db_client()


col1, col2 = st.columns(2)
with col1:
    if devices_smartphone_events_counter:
        df_devices_smartphone_events_counter = pd.DataFrame(devices_smartphone_events_counter, columns=['device_timestamp', 'count_events'])
        df_devices_smartphone_events_counter['device_timestamp'] = pd.to_datetime(df_devices_smartphone_events_counter['device_timestamp'])
        charts.create_chart_devices_smartphone_events_counter(df_devices_smartphone_events_counter)

with col2:
    if devices_locations:
        df_devices_locations = pd.DataFrame(devices_locations, columns=['latitude', 'longitude'])
        maps.create_chart_devices_location_latitude_longitude_osm(df_devices_locations)


col3, col4 = st.columns(2)
with col3:
    pass
    if devices_location_altitude_m:
        df_devices_location_altitude_m = pd.DataFrame(devices_location_altitude_m, columns=['device_timestamp', 'altitude_min', 'altitude_avg', 'altitude_max'])
        df_devices_location_altitude_m['device_timestamp'] = pd.to_datetime(df_devices_location_altitude_m['device_timestamp'])
        charts.create_chart_devices_location_altitude_m(df_devices_location_altitude_m)
    else:
        st.write("Brak danych o wysokości urządzeń")    

with col4:  
    if devices_smartphone_battery_level:
        df_devices_smartphone_battery_level = pd.DataFrame(devices_smartphone_battery_level, columns=['device_timestamp', 'level_min', 'level_avg', 'level_max'])
        df_devices_smartphone_battery_level['device_timestamp'] = pd.to_datetime(df_devices_smartphone_battery_level['device_timestamp'])
        charts.create_chart_devices_smartphone_battery_level(df_devices_smartphone_battery_level)
    else:
        st.write("Brak danych o poziomie baterii urządzeń")
   
col5, col6 = st.columns(2)
with col5:
    if devices_smartphone_battery_temperature:
        df_devices_smartphone_battery_temperature = pd.DataFrame(devices_smartphone_battery_temperature, columns=['device_timestamp', 'temperature_min', 'temperature_avg', 'temperature_max'])
        df_devices_smartphone_battery_temperature['device_timestamp'] = pd.to_datetime(df_devices_smartphone_battery_temperature['device_timestamp'])
        charts.create_chart_devices_smartphone_battery_temperature(df_devices_smartphone_battery_temperature)
    else:
        st.write("Brak danych o temperaturze baterii urządzeń")

with col6:
    if devices_smartphone_battery_usage_current_mA:
        df_devices_smartphone_battery_usage_current_mA = pd.DataFrame(devices_smartphone_battery_usage_current_mA, columns=['device_timestamp', 'usage_current_mA_min', 'usage_current_mA_avg', 'usage_current_mA_max'])
        df_devices_smartphone_battery_usage_current_mA['device_timestamp'] = pd.to_datetime(df_devices_smartphone_battery_usage_current_mA['device_timestamp'])
        charts.create_chart_devices_smartphone_battery_usage_current_mA(df_devices_smartphone_battery_usage_current_mA)
    else:
        st.write("Brak danych o zużyciu prądu baterii urządzeń")
