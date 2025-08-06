import streamlit as st
import pandas as pd
import numpy as np
from db_managment.DB_Client import DB_Client

st.title("IoT Dashboard")

db_client = DB_Client()
data = db_client.get_data_from_db()
db_client.close_db_client()


if data:
    df = pd.DataFrame(data, columns=['timestamp', 'value'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Wykres w Streamlit (bez matplotlib)
    tab1, tab2 = st.tabs(["Wykres", "Dane"])
    with tab1:
        st.subheader("Ilość wysłanych zdarzeń przez urządzenie")
        st.write("Wykres przedstawia ile zestwau danych zostało wysłanych w dniu i godzinie. Dane za ostatnie 7 dni")
        st.line_chart(df.set_index('timestamp')['value'])
        st.caption(f"Liczba pomiarów: {len(df)} | Zakres: {df['timestamp'].min()} - {df['timestamp'].max()}")
    with tab2:
        st.subheader("Dane tabelaryczne")
        st.dataframe(df)
