import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
default_location = [20.5937, 78.9629]
if 'locations' not in st.session_state:
    st.session_state.locations = []

def display_map():
    map_ = folium.Map(location=default_location, zoom_start=5)
    for loc in st.session_state.locations:
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=loc['name']
        ).add_to(map_)
    return map_

# Reverse Geocode and get Address info
def get_address(lat, lon):
    api_key = ""
    url = f"https://api.olamaps.io/places/v1/reverse-geocode?latlng={lat},{lon}&api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data.get('display_name', 'Address not found')
    else:
        return "Address not found"

st.title("Reverse Geocoding Location with Olamaps")

folium_map = st_folium(display_map(), width=700, height=500)

# Click
if folium_map and 'last_clicked' in folium_map and folium_map['last_clicked'] is not None:
    lat = folium_map['last_clicked']['lat']
    lon = folium_map['last_clicked']['lng']
    st.session_state.last_location = (lat, lon)
    address = get_address(lat, lon)
    st.write(f"Selected Location: Latitude: {lat}, Longitude: {lon}")
    st.write(f"Address: {address}")


# Loc list
if 'last_location' in st.session_state:
    location_name = st.text_input("Enter a name for this location:")
    if st.button("Add Location"):
        lat, lon = st.session_state.last_location
        st.session_state.locations.append({
            'lat': lat,
            'lon': lon,
            'name': location_name
        })
        st.success("Location added!")
        st.experimental_rerun()  # To refresh the map with the new marker

st.write("### Locations Added:")
for loc in st.session_state.locations:
    st.write(f"Name: {loc['name']}, Latitude: {loc['lat']}, Longitude: {loc['lon']}")
