# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:00:30 2022
Last Updated on Wed Feb 1 2023
@author: Dominic Van Cleave-Schottland
"""
"""
The code below takes in and visualizes DHS's HIFLD (Homeland Infrastructure Foundation-Level Data) on 
ASTs in Nebraska, showing the types of chemicals in the tanks and how frequently they appear. 
The general site to find such data is here: https://hifld-geoplatform.opendata.arcgis.com/
HIFLD Data includes such information as:
  - Geographic Information (longitude & latitudes) of facilities
  - General information on tank contents
  - Total capcity of each facility
The output of this code is a bar graph showing the frequencies of each of the 4 types of tanks.
"""
#%% Importing Modules
import pandas as pd
import collections
import matplotlib.pyplot as plt
import textwrap

#%% Code to efficiently wrap text in the bar graph
def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width,
                      break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)

#%% Importing and parsing the data
neb_hifld_data = pd.read_csv('HIFLD_data.csv')

chemicals = neb_hifld_data['TANK TYPE'].tolist()

latitudes = neb_hifld_data['LATITUDE'].tolist()
longitudes = neb_hifld_data['LONGITUDE'].tolist()
            
# Create a sorted dictionary with all chemical names
freq = dict(sorted(collections.Counter(chemicals).items(), key=lambda item: item[1], reverse=True))

#%% Plotting the data in a bar graph
fig, ax = plt.subplots(figsize=(5,5))
ax.set_title('Frequency of Chemicals in HIFLD ASTs, NE')
ax.bar(range(len(freq)), list(freq.values()), tick_label = list(freq.keys()))
ax.set_xlabel('Tank Type')
ax.set_ylabel('Number of Tanks')
wrap_labels(ax, 10)
ax.figure
