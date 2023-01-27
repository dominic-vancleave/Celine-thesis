# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 17:20:03 2022
Last Updated on Fri Jan 27 2023
@author: Dominic Van Cleave-Schottland
"""
"""
The code below taks in the geographic location data of TRI, Tier II, and LabelImg tanks in Nebraska 
and outputs a map displaying these tanks within Nebraska. Each dot on the map represents one AST. 
Color Code:
    - Blue = TRI
    - Red = LabelImg
    - Magenta = Tier II
The site used for creating and displaying a map of Nebraska is:
https://www.openstreetmap.org/
"""
#%% Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt

#%% Importing Necessary Data from .csv Files
neb_tri_data = pd.read_csv('tri_2020_ne.csv')
neb_label_data = pd.read_csv('Nebraska_labeled.csv')
neb_tier2_data = pd.read_csv('coordinates.csv')

latitudes_tri = neb_tri_data['12. LATITUDE'].tolist()
longitudes_tri = neb_tri_data['13. LONGITUDE'].tolist()

latitudes_lab = neb_label_data['Lat'].tolist()
longitudes_lab = neb_label_data['Long'].tolist()

latitudes_tier2 = neb_tier2_data['LAT'].tolist()
longitudes_tier2_pos = neb_tier2_data['LON'].tolist()

longitudes_tier2 = [ -x for x in longitudes_tier2_pos]

for i in range(0, len(latitudes_tier2)-1):
    if latitudes_tier2[i] > 100:
        del latitudes_tier2[i]
        del longitudes_tier2[i]

#%% Setting Boundaries and Importing the Image of Nebraska
neb_boundary = (-104.2, -95.1,
                  39.9,  43.1)

neb_map = plt.imread('Nebraska_map.png')

#%% Plotting Tank Coords
fig = plt.figure(figsize=(25,12), dpi=100)
ax = fig.add_subplot(111)

### NOTE ###
# The below code for displaying each dataset can be commented out to create
# comparisons just between two datasets (ie. Tier II and TRI)
ax.scatter(longitudes_tri, latitudes_tri, zorder = 2, alpha = 0.3, c ='b', 
           s = 10, marker = 's', label = 'TRI Data')
ax.scatter(longitudes_lab, latitudes_lab, zorder = 3, alpha = 0.3, c = 'r', 
           s= 10, label = 'Labeled Data')
ax.scatter(longitudes_tier2, latitudes_tier2, zorder = 1, alpha = 0.3, c = 'm', 
           s= 10, marker = 'D', label = 'Tier II Data')

ax.set_title('Plotting Tank Data on Nebraska Map (Overlap)') # if comparing only two, change title
ax.set_xlim(neb_boundary[0], neb_boundary[1])
ax.set_ylim(neb_boundary[2], neb_boundary[3])
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.legend()
ax.imshow(neb_map, zorder = 0, extent = neb_boundary, aspect = 'equal')
# If comparing only two datasets, change .png file name
plt.savefig('Nebraska_tanks_comparison.png', bbox_inches='tight',pad_inches = 0.1)
