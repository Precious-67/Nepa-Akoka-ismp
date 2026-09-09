import os
import folium
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Substation 

# Load variables from a local .env file (this file is never uploaded to GitHub)
load_dotenv()

# 1. Connect to the database (the real password lives in your local .env file)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

print("🗺️ Querying database and generating NEPA Unilag Map...")

# 2. Create the base map centered exactly on the Unilag campus
campus_map = folium.Map(location=[6.5170, 3.3980], zoom_start=15, tiles="CartoDB positron")

# 3. Ask PostGIS to extract the exact Latitude (ST_Y) and Longitude (ST_X) for every station
stations = session.query(
    Substation.station_id,
    Substation.ring_cluster,
    Substation.current_status,
    func.ST_Y(Substation.coordinates).label('latitude'),
    func.ST_X(Substation.coordinates).label('longitude')
).all()

# 4. Loop through every station and draw it on the map
for station in stations:
    # If the station is tripping, make it RED. Otherwise, make it GREEN.
    if station.current_status == "FAULT":
        marker_color = "red"
        icon_symbol = "info-sign"
    else:
        marker_color = "green"
        icon_symbol = "bolt"

    # Create the text box that pops up when you click a station
    popup_text = f"""
    <b>Station ID:</b> {station.station_id}<br>
    <b>Ring Cluster:</b> {station.ring_cluster}<br>
    <b>Status:</b> {station.current_status}
    """

    # Drop the pin on the map
    folium.Marker(
        location=[station.latitude, station.longitude],
        popup=folium.Popup(popup_text, max_width=250),
        icon=folium.Icon(color=marker_color, icon=icon_symbol)
    ).add_to(campus_map)

# 5. Save the final map as a webpage
campus_map.save("unilag_grid_map.html")
print("✅ Success! The map has been saved as 'unilag_grid_map.html'.")