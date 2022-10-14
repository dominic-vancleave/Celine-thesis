# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 17:39:26 2022

@author: domin
"""
#%% Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt

#%% Importing Necessary Data from .csv Files
neb_tier2_data = pd.read_csv('coordinates.csv')

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

plt.scatter(longitudes_tier2, latitudes_tier2, alpha = 0.2, c = 'g', s= 10, marker = 'D')

ax.set_title('Plotting Tank Data on Nebraska Map (Tier II)')
ax.set_xlim(neb_boundary[0], neb_boundary[1])
ax.set_ylim(neb_boundary[2], neb_boundary[3])

ax.imshow(neb_map, zorder = 0, extent = neb_boundary, aspect = 'equal')
plt.savefig('Nebraska_tanks_tier2.png', bbox_inches='tight',pad_inches = 0.1)