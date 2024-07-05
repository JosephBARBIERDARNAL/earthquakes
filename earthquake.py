import folium
import pandas as pd
from folium import plugins
import os

# Load dataset
df = pd.read_csv("../The-Python-Graph-Gallery/static/data/earthquakes.csv")
df = df[df['Depth (km)'] >= 0.01]  # depth of at least 10 meters
df.sort_values(by='Depth (km)', ascending=False, inplace=True)

# Initialize map
m = folium.Map(
    location=[0, 0],
    zoom_start=2,
    tiles='cartodb positron'
)

# Add earthquake data with clustering
marker_cluster = plugins.MarkerCluster().add_to(m)

# Add all the individual earthquakes to the map
for idx, row in df.iterrows():
    tooltip_text = f"""
    <h3><b>Location:</b> {row['Region']}</h3>
    <h3><b>Magnitude:</b> {row['Magnitude']}</h3>
    <h3><b>Depth:</b> {row['Depth (km)']} km</h3>
    <h3><b>Date:</b> {row['Date']}</h3>
    """
    color = '#0a9396' if row['Magnitude'] < 5 else '#ee9b00' if row['Magnitude'] < 7 else '#ae2012'
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Depth (km)'] * 0.05,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        weight=0.4,
        tooltip=folium.Tooltip(tooltip_text, sticky=True)
    ).add_to(marker_cluster)

heat_data = [[row['Latitude'], row['Longitude'], row['Magnitude']] for idx, row in df.iterrows()]
plugins.HeatMap(heat_data).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save the map
path = 'index.html'
m.save(path)
os.system(f"open {path}")
