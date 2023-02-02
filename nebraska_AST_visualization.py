# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 22:11:40 2022
Last Updated on Wed Feb 1 2023

@author: Dominic Van Cleave-Schottland
"""
"""
The below code takes the data from nebraska_filtered_ASTs.py and finds *the*
closest tank to each LabelImg AST that's matched. Its output prints bar graphs 
for the chemicals associated with each LabelImg tank (based on its corresponding
dataset) as well as a map of Nebraska showing the LabelImg tanks and matching
dataset tanks. 
"""
#%% Import Modules and Libraries
import matplotlib.pyplot as plt
import collections
import pandas as pd
import csv
from shapely.geometry import Point

#%% Import data and extract the needed values
neb_tier2_coords = pd.read_csv('coordinates.csv')
neb_tier2_chems = pd.read_csv('chemicals.csv', encoding="ISO-8859-1")
chemicals_tier2 = neb_tier2_chems['CHMSRT'].tolist()
rptname_tier2 = neb_tier2_chems['RPTNAM'].tolist()
latitudes_tier2 = neb_tier2_coords['LAT'].tolist()
longitudes_tier2_pos = neb_tier2_coords['LON'].tolist()

longitudes_tier2 = [ -x for x in longitudes_tier2_pos]

for i in range(0, len(latitudes_tier2)-1):
    if latitudes_tier2[i] > 100:
        del latitudes_tier2[i]
        del longitudes_tier2[i]

neb_tri_data = pd.read_csv('tri_2020_ne.csv')
latitudes_tri = neb_tri_data['12. LATITUDE'].tolist()
longitudes_tri = neb_tri_data['13. LONGITUDE'].tolist()
chemicals_tri = neb_tri_data['34. CHEMICAL'].tolist()

neb_hifld_data = pd.read_csv('HIFLD_data.csv')
latitudes_hifld = neb_hifld_data['LATITUDE'].tolist()
longitudes_hifld = neb_hifld_data['LONGITUDE'].tolist()
hifld_tank_type = neb_hifld_data['TANK TYPE'].tolist()

#%% Extract the data from the "filtered_tanks" excel sheet
close_tanks = {}
with open('filtered_tanks.csv') as file_obj:
    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        close_tanks[row[0]] = row[1:]

closest_tanks = {}
closest_tank = []
tank_chemicals = []

# Find *the* closest tank for each matching LabelImg tank
for key in close_tanks:    
    minimum_distance = 99
    for tank in close_tanks[key]:
        if Point(float(key[1:len(key)-1].split(", ")[0]), float(key[1:len(key)-1].split(", ")[1])).distance(Point(float(tank[1:len(tank)-1].split(", ")[0]), float(tank[1:len(tank)-1].split(", ")[1]))) < minimum_distance:
            minimum_distance = Point(float(key[1:len(key)-1].split(", ")[0]), float(key[1:len(key)-1].split(", ")[1])).distance(Point(float(tank[1:len(tank)-1].split(", ")[0]), float(tank[1:len(tank)-1].split(", ")[1])))
            closest_tank = [float(tank[1:len(tank)-1].split(", ")[0]), float(tank[1:len(tank)-1].split(", ")[1])]
    closest_tanks[float(key[1:len(key)-1].split(", ")[0]), float(key[1:len(key)-1].split(", ")[1])] = closest_tank

# Figure out which dataset matches the tank and find the chemical associated with the facility
for value in closest_tanks.values():
    if ((value[0] in latitudes_tri) and 
        (value[1] in longitudes_tri)):
        tank_index = latitudes_tri.index(value[0])
        tank_chemicals.append(str(chemicals_tri[tank_index]).lower().title())
    elif ((value[0] in latitudes_tier2) and 
        (value[1] in longitudes_tier2)):
        tank_index = latitudes_tier2.index(value[0])
        if str(chemicals_tier2[tank_index]).lower().title() == 'Nan':
            tank_chemicals.append(str(rptname_tier2[tank_index]).lower().title())
        else:
            tank_chemicals.append(str(chemicals_tier2[tank_index]).lower().title())
    elif ((value[0] in latitudes_hifld) and 
        (value[1] in longitudes_hifld)):
        tank_index = latitudes_hifld.index(value[0])
        tank_chemicals.append(str(hifld_tank_type[tank_index]).lower().title())
        
freq = dict(sorted(collections.Counter(tank_chemicals).items(), key=lambda item: item[1], reverse=True))
chem_freq = {}

# Clean up the chemical names within the tank data
for key in freq:
    if '(' in key and '(' not in key.split()[0]:
        temp =  ''
        for word in key.split():
            if '(' not in word:
                temp += word
            if '(' in word:
                break
            temp += ' '
        if ',' in temp:
            if temp[:-2] in chem_freq:
                temp_num = chem_freq[temp[:-2]]
                chem_freq[temp[:-2]] = freq[key] + temp_num
            else:
                chem_freq[temp[:-2]] = freq[key]
        elif temp[:-1] in chem_freq:
            temp_num = chem_freq[temp[:-1]]
            chem_freq[temp[:-1]] = freq[key] + temp_num
        else:
            chem_freq[temp[:-1]] = freq[key]
    else:
        chem_freq[key] = freq[key]
        
above_10 = {}
below_10 = {}

for chem in list(chem_freq.keys()):
    if chem_freq[chem] <= 10:
        below_10[chem] = chem_freq[chem]
    else:
        above_10[chem] = chem_freq[chem]

# Plotting Chemical Frequencies BELOW 10 Tanks
plt.figure(1)
plt.figure(figsize=(10,4))
plt.bar(range(len(below_10)), list(dict(sorted(below_10.items(), key=lambda item: item[1], reverse=True)).values()), tick_label = list(below_10.keys()))
plt.title('Frequency of Chemicals in Labeled ASTs, NE (freq < 10)')
plt.xlabel('Chemical Name')
plt.ylabel('Number of Tanks')
plt.xticks(rotation=90)

# Plotting Chemical Frequencies ABOVE 10
plt.figure(2)
plt.figure(figsize=(10,4))
plt.bar(range(len(above_10)), list(dict(sorted(above_10.items(), key=lambda item: item[1], reverse=True)).values()), tick_label = list(above_10.keys()))
plt.title('Frequency of Chemicals in Labeled ASTs, NE (freq > 10)')
plt.xlabel('Chemical Name')
plt.ylabel('Number of Tanks')
plt.xticks(rotation=90)
plt.show()


# #%% Setting Boundaries and Importing the Image of Nebraska
# # LAT = Y
# # LONG = X
# plot_labeled_asts_x = []
# plot_labeled_asts_y = []

# for key in closest_tanks:
#     if (closest_tanks[key][0] == 41.149976) and (closest_tanks[key][1] == -102.933624):
#         plot_labeled_asts_x.append(key[1])
#         plot_labeled_asts_y.append(key[0])

# boundary = (-102.93724, -102.92855,
#              41.14786,  41.15265)

# neb_map = plt.imread('Nebraska_example_map.png')
# #%% Plotting Tank Coords
# fig = plt.figure(figsize=(12,12), dpi=100)
# ax = fig.add_subplot(111)

# plt.plot(-102.933624, 41.149976, 'ro', label='Publicly Available Dataset Point')
# # THIS IS AN HIFLD DATA POINT!!!

# plt.plot(plot_labeled_asts_x, plot_labeled_asts_y, 'bo', label='AST Dataset Points')

# ax.set_title('Example of the Problem with the Current Data')
# ax.set_xlim(boundary[0], boundary[1])
# ax.set_ylim(boundary[2], boundary[3])
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')

# plt.legend()
# ax.imshow(neb_map, zorder = 0, extent = boundary, aspect = 'equal')
# plt.savefig('Nebraska_test_tank1.png', bbox_inches='tight',pad_inches = 0.1)

#%% Setting Boundaries and Importing the Image of Nebraska
neb_boundary = (-104.2, -95.1,
                  39.9,  43.1)

neb_map = plt.imread('Nebraska_map.png')
#%% Plotting Tank Coords
fig = plt.figure(figsize=(25,12), dpi=100)
ax = fig.add_subplot(111)

labeled_tanks_x = []
labeled_tanks_y = []
matching_tanks_x = []
matching_tanks_y = []

for i in range(0, len(closest_tanks)):
    labeled_tanks_x.append(list(closest_tanks.keys())[i][1])
    labeled_tanks_y.append(list(closest_tanks.keys())[i][0])
    matching_tanks_x.append(list(closest_tanks.values())[i][1])
    matching_tanks_y.append(list(closest_tanks.values())[i][0]) 
    
# Change the "zorder" parameter to put either the Labeled Data or Matching Data
# on top
ax.scatter(labeled_tanks_x, labeled_tanks_y, zorder = 1, alpha = 1, c = 'r', 
            s= 15, label = 'Labeled Data')
ax.scatter(matching_tanks_x, matching_tanks_y, zorder = 2, alpha = 0.5, c ='b', 
            s = 10, marker = 's', label = 'Matching Tanks')

ax.set_title('Plotting Tank Data on Nebraska Map (Overlap: All Datasets)')
ax.set_xlim(neb_boundary[0], neb_boundary[1])
ax.set_ylim(neb_boundary[2], neb_boundary[3])
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.legend()
ax.imshow(neb_map, zorder = 0, extent = neb_boundary, aspect = 'equal')
#plt.savefig('Nebraska_tanks_HIFLD.png', bbox_inches='tight',pad_inches = 0.1)