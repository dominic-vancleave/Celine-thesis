# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:30:11 2022
Last Updated on Fri Jan 27 2023
@author: Dominic Van Cleave-Schottland
"""
"""
The code below takes in and visualizes EPA's TRI (Toxic Registry Inventory) Data on ASTs in Nebraska,
showing the types of chemicals in the tanks and how frequently they appear. The general site to find 
such data is here: https://enviro.epa.gov/facts/tri/form_r_search.html?
TRI Data includes such information as:
  - Geographic Information (longitude & latitudes) of facilities
  - Name of Facility & Parent company owning the tank
  - Specific name and CAS number of chemicals stored in each tank
The output of this code is a bar graph showing the frequencies of all chemicals which appear more than
10 times and betweeen 2 and 10 times. Also, an Excel document with all chemicals appearing fewer than 2
times is also produces. 
"""
#&& Import Modules
import pandas as pd
import collections
import matplotlib.pyplot as plt

#&& Load in TRI Data & Extract Specific Values Needed
neb_tri_data = pd.read_csv('tri_2020_ne.csv')

chemicals = neb_tri_data['34. CHEMICAL'].tolist()

latitudes = neb_tri_data['12. LATITUDE'].tolist()
longitudes = neb_tri_data['13. LONGITUDE'].tolist()

#&& Manipulate Data to Exclude Unnecessary Artifacts (ie to make the chemical names shorter)
for i in range(0, len(chemicals)-1):
    for j in range(0, len(chemicals)-1):
        if '(' in chemicals[j]:
            temp =  ''
            for word in chemicals[j].split():
                if '(' not in word:
                    temp += word
                if '(' in word:
                    break
                temp += ' '
            chemicals[j] = temp[:-1]
        if 'and' in chemicals[j].lower():
            temp =  ''
            for word in chemicals[j].split():
                if word.lower() != 'and':
                    temp += word
                if word.lower() == 'and':
                    break
                temp += ' '
            chemicals[j] = temp[:-1]
        if chemicals[i] in chemicals[j]:
            chemicals[j] = chemicals[i]
  
# Create a sorted dictionary with all chemical names  
freq = dict(sorted(collections.Counter(chemicals).items(), key=lambda item: item[1], reverse=True))

above_10 = {}
below_10 = {}
one_and_two_tanks = {}

# Sort chemicals based on frequency
for chem in list(freq.keys()):
    if freq[chem] <= 2:
        one_and_two_tanks[chem] = freq[chem]
    elif freq[chem] <= 10:
        below_10[chem] = freq[chem]
    else:
        above_10[chem] = freq[chem]

# Plotting Chemical Frequencies BELOW 10 Tanks
plt.figure(1)
plt.figure(figsize=(10,4))
plt.bar(range(len(below_10)), list(below_10.values()), tick_label = list(below_10.keys()))
plt.title('Frequency of Chemicals in TRI ASTs, NE (freq < 10)')
plt.xlabel('Chemical Name')
plt.ylabel('Number of Tanks')
plt.xticks(rotation=90)

# Plotting Chemical Frequencies ABOVE 10
plt.figure(2)
plt.figure(figsize=(10,4))
plt.bar(range(len(above_10)), list(above_10.values()), tick_label = list(above_10.keys()))
plt.title('Frequency of Chemicals in TRI ASTs, NE (freq > 10)')
plt.xlabel('Chemical Name')
plt.ylabel('Number of Tanks')
plt.xticks(rotation=90)
plt.show()

# Printing Chemical Frequencies of ONE
# for c in one_and_two_tanks:
#     print(c)
    
# Create Excel Sheet with Chemicals Appearing Once
df = pd.DataFrame(data=one_and_two_tanks, index=[0])
df = (df.T)
df.to_excel('one_and_two_tanks.xlsx')