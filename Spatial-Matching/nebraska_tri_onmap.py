# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 17:20:03 2022
Last Updated on Fri Jan 27 2023
@author: Dominic Van Cleave-Schottland
"""
"""
The code below taks in the geographic location data of TRI tanks in Nebraska and outputs a 
map displaying these tanks within Nebraska. Each dot on the map represents one AST. The site
used for creating and displaying a map of Nebraska is:
https://www.openstreetmap.org/
"""
#%% Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt

#%% Importing Necessary Data from .csv Files
neb_tri_data = pd.read_csv('tri_2020_ne.csv')

latitudes_tri = neb_tri_data['12. LATITUDE'].tolist()
longitudes_tri = neb_tri_data['13. LONGITUDE'].tolist()

#%% Setting Boundaries and Importing the Image of Nebraska
neb_boundary = (-104.2, -95.1,
                  39.9,  43.1)

neb_map = plt.imread('Nebraska_map.png')

#%% Plotting Tank Coords
fig = plt.figure(figsize=(25,12), dpi=100)
ax = fig.add_subplot(111)

ax.scatter(longitudes_tri, latitudes_tri, zorder = 1, c ='b', s = 10, marker = 's')

ax.set_title('Plotting Tank Data on Nebraska Map (TRI)')
ax.set_xlim(neb_boundary[0], neb_boundary[1])
ax.set_ylim(neb_boundary[2], neb_boundary[3])

ax.imshow(neb_map, zorder = 0, extent = neb_boundary, aspect = 'equal')
plt.savefig('Nebraska_tanks_TRI.png', bbox_inches='tight',pad_inches = 0.1)
