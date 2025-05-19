import streamlit as st
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

#Стилі (анімований заголовок + неонові рамки)
st.markdown("""
    <style>
    @keyframes glow {
        0% {color: #ff0066;}
        50% {color: #0ff;}
        100% {color: #ff0066;}
    }

    .title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        animation: glow 2s infinite alternate;
    }

    .stTextArea, .stSelectbox {
        border: 2px solid #0ff;
        box-shadow: 0px 0px 10px #0ff;
        font-size: 18px;
        padding: 10px;
    }

    .stButton > button {
        background-color: #ff0066;
        color: white;
        border-radius: 8px;
        box-shadow: 0px 0px 10px #ff0066;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #ff3399;
        box-shadow: 0px 0px 20px #ff3399;
    }
    </style>
""", unsafe_allow_html=True)

#Кешування координат
@st.cache_data
def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(place_name)
    return (location.latitude, location.longitude) if location else None

#Категорії та кольори точок (українською)
categories = ["A", "B", "C", "D"]
colors = {"Червоний": "red", "Зелений": "green", "Рожевий": "pink", "Синій": "blue"}

#Анімований заголовок
st.markdown(f"<div class='title'>Інтерактивна карта районів</div>", unsafe_allow_html=True)

#Інтерактивне введення районів
district_input = st.text_area("📍 Введіть райони через кому", "Івано-Франківський район, Калуський район, Коломийський район")
districts = [d.strip() for d in district_input.split(",")]

#Вибір категорії та кольору маркерів
selected_category = st.selectbox("📌 Оберіть категорію", categories)
selected_color_name = st.selectbox("🖌️ Оберіть колір маркерів", list(colors.keys()))
selected_color = colors[selected_color_name]  # Перетворення у формат Folium

#Створення базової карти
m = folium.Map(location=[48.9226, 24.7103], zoom_start=8)
cat_groups = {c: folium.FeatureGroup(c).add_to(m) for c in categories}
folium.LayerControl().add_to(m)

#Додавання точок
for district in districts:
    coords = get_coordinates(district)
    if coords:
        folium.Marker(location=coords, popup=district, icon=folium.Icon(color=selected_color)).add_to(cat_groups[selected_category])

#Відображення карти у Streamlit
st_folium(m, width=700, height=500)

#Підпис автора
st.markdown("<div style='text-align: center; font-size: 20px; font-weight: bold; margin-top: 20px;'>Автор: Шаблінський С.І.</div>", unsafe_allow_html=True)
