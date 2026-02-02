import requests
import folium
from folium.plugins import MeasureControl


def calculate_elevation_difference(lat1, lon1, lat2, lon2):
    # Using the OpenTopography API to get the elevation data
    url = f"https://api.opentopography.org/api/v2/requests?format=json&request_type=point&lat={lat1}&lon={lon1}&lat2={lat2}&lon2={lon2}"
    response = requests.get(url)
    data = response.json()
    
    # Get the elevation values from the API response
    elevation1 = data["elevation"]["value"]
    elevation2 = data["elevation"]["value2"]
    
    return abs(elevation1 - elevation2)

def create_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    MeasureControl().add_to(m)
    return m

def main():
    lat1 = float(input("Enter the latitude of point 1: "))
    lon1 = float(input("Enter the longitude of point 1: "))
    lat2 = float(input("Enter the latitude of point 2: "))
    lon2 = float(input("Enter the longitude of point 2: "))

    elevation_difference = calculate_elevation_difference(lat1, lon1, lat2, lon2)
    
    m = create_map(lat1, lon1)
    folium.Marker([lat1, lon1], popup=f"Elevation: {elevation_difference}m").add_to(m)
    folium.Marker([lat2, lon2], popup=f"Elevation: {elevation_difference}m").add_to(m)

    m.save("map.html")

if __name__ == "__main__":
    main()