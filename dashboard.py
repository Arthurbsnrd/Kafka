import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

st.title("Dashboard météo global")

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath) as f:
            return pd.DataFrame(json.load(f))
    else:
        st.warning(f"Fichier non trouvé : {filepath}")
        return pd.DataFrame()

st.header("Profils saisonniers (historique)")

seasonal_profile_path = "./alerts_data/seasonal_profile.json"
seasonal_profile_df = load_json(seasonal_profile_path)

if not seasonal_profile_df.empty:
    st.write(seasonal_profile_df.head())

    fig, ax = plt.subplots()
    for city in seasonal_profile_df.city.unique():
        city_data = seasonal_profile_df[seasonal_profile_df.city == city]
        ax.plot(city_data["month"], city_data["temperature_month_avg"], label=f"Température {city}")
    ax.set_xlabel("Mois")
    ax.set_ylabel("Température moyenne")
    ax.legend()
    st.pyplot(fig)
else:
    st.info("Données saisonnières non disponibles.")

st.header("Données temps réel")

realtime_example = {
    "event_time": "2025-09-23T15:00:00",
    "city": "Paris",
    "country": "France",
    "temperature": 30,
    "windspeed": 20,
    "wind_alert_level": "level_2"
}
st.json(realtime_example)

st.header("Anomalies détectées")

anomalies_path = "./hdfs-data/France/Paris/anomalies/2025/09/anomalies_20250923T150000.json"
anomalies_df = load_json(anomalies_path)

if not anomalies_df.empty:
    st.write(anomalies_df)
else:
    st.info("Pas d'anomalies détectées ou fichier non trouvé.")

st.header("Comparaison historique vs temps réel")

if not seasonal_profile_df.empty:
    city = realtime_example["city"]
    month = pd.to_datetime(realtime_example["event_time"]).month
    hist_row = seasonal_profile_df[(seasonal_profile_df.city == city) & (seasonal_profile_df.month == month)]
    if not hist_row.empty:
        st.write(f"Profil historique pour {city}, mois {month}")
        st.write(hist_row)
    else:
        st.info("Pas de profil historique pour ce mois.")
else:
    st.info("Pas de données saisonnières pour comparaison.")
