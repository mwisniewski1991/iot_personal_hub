import streamlit as st
import pandas as pd
import numpy as np
from db_managment.DB_Client import DB_Client

st.title("IoT Dashboard")
st.caption("System monitorowania urządzeń IoT - dane w czasie rzeczywistym")

db_client = DB_Client()
data = db_client.get_data_from_db()
devices_locations = db_client.get_devices_locations()
devices_battery_level = db_client.get_devices_battery_level()
devices_temperature = db_client.get_devices_temperature()
db_client.close_db_client()


if data:
    df = pd.DataFrame(data, columns=['timestamp', 'value'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Wykres w Streamlit (bez matplotlib)
    tab1, tab2 = st.tabs(["Wykres", "Dane"])
    with tab1:
        st.subheader("Ilość wysłanych zdarzeń przez urządzenie")
        st.write("Wykres przedstawia ile zestawów danych zostało wysłanych w dniu i godzinie. Dane za ostatnie 7 dni")
        st.line_chart(df.set_index('timestamp')['value'], x_label="Data godzina", y_label="Ilość wysłanych zdarzeń")
        # st.vega_lite_chart(df, {
        #     "mark": "line",
        #     "encoding": {
        #         "x": {"field": "timestamp", "type": "temporal", "title":"Data"},
        #         "y": {"field": "value", "type": "quantitative", "title":"Ilość wysłanych zdarzeń"}
        #     },
        #     "width": 700,
        #     "height": 400
        # })
        st.caption(f"Liczba pomiarów: {len(df)} | Zakres: {df['timestamp'].min()} - {df['timestamp'].max()}")
    with tab2:
        st.subheader("Dane tabelaryczne")
        st.dataframe(df)

if devices_locations:
    df_devices_locations = pd.DataFrame(devices_locations, columns=['latitude', 'longitude'])
    st.subheader("Lokalizacja urządzenia")
    st.write("Mapa przedstawia zarejestrowane loklizacje.")
    st.vega_lite_chart(df_devices_locations, {
        "mark": {"type": "circle", "size": 20, "color": "red"},
        "encoding": {
            "longitude": {"field": "longitude", "type": "quantitative"},
            "latitude": {"field": "latitude", "type": "quantitative"}
        },
        "projection": {"type": "mercator"},
        "width": 700,
        "height": 400
    })


col1, col2 = st.columns(2)
with col1:
    if devices_battery_level:
        df_devices_battery_level = pd.DataFrame(devices_battery_level, columns=['device_timestamp', 'battery'])
        st.subheader("Poziom baterii urządzenia")
        st.line_chart(df_devices_battery_level.set_index('device_timestamp')['battery'], x_label="Data godzina", y_label="Poziom baterii")
        
with col2:
    if devices_temperature:
        df_devices_temperature = pd.DataFrame(devices_temperature, columns=['device_timestamp', 'temperature'])
        st.subheader("Temperatura urządzenia")
        st.line_chart(df_devices_temperature.set_index('device_timestamp')['temperature'], x_label="Data godzina", y_label="Temperatura")