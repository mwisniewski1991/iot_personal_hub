import json
import os
import streamlit as st

def _read_geojson():  
    # Wczytaj dane GeoJSON
    geojson_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'powiaty-medium.geojson')
    try:
        with open(geojson_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        st.warning("Nie znaleziono pliku powiaty-medium.geojson")
        geojson_data = None
    return geojson_data['features']

def create_chart_devices_location_latitude_longitude(data): 
    geojson_data = _read_geojson()

    st.subheader("Lokalizacja urządzenia")
    st.write("Mapa przedstawia zarejestrowane loklizacje.")

    chart_spec = {
        "layer": [
            # Warstwa GeoJSON (granice powiatów)
            # {
            #     "data": {
            #         "values": geojson_data,
            #         "format": {"type": "topojson", "feature": "collection"}
            #     } if geojson_data else {"values": []},
            #     "mark": {
            #         "type": "geoshape",
            #         "fill": "lightgray",
            #         "stroke": "white",
            #         "strokeWidth": 0.5,
            #         "opacity": 0.3
            #     }
            # },
            # Warstwa punktów (lokalizacje urządzeń)
            {
                "data": {"values": data.to_dict('records')},
                "mark": {"type": "circle", "size": 60, "color": "red", "opacity": 0.8},
                "encoding": {
                    "longitude": {"field": "longitude", "type": "quantitative"},
                    "latitude": {"field": "latitude", "type": "quantitative"},
                    "tooltip": [
                        {"field": "longitude", "type": "quantitative"},
                        {"field": "latitude", "type": "quantitative"}
                    ]
                }
            }
        ],
        "projection": {"type": "mercator"},
        "resolve": {"scale": {"color": "independent"}},
        "width": 700,
        "height": 400
    }
    st.vega_lite_chart(chart_spec, use_container_width=True)

def create_chart_devices_location_latitude_longitude_osm(data): 

    st.subheader("Lokalizacja urządzenia")
    st.write("Mapa przedstawia zarejestrowane lokalizacje.")

    st.map(data, latitude='latitude', longitude='longitude', size=6, color='#ff0000')