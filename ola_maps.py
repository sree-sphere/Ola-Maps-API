import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import time

def get_lat_lng(location):
    url = "https://api.olamaps.io/places/v1/autocomplete"
    params = {
        'input': location,
        'api_key': ''
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'predictions' in data and len(data['predictions']) > 0:
            first_prediction = data['predictions'][0]
            if 'geometry' in first_prediction and 'location' in first_prediction['geometry']:
                return (first_prediction['geometry']['location']['lat'], first_prediction['geometry']['location']['lng'])
    except requests.exceptions.RequestException as e:
        st.write(f"Request failed: {e}")
        time.sleep(6)
    return (None, None)

def get_autocomplete_results(place_type, lat, lng, radius):
    url = "https://api.olamaps.io/places/v1/autocomplete"
    params = {
        'input': place_type,
        'api_key': '',
        'location': f"{lat},{lng}",
        'radius': radius,
        'strictbounds': True
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'predictions' in data:
            return data['predictions'][:10]
    except requests.exceptions.RequestException as e:
        st.write(f"Request failed: {e}")
        time.sleep(6)
    return []

st.title("Ola Maps with Folium")

place_type = st.text_input("Enter the place type (e.g., Temple, Hospital, School, etc.):")
location = st.text_input("Enter location/region (e.g., Delhi, Chennai, Anna Nagar):")
radius = st.number_input("Enter the search radius in meters:", min_value=0, value=3000, step=100)
if place_type and location:
    lat, lng = get_lat_lng(location)
    if lat is not None and lng is not None:
        results = get_autocomplete_results(place_type, lat, lng, radius)
        if results:
            st.write("Search Results:")
            m = folium.Map(location=[lat, lng], zoom_start=13)
            folium.Marker([lat, lng], popup=location, icon=folium.Icon(color='green', icon='ok-sign')).add_to(m)  # City geomarker
            for place in results:
                place_name = place['structured_formatting']['main_text']
                place_lat = place['geometry']['location']['lat']
                place_lng = place['geometry']['location']['lng']
                folium.Marker([place_lat, place_lng], popup=place_name).add_to(m)
            folium_static(m)
            
            for place in results:
                place_name = place['structured_formatting']['main_text']
                place_lat = place['geometry']['location']['lat']
                place_lng = place['geometry']['location']['lng']
                st.write(f"Place Name: {place_name}")
                st.write(f"Latitude: {place_lat}")
                st.write(f"Longitude: {place_lng}\n")
        else:
            st.write("No results.")
    else:
        st.write("Could not find coordinates.")
