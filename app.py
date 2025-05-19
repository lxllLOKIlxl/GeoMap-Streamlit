import streamlit as st
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

# Кешування для швидкої роботи
@st.cache_data
def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(place_name)
    return (location.latitude, location.longitude) if location else None

# Категорії та кольори точок
categories = ["A", "B", "C", "D"]
colors = ["red", "green", "pink", "blue"]

#Інтерактивне введення районів
st.title("Інтерактивна карта районів")
district_input = st.text_area("Введіть райони через кому", "Івано-Франківський район, Калуський район, Коломийський район")
districts = [d.strip() for d in district_input.split(",")]

#Вибір категорії та кольору
selected_category = st.selectbox("Оберіть категорію", categories)
selected_color = st.selectbox("Оберіть колір маркерів", colors)

#Створення базової карти
m = folium.Map(location=[48.9226, 24.7103], zoom_start=8)
cat_groups = {c: folium.FeatureGroup(c).add_to(m) for c in categories}
folium.LayerControl().add_to(m)

#Додавання точок
for district in districts:
    coords = get_coordinates(district)
    if coords:
        folium.Marker(location=coords, popup=district, icon=folium.Icon(color=selected_color)).add_to(cat_groups[selected_category])

# Відображення карти у Streamlit
st_folium(m, width=700, height=500)
