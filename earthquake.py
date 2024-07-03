import folium
import pandas as pd
import geopandas as gpd
from folium import plugins

# Data URLs
geojson_url = "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/all_world.geojson"
csv_url = "../The-Python-Graph-Gallery/static/data/earthquakes.csv"

# Load data
world = gpd.read_file(geojson_url)
world = world[~world['name'].isin(["Antarctica", "Greenland"])]

df = pd.read_csv(csv_url)
df = df[df['Depth (km)'] >= 0.01]  # depth of at least 10 meters
df.sort_values(by='Depth (km)', ascending=False, inplace=True)

# Initialize map
m = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodb positron')

# Add world boundaries
folium.GeoJson(world, style_function=lambda x: {'fillColor': '#E9C46A', 'color': '#E9C46A', 'weight': 0.1, 'fillOpacity': 0.2}).add_to(m)

# Add earthquake data with tooltips
for idx, row in df.iterrows():
    tooltip_text = f"""
    <b>Location:</b> {row['Region']}<br>
    <b>Magnitude:</b> {row['Magnitude']}<br>
    <b>Depth:</b> {row['Depth (km)']} km<br>
    <b>Date:</b> {row['Date']}
    """
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Depth (km)'] * 0.05,
        color='#B95F4C',
        fill=True,
        fill_color='#FEA996',
        fill_opacity=0.6,
        weight=0.4,
        tooltip=folium.Tooltip(tooltip_text, sticky=True)
    ).add_to(m)

# Save and display the map
m.save('index.html')