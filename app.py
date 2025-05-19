import streamlit as st
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

# Кешування для оптимізації
@st.cache_data
def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(place_name)
    return (location.latitude, location.longitude) if location else None

# Категорії та кольори точок
districts = ["Івано-Франківський район", "Калуський район", "Коломийський район", "Надвірнянський район"]
categories = ["A", "B", "C", "D"]
colors = ["red", "green", "pink", "blue"]

# Створення Streamlit UI
st.title("Інтерактивна карта районів")

selected_category = st.selectbox("Оберіть категорію", categories)

# Створення базової карти
m = folium.Map(location=[48.9226, 24.7103], zoom_start=8)

cat_groups = {c: folium.FeatureGroup(c).add_to(m) for c in categories}
folium.LayerControl().add_to(m)

# Додавання точок
for district, category, color in zip(districts, categories, colors):
    coords = get_coordinates(district)
    if coords:
        folium.Marker(location=coords, popup=district, icon=folium.Icon(color=color)).add_to(cat_groups[category])

# Відображення карти у Streamlit
st_folium(m, width=700, height=500)
