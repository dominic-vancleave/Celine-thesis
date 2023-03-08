# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 09:27:33 2023
Last Updated on Wed Mar 1 2023

@author: Dominic Van Cleave-Schottland
"""
"""

"""
#%% Import Librariess
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry import mapping

import json
from geopy.geocoders import Nominatim

#%% Get polygons (parcels) and points (tank locations)
parcels = gpd.GeoDataFrame.from_file('Douglas_Parcels_4326.shp')

neb_label_data = pd.read_csv('Nebraska_labeled.csv')

# Extracting only tanks in Douglas County
douglas_tanks_lat = []
douglas_tanks_long = []

# Initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")

for coord in range(0, len(neb_label_data)):
    if neb_label_data['Lat'][coord] <= 41.40 and neb_label_data['Lat'][coord] >= 41.18 and neb_label_data['Long'][coord] <= -95.86 and neb_label_data['Long'][coord] >= -96.48:
        
        location = geolocator.reverse(str(neb_label_data['Lat'][coord])+','+str(neb_label_data['Long'][coord]))
        if location.raw['address'].get('county', '') == 'Douglas County':
            douglas_tanks_lat.append(neb_label_data['Lat'][coord])
            douglas_tanks_long.append(neb_label_data['Long'][coord])
           
# Create a Data Frame with the tank points (ie center of tanks)
df = pd.DataFrame({'lon':(pd.Series(douglas_tanks_long)).to_numpy(), 'lat':(pd.Series(douglas_tanks_lat)).to_numpy()})
df['coords'] = list(zip(df['lon'],df['lat']))
df['coords'] = df['coords'].apply(Point)
tanks = gpd.GeoDataFrame(df, geometry='coords', crs=parcels.crs)

# Perform spatial join to match points and polygons
pointInPolys = gpd.tools.sjoin(tanks, parcels, predicate="within", how='left')

# Plot
base = parcels.boundary.plot(linewidth=0.1, edgecolor="black")
tanks.plot(ax=base, color="blue", markersize=1)
base.set_xlim([-95.93, -95.91])
base.set_ylim([41.27, 41.28])
plt.show()
