from pathlib import Path

import pandas as pd
import streamlit as st


CITY_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "cities.csv"
)


@st.cache_data
def get_cities():

    cities = pd.read_csv(CITY_FILE)

    cities = cities.sort_values(
        by=["State", "City"]
    )

    return cities


def get_city_names():

    cities = get_cities()

    return cities["City"].tolist()


def get_city_details(city_name):

    cities = get_cities()

    result = cities[
        cities["City"] == city_name
    ]

    if result.empty:
        return None

    row = result.iloc[0]

    return {
        "city": row["City"],
        "state": row["State"],
        "latitude": float(row["Latitude"]),
        "longitude": float(row["Longitude"]),
    }