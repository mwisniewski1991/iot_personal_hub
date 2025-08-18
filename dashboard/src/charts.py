import streamlit as st
from pandas import Timestamp

def create_chart_devices_events_counter(data):
    st.subheader("Ilość wysłanych zdarzeń przez smartphone")
    st.write("Wykres przedstawia ile zestawów danych zostało wysłanych w dniu i godzinie. Dane za ostatnie 7 dni")

    tab1, tab2 = st.tabs(["Wykres", "Dane"])
    with tab1:
        unique_days = data['date'].dt.date.unique()
        day_starts = [Timestamp(day) for day in unique_days]

        st.vega_lite_chart(data, {
            "layer": [
                {
                    "mark": "line",
                    "encoding": {
                        "x": {
                            "field": "date", 
                            "type": "temporal", 
                            "title": "Data godzina",
                            "axis": {
                                "format": "%d.%m %H:00"
                            }
                        },
                        "y": {"field": "count_events", "type": "quantitative", "title": "Ilość wysłanych zdarzeń"}
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
        st.caption(f"Liczba pomiarów: {len(data)} | Zakres: {data['date'].min()} - {data['date'].max()}")
    with tab2:
        st.subheader("Dane tabelaryczne")
        st.dataframe(data)

def create_chart_devices_location_altitude_m(data):
    st.subheader("Wysokość urządzenia nad poziomem morza")
    

    unique_days = data['device_timestamp'].dt.date.unique()
    day_starts = [Timestamp(day) for day in unique_days]
    
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
    
    tab1, tab2 = st.tabs(["Wykres", "Legenda"])
    
    with tab1:
        st.vega_lite_chart(data, chart_spec)
        st.caption(f"Liczba pomiarów: {len(data)} | Zakres: {data['device_timestamp'].min()} - {data['device_timestamp'].max()}")
    
    with tab2:
        st.markdown("""
        Dane za ostatnie 7 dni:  
        🔵 **Niebieska linia ciągła** - Wysokość urządzenia nad poziomem morza  
        ⚪ **Białe linie pionowe** - Początek doby  
        """)

def create_chart_devices_battery_level(data):
    st.subheader("Poziom baterii urządzenia")

    unique_days = data['device_timestamp'].dt.date.unique()
    day_starts = [Timestamp(day) for day in unique_days]

    chart_spec = {
            "layer": [
                { # Avg
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
                        "y": {"field": "level_avg", "type": "quantitative", "title": "Poziom baterii"}
                    }
                },
                { # Min
                    "mark": {"type": "line", "color": "green", "strokeDash": [4, 4]},
                    "encoding": {
                        "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                        "y": {"field": "level_min", "type": "quantitative", "title": "Poziom baterii"}
                    }
                },
                { # Max
                    "mark": {"type": "line", "color": "red", "strokeDash": [4, 4]},
                    "encoding": {
                        "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                        "y": {"field": "level_max", "type": "quantitative", "title": "Poziom baterii"}
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
    
    tab1, tab2 = st.tabs(["Wykres", "Legenda"])
    
    with tab1:
        st.vega_lite_chart(data, chart_spec)
        st.caption(f"Liczba pomiarów: {len(data)} | Zakres: {data['device_timestamp'].min()} - {data['device_timestamp'].max()}")
    
    with tab2:
        st.markdown("""
        Dane za ostatnie 7 dni:  
        🔵 **Niebieska linia ciągła** - Średni poziom baterii w godzinie  
        🟢 **Zielona linia przerywana** - Minimalny poziom baterii w godzinie  
        🔴 **Czerwona linia przerywana** - Maksymalny poziom baterii w godzinie  
        ⚪ **Białe linie pionowe** - Początek doby  
        """)

def create_chart_devices_battery_temperature(data):
    st.subheader("Temperatura urządzenia")
    

    unique_days = data['device_timestamp'].dt.date.unique()
    day_starts = [Timestamp(day) for day in unique_days]
    
    chart_spec = {
        "layer": [
            { # Avg
                "mark": "line",
                "encoding": {
                    "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                    "y": {"field": "temperature_avg", "type": "quantitative", "title": "Temperatura"}
                }
            },
            { # Min
                "mark": {"type": "line", "color": "green", "strokeDash": [4, 4]},
                "encoding": {
                    "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                    "y": {"field": "temperature_min", "type": "quantitative", "title": "Temperatura"}
                }
            },
            { # Max
                "mark": {"type": "line", "color": "red", "strokeDash": [4, 4]},
                "encoding": {
                    "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                    "y": {"field": "temperature_max", "type": "quantitative", "title": "Temperatura"}
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
    
    tab1, tab2 = st.tabs(["Wykres", "Legenda"])
    
    with tab1:
        st.vega_lite_chart(data, chart_spec)
        st.caption(f"Liczba pomiarów: {len(data)} | Zakres: {data['device_timestamp'].min()} - {data['device_timestamp'].max()}")
    
    with tab2:
        st.markdown("""
        Dane za ostatnie 7 dni:  
        🔵 **Niebieska linia ciągła** - Średnia temperatura w godzinie  
        🟢 **Zielona linia przerywana** - Minimalna temperatura w godzinie  
        🔴 **Czerwona linia przerywana** - Maksymalna temperatura w godzinie  
        ⚪ **Białe linie pionowe** - Początek doby  
        """)

def create_devices_battery_usage_current_average_mA(data):
    st.subheader("Średni prąd urządzenia")
    
    unique_days = data['device_timestamp'].dt.date.unique()
    day_starts = [Timestamp(day) for day in unique_days]
    
    chart_spec = {
        "layer": [
            { # Avg
                "mark": "line",
                "encoding": {
                    "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                    "y": {"field": "usage_current_average_mA_avg", "type": "quantitative", "title": "Średni prąd"}
                }
            },
            { # Min
                "mark": {"type": "line", "color": "green", "strokeDash": [4, 4]},
                "encoding": {
                    "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                    "y": {"field": "usage_current_average_mA_min", "type": "quantitative", "title": "Średni prąd"}
                }
            },
            { # Max
                "mark": {"type": "line", "color": "red", "strokeDash": [4, 4]},
                "encoding": {
                    "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                    "y": {"field": "usage_current_average_mA_max", "type": "quantitative", "title": "Średni prąd"}
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
    
    tab1, tab2 = st.tabs(["Wykres", "Legenda"])
    
    with tab1:
        st.vega_lite_chart(data, chart_spec)
        st.caption(f"Liczba pomiarów: {len(data)} | Zakres: {data['device_timestamp'].min()} - {data['device_timestamp'].max()}")
    
    with tab2:
        st.markdown("""
        Dane za ostatnie 7 dni:  
        🔵 **Niebieska linia ciągła** - Średni prąd (średnia) w godzinie  
        🟢 **Zielona linia przerywana** - Minimalny średni prąd w godzinie  
        🔴 **Czerwona linia przerywana** - Maksymalny średni prąd w godzinie  
        ⚪ **Białe linie pionowe** - Początek doby  
        """)

def create_chart_devices_battery_usage_current_mA(data):
    st.subheader("Prąd pobierany przez urządzenie")
    

    unique_days = data['device_timestamp'].dt.date.unique()
    day_starts = [Timestamp(day) for day in unique_days]

    
    chart_spec = {
        "layer": [
            { # Avg
                "mark": "line",
                "encoding": {
                    "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                    "y": {"field": "usage_current_mA_avg", "type": "quantitative", "title": "Prąd"}
                }
            },
            { # Min
                "mark": {"type": "line", "color": "green", "strokeDash": [4, 4]},
                "encoding": {   
                    "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                    "y": {"field": "usage_current_mA_min", "type": "quantitative", "title": "Prąd"}
                }
            },
            { # Max
                "mark": {"type": "line", "color": "red", "strokeDash": [4, 4]},
                "encoding": {
                    "x": {"field": "device_timestamp", "type": "temporal", "title": "Data godzina", "axis": {"format": "%d.%m %H:00"}},
                    "y": {"field": "usage_current_mA_max", "type": "quantitative", "title": "Prąd"}
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
    
    tab1, tab2 = st.tabs(["Wykres", "Legenda"])
    
    with tab1:
        st.vega_lite_chart(data, chart_spec)
        st.caption(f"Liczba pomiarów: {len(data)} | Zakres: {data['device_timestamp'].min()} - {data['device_timestamp'].max()}")
    
    with tab2:
        st.markdown("""
        Dane za ostatnie 7 dni:  
        🔵 **Niebieska linia ciągła** - Średni prąd pobierany w godzinie  
        🟢 **Zielona linia przerywana** - Minimalny prąd pobierany w godzinie  
        🔴 **Czerwona linia przerywana** - Maksymalny prąd pobierany w godzinie  
        ⚪ **Białe linie pionowe** - Początek doby  
        """)
