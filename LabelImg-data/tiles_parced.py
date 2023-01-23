# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 2022
Last Updated on Mon Jan 23 2023

@author: Dominic Van Cleave-Schottland
"""
"""
This code breaks up the larger .json file by state (or region), creating 50+ new
Excel documents for each. Contained in each Excel file is simply the geographic 
center of each AST, however code could be added to also add in information 
about the size of each tank (or any other characteristic in the .json file) if 
wanted. Note that the code below only keeps information about close roof, external
floating, narrow closed roof, and spherical tanks. Again, code could be added
(or in this case deleted) to include more or fewer tanks.
"""
#%% Import Modules
import json
import pandas as pd

#%% Load and Manipulate Data
# Load data from tiles
tile_data = json.load(open("tile_level_annotations_FIXED.json"))
## NOTE: this FIXED .json file accounts for the geographical errors in the original
#        json file, specifically the inclusion of Canadian and Mexican tanks, but also
#        has figured out the states of tanks located far enough off the coast to result
#        in LabelImg giving it no state

# Create arrays/sets to hold information
# WANT: State & Geographic Center of tank box
# NOTE: Could also add in the size of the tank box for more precise location
#       when matching
tank_info = {}

temp_NWlong = 0
temp_SElong = 0
temp_center_long = 0
temp_NWlat = 0
temp_SElat = 0
temp_center_lat = 0
center = []

for feature in tile_data['features']:
    if ((feature['properties']['object_class'] == 'closed_roof_tank') or
       (feature['properties']['object_class'] == 'external_floating_roof_tank') or
       (feature['properties']['object_class'] == 'narrow_closed_roof_tank') or
       (feature['properties']['object_class'] == 'spherical_tank')):
        try:
            # Geographic Center
            temp_NWlong = feature['properties']['nw_corner_polygon_lon']
            temp_SElong = feature['properties']['se_corner_polygon_lon']
            temp_center_long = (temp_NWlong + temp_SElong) / 2
            temp_NWlat = feature['properties']['nw_corner_polygon_lat']
            temp_SElat = feature['properties']['se_corner_polygon_lat']
            temp_center_lat = (temp_NWlat + temp_SElat) / 2
            
            center = [temp_center_lat, temp_center_long]
            
            # Determining if seen the state before
            # If not, create a new dictionary entry within tank_info
            if feature['properties']['state'] not in tank_info:
                tank_info[feature['properties']['state']] = [center]
            else:
                # If so, just addend the center coords in the tank_info dict spot
                tank_info[feature['properties']['state']].append(center)
                
        except KeyError:
            print("Error")
        
# Creating Excel Sheets for each individual State with all the tanks therein
for state in tank_info:
    # NOTE: Because of the "/" in New Brunswick and the inability to have slashes
    #       in excel file names, I've just replaced the state below
    if state == 'New Brunswick / Nouveau-Brunswick':
        df = pd.DataFrame(tank_info[state])
        writer = pd.ExcelWriter(('New Brunswick.xlsx'), engine='xlsxwriter')
        df.to_excel(writer, sheet_name='New Brunswick', index=False)
        writer.save()
    else:
        df = pd.DataFrame(tank_info[state])
        writer = pd.ExcelWriter((state + '.xlsx'), engine='xlsxwriter')
        df.to_excel(writer, sheet_name=state, index=False)
        writer.save()
    