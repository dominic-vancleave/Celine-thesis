# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 2022
Last Updated on Mon Jan 23 2023

@author: Dominic Van Cleave-Schottland
"""
"""
This code's purpose is to fix the original .json file given in Sept 2022. The 
main problem fixed here is that some tanks in the original file did not have
a state assigned to them, as they were located sufficiently far off the coast
of America to be considered "stateless" by LabelImg. Thus, this code finds which
state these tanks are closest too and assigns said state to them. Also, some
tanks in the LabelImg set were located in Canada or Mexico which, again,
is considered "stateless" by LabelImg. This problem is also fixed herein. 
"""
#%% Import Modules
import json
from geopy.geocoders import Nominatim

#%% Load and Manipulate Data
# Load data from tiles
tile_data = json.load(open("tile_level_annotations.json"))
        
# Initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")

# Create arrays/sets to hold information
# NEED: Geographic center of tank to figure out which state it's in
nones = [] # holds information on the tank ID and coordinates of the "nones"
nones_locations = [] # holds information on the tank ID and final location of
                     # "nones"

for feature in tile_data['features']:
    temp_NWlong = 0
    temp_SElong = 0
    temp_center_long = 0
    temp_NWlat = 0  
    temp_SElat = 0
    temp_center_lat = 0
    temp_state = ''
    try:
        if (str(feature['properties']['state']) == 'None'):
            nones.append(str(feature['id']) + str(feature['geometry']['coordinates'][0][1]))
            temp_NWlong = round(feature['properties']['nw_corner_polygon_lon'], 5)
            temp_SElong = round(feature['properties']['se_corner_polygon_lon'], 5)
            temp_center_long = (temp_NWlong + temp_SElong) / 2
            temp_NWlat = round(feature['properties']['nw_corner_polygon_lat'], 5)
            temp_SElat = round(feature['properties']['se_corner_polygon_lat'], 5)
            temp_center_lat = (temp_NWlat + temp_SElat) / 2
            
            # Determination of "stateless" tanks state
            location = geolocator.reverse(str(temp_center_lat)+','+str(temp_center_long))
            
            temp_state = location.raw['address'].get('state', '')
            
            feature['properties']['state'] = temp_state
            nones_locations.append(str(feature['id']) + ": " + location.raw['address'].get('state', '') + ", " + location.raw['address'].get('country', ''))
    except KeyError:
        print("Error?")

with open('tile_level_annotations_FIXED.json', 'w') as test_json:
   json.dump(tile_data, test_json)