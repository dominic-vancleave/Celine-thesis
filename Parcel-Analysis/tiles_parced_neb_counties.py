# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 2022
Last Updated on Wed Mar 8 2023

@author: Dominic Van Cleave-Schottland
"""
"""
This code breaks up the larger .json file by county within Nebraska, creating new
Excel documents for each. Contained in each Excel file is simply the geographic 
center of each AST, however code could be added to also add in information 
about the size of each tank (or any other characteristic in the .json file) if 
wanted. 

Note that the code below only keeps information about close roof, external
floating, narrow closed roof, and spherical tanks. Again, code could be added
(or in this case deleted) to include more or fewer tanks.
"""
#%% Import Modules
import json
import pandas as pd
import csv

#%% Load and Manipulate Data
# Load data from tiles
tile_data = json.load(open("tile_level_annotations.json"))

# Load FIPS excel data
fips_data = pd.read_csv('fips-by-state.csv', encoding= 'unicode_escape')

fips = fips_data['fips'].tolist()
county_names = fips_data['name']

# Create arrays/sets to hold information
# WANT: Geographic Center of tank box sorted by County
# NOTE: Could also add in the size of the tank box for more precise location
#       when matching
tank_info = {}

center_lat = 0
center_lon = 0
center = 0

county_fips = ""
state_fips = ""
state_county = 0
tank_county = ""

for feature in tile_data['features']:
    if ((feature['properties']['object_class'] == 'closed_roof_tank') or
        (feature['properties']['object_class'] == 'external_floating_roof_tank') or
        (feature['properties']['object_class'] == 'narrow_closed_roof_tank') or
        (feature['properties']['object_class'] == 'spherical_tank')):
        try:
            # Geographic Center
            center_lat = feature['properties']['centroid_lat']
            center_lon = feature['properties']['centroid_lon']
            
            center = [center_lat, center_lon]
            
            # Setting up County Information
            county_fips = feature['properties']['county_fips']
            state_fips = feature['properties']['state_fips']
            if county_fips is None or state_fips is None:
                county_fips = '0'
                state_fips = '0'
            state_county = int(state_fips + county_fips)
            tank_county = county_names[fips.index(state_county)].split()[0]
            
            # Determining if seen the state before
            # If not, create a new dictionary entry within tank_info
            if (int(state_fips) == 31 and int(county_fips) == 25): # Code 31 is Nebraska # 
                if tank_county not in tank_info:
                    tank_info[tank_county] = [center]
                else:
                    # If so, just addend the center coords in the tank_info dict spot
                    tank_info[tank_county].append(center)
                
        except KeyError:
            print("Error")
        
# Creating Excel Sheets for each individual County with all the tanks therein
for county in tank_info:
    df = pd.DataFrame(tank_info[county])
    writer = pd.ExcelWriter((county + '.xlsx'), engine='xlsxwriter')
    df.to_excel(writer, sheet_name=county, index=False)
    writer.save()