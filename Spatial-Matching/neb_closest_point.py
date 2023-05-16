# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 22:58:34 2022
Last Updated on May 16 2023

@author: Dominic Van Cleave-Schottland
"""
"""
The code below attempts to find the closest TRI or Tier II point for each
Labeled AST in Nebraska. Because it uses a very simple algorithm, the code
can take quite a long time to run. 
"""

#%% Imports
import pandas as pd
import json
from geopy.geocoders import Nominatim
from geopy import distance
import numpy as np
import collections

#%% Closest Node Function for finding the closest TRI or Tier II tank
def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    print(type(dist_2))
    return np.argmin(dist_2)

#%% Import Data
neb_tier2_data = pd.read_csv('coordinates.csv')
lat_lon_tier2 = np.empty((len(neb_tier2_data), 2), dtype=object)
for i in range(0, len(neb_tier2_data)):
    lat_lon_tier2[i] = (neb_tier2_data['LAT'][i], -neb_tier2_data['LON'][i])

neb_tri_data = pd.read_csv('tri_2020_ne.csv')
lat_lon_tri = np.empty((len(neb_tri_data), 2), dtype=object)
for j in range(0, len(neb_tri_data)):
    lat_lon_tri[j] = (neb_tri_data['12. LATITUDE'][j], neb_tri_data['13. LONGITUDE'][j])

neb_label_data = pd.read_csv('Nebraska_labeled.csv')
lat_lon_lab = np.empty((len(neb_label_data), 2), dtype=object)
for k in range(0, len(neb_label_data)):
    lat_lon_lab[k] = (neb_label_data['Lat'][k], neb_label_data['Long'][k])

tile_data = json.load(open("tile_level_annotations_FIXED.json"))

geolocator = Nominatim(user_agent="geoapiExercises")

#%% Initialize arrays and parse through the data using the geopy library
# to find the closest points

distances = np.empty((0, 1), dtype=object)
tanks = np.empty((0, 1), dtype=object)

for tank_lab in lat_lon_lab:
    temp_closest_dist = distance.distance(lat_lon_lab[0], lat_lon_tri[0]).km
    temp_closest_tank = lat_lon_tri[0]
    for tank_tri in lat_lon_tri:
        if distance.distance(tank_lab, tank_tri).km < temp_closest_dist:
            temp_closest_dist = distance.distance(tank_lab, tank_tri).km
            temp_closest_tank = tank_tri
    distances = np.append(distances, temp_closest_dist)
    tanks = np.append(tanks, temp_closest_tank)

print(str(round(distance.distance(lat_lon_tier2[4], lat_lon_lab[4]).km*100, 3)) + " meters")

print(closest_node(lat_lon_lab[1000], lat_lon_tri))