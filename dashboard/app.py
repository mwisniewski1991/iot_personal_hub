import streamlit as st
import pandas as pd
import numpy as np
from db_managment.DB_Client import DB_Client

st.set_page_config(layout="wide")

st.title("IoT Dashboard")
st.caption("System monitorowania urządzeń IoT - dane w czasie rzeczywistym")

db_client = DB_Client()
data = db_client.get_data_from_db()
devices_locations = db_client.get_devices_locations()
devices_battery_level = db_client.get_devices_battery_level()
devices_battery_temperature = db_client.get_devices_battery_temperature()
devices_battery_usage_current_mA = db_client.get_devices_battery_usage_current_mA()
devices_battery_usage_current_average_mA = db_client.get_devices_battery_usage_current_average_mA()
devices_location_altitude_m = db_client.get_devices_location_altitude_m()
db_client.close_db_client()


if data:
    df = pd.DataFrame(data, columns=['timestamp', 'value'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Wykres w Streamlit (bez matplotlib)
    tab1, tab2 = st.tabs(["Wykres", "Dane"])
    with tab1:
        st.subheader("Ilość wysłanych zdarzeń przez urządzenie")
        st.write("Wykres przedstawia ile zestawów danych zostało wysłanych w dniu i godzinie. Dane za ostatnie 7 dni")
        # Znajdź początek każdej doby dla pierwszego wykresu
        unique_days = df['timestamp'].dt.date.unique()
        day_starts = [pd.Timestamp(day) for day in unique_days]

        st.vega_lite_chart(df, {
            "layer": [
                {
                    "mark": "line",
                    "encoding": {
                        "x": {
                            "field": "timestamp", 
                            "type": "temporal", 
                            "title": "Data",
                            "axis": {
                                "format": "%d.%m %H:00"
                            }
                        },
                        "y": {"field": "value", "type": "quantitative", "title": "Ilość wysłanych zdarzeń"}
                    }
                },
                {
                    "mark": {"type": "rule", "color": "white", "strokeDash": [4, 4]},
                    "encoding": {
                        "x": {"field": "day_start", "type": "temporal"}
                    },
                    "data": {"values": [{"day_start": str(day)} for day in day_starts]}
                }
            ],
            "resolve": {"scale": {"color": "independent"}},
            "width": 700,
            "height": 400
        })
        st.caption(f"Liczba pomiarów: {len(df)} | Zakres: {df['timestamp'].min()} - {df['timestamp'].max()}")
    with tab2:
        st.subheader("Dane tabelaryczne")
        st.dataframe(df)

col1, col2 = st.columns(2)
with col1:
    if devices_battery_level:
        df_devices_battery_level = pd.DataFrame(devices_battery_level, columns=['device_timestamp', 'battery'])
        df_devices_battery_level['device_timestamp'] = pd.to_datetime(df_devices_battery_level['device_timestamp'])
        
        # Znajdź początek każdej doby
        unique_days = df_devices_battery_level['device_timestamp'].dt.date.unique()
        day_starts = [pd.Timestamp(day) for day in unique_days]
        
        st.subheader("Poziom baterii urządzenia")
        st.write("Pionowa linia oznacza początek doby")
        # Użyj vega-lite dla większej kontroli
        chart_spec = {
            "layer": [
                {
                    "mark": "line",
                    "encoding": {
                        "x": {
                            "field": "device_timestamp", 
                            "type": "temporal", 
                            "title": "Data godzina",
                            "axis": {
                                "format": "%d.%m %H:00"
                            }
                        },
                        "y": {"field": "battery", "type": "quantitative", "title": "Poziom baterii"}
                    }
                },
                {
                    "mark": {"type": "rule", "color": "white", "strokeDash": [4, 4]},
                    "encoding": {
                        "x": {"field": "day_start", "type": "temporal"}
                    },
                    "data": {"values": [{"day_start": str(day)} for day in day_starts]}
                }
            ],
            "resolve": {"scale": {"color": "independent"}},
            "width": 400,
            "height": 300
        }
        
        st.vega_lite_chart(df_devices_battery_level, chart_spec)
        
with col2:  
    if devices_battery_temperature:
        df_devices_battery_temperature = pd.DataFrame(devices_battery_temperature, columns=['device_timestamp', 'battery_temperature'])
        df_devices_battery_temperature['device_timestamp'] = pd.to_datetime(df_devices_battery_temperature['device_timestamp'])
        
        # Znajdź początek każdej doby
        unique_days = df_devices_battery_temperature['device_timestamp'].dt.date.unique()
        day_starts = [pd.Timestamp(day) for day in unique_days]
        
        st.subheader("Temperatura urządzenia")
        st.write("Pionowa linia oznacza początek doby")
        
        chart_spec = {
            "layer": [
                {
                    "mark": "line",
                    "encoding": {
                        "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                        "y": {"field": "battery_temperature", "type": "quantitative", "title": "Temperatura"}
                    }
                },
                {
                    "mark": {"type": "rule", "color": "white", "strokeDash": [4, 4]},
                    "encoding": {
                        "x": {"field": "day_start", "type": "temporal"}
                    },
                    "data": {"values": [{"day_start": str(day)} for day in day_starts]}
                }
            ],
            "resolve": {"scale": {"color": "independent"}},
            "width": 400,
            "height": 300
        }
        
        st.vega_lite_chart(df_devices_battery_temperature, chart_spec)

col3, col4 = st.columns(2)
with col3:
    if devices_battery_usage_current_mA:
        df_devices_battery_usage_current_mA = pd.DataFrame(devices_battery_usage_current_mA, columns=['device_timestamp', 'battery_usage_current_mA'])
        df_devices_battery_usage_current_mA['device_timestamp'] = pd.to_datetime(df_devices_battery_usage_current_mA['device_timestamp'])
        st.subheader("Prąd urządzenia")
        st.write("Pionowa linia oznacza początek doby")
        chart_spec = {
            "layer": [
                {
                    "mark": "line",
                    "encoding": {
                        "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                        "y": {"field": "battery_usage_current_mA", "type": "quantitative", "title": "Prąd"}
                    }
                },
                {
                    "mark": {"type": "rule", "color": "white", "strokeDash": [4, 4]},
                    "encoding": {
                        "x": {"field": "day_start", "type": "temporal"}
                    },
                    "data": {"values": [{"day_start": str(day)} for day in day_starts]}
                }
            ],
            "resolve": {"scale": {"color": "independent"}},
            "width": 400,
            "height": 300
        }
        st.vega_lite_chart(df_devices_battery_usage_current_mA, chart_spec)

with col4:
    if devices_battery_usage_current_average_mA:
        df_devices_battery_usage_current_average_mA = pd.DataFrame(devices_battery_usage_current_average_mA, columns=['device_timestamp', 'battery_usage_current_average_mA'])
        df_devices_battery_usage_current_average_mA['device_timestamp'] = pd.to_datetime(df_devices_battery_usage_current_average_mA['device_timestamp'])
        st.subheader("Średni prąd urządzenia")
        st.write("Pionowa linia oznacza początek doby")
        chart_spec = {
            "layer": [
                {
                    "mark": "line",
                    "encoding": {
                        "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                        "y": {"field": "battery_usage_current_average_mA", "type": "quantitative", "title": "Średni prąd"}
                    }
                },
                {
                    "mark": {"type": "rule", "color": "white", "strokeDash": [4, 4]},
                    "encoding": {
                        "x": {"field": "day_start", "type": "temporal"}
                    },
                    "data": {"values": [{"day_start": str(day)} for day in day_starts]}
                }
            ],
            "resolve": {"scale": {"color": "independent"}},
            "width": 400,
            "height": 300
        }
        st.vega_lite_chart(df_devices_battery_usage_current_average_mA, chart_spec)

col5, col6 = st.columns(2)
with col5:
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
with col6:
    if devices_location_altitude_m:
        df_devices_location_altitude_m = pd.DataFrame(devices_location_altitude_m, columns=['device_timestamp', 'altitude_m'])
        df_devices_location_altitude_m['device_timestamp'] = pd.to_datetime(df_devices_location_altitude_m['device_timestamp'])
        st.subheader("Wysokość urządzenia")
        st.write("Pionowa linia oznacza początek doby")
        chart_spec = {
            "layer": [
                {
                    "mark": "line",
                    "encoding": {
                        "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                        "y": {"field": "altitude_m", "type": "quantitative", "title": "Wysokość"}
                    }
                },
                {
                    "mark": {"type": "rule", "color": "white", "strokeDash": [4, 4]},
                    "encoding": {
                        "x": {"field": "day_start", "type": "temporal"}
                    },
                    "data": {"values": [{"day_start": str(day)} for day in day_starts]}
                }
            ],
            "resolve": {"scale": {"color": "independent"}},
            "width": 400,
            "height": 300
        }
        st.vega_lite_chart(df_devices_location_altitude_m, chart_spec)