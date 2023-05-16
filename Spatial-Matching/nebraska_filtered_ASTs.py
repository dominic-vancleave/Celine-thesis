# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:29:07 2022
Last Updated on Wed Feb 1 2023

@author: Dominic Van Cleave-Schottland
"""
"""
This code's purpose is to filter out erroneous tanks from the TRI, Tier II, and
HIFLD by a simple distance metric (in this code, roughly 170m), creating an 
excel spreadsheet of 1) each LabelImg tank with a matching TRI, Tier II, and/or
HIFLD tank and 2) a corresponding list of all tanks within the distance buffer.

This code also tells the user how many LabelImg tanks are *not* matched within 
the distance buffer. 

This code makes use of the shapely library, a site to which is found below:
https://shapely.readthedocs.io/en/stable/manual.html
"""
#%% Import Modules
import pandas as pd
from shapely.geometry import Point
import csv

#%% Import datasets and extract necessary data
neb_label_data = pd.read_csv('Nebraska_labeled.csv')
neb_tier2_data = pd.read_csv('coordinates.csv')
neb_tri_data = pd.read_csv('tri_2020_ne.csv')
neb_hifld_data = pd.read_csv('HIFLD_data.csv')

#%% Create lists and dictionaries for each LabelImg tank
lat_lon_labeled_empty = []
lat_lon_labeled = {}
for i in range(0, len(neb_label_data)):
    p = Point(neb_label_data['Lat'][i], neb_label_data['Long'][i])
    lat_lon_values = []
    for j in range(0, len(neb_tri_data)):
        if Point(neb_tri_data['12. LATITUDE'][j], neb_tri_data['13. LONGITUDE'][j]).within(p.buffer(0.0012)): #0.0007 = ~100m
            lat_lon_values.append([neb_tri_data['12. LATITUDE'][j], neb_tri_data['13. LONGITUDE'][j]])        #0.0012 = ~170m
    for k in range(0, len(neb_tier2_data)):
        if Point(neb_tier2_data['LAT'][k], -neb_tier2_data['LON'][k]).within(p.buffer(0.0012)):
            lat_lon_values.append([neb_tier2_data['LAT'][k], -neb_tier2_data['LON'][k]])
    for k in range(0, len(neb_hifld_data)):
        if Point(neb_hifld_data['LATITUDE'][k], neb_hifld_data['LONGITUDE'][k]).within(p.buffer(0.0012)):
            lat_lon_values.append([neb_hifld_data['LATITUDE'][k], neb_hifld_data['LONGITUDE'][k]])
    if lat_lon_values == []:
        lat_lon_labeled_empty.append([neb_label_data['Lat'][i], neb_label_data['Long'][i]])
    else:
        lat_lon_labeled[neb_label_data['Lat'][i], neb_label_data['Long'][i]] = lat_lon_values
   
# Print the number of unassigned tanks based on the distance buffer
print("Number of Unassigned Tanks = " + str(len(lat_lon_labeled_empty)))

# Create an excel sheet for these filtered tanks
with open ('filtered_tanks.csv','w', newline='') as csv_file:
    csv.writer(csv_file).writerows([k, *v] for k,v in lat_lon_labeled.items())