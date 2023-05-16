# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:30:11 2022
Last Updated on Wed Feb 1 2023

@author: Dominic Van Cleave-Schottland
"""
"""
The code below takes in and visualizes EPA's Tier II Data on ASTs in Nebraska,
as required by Section 312 of the Emergency Planning and Community Right-to-Know Act
(EPCRA), showing the types of chemicals in the tanks and how frequently they appear. 
The general site to find such data is here: https://deq-iis.ne.gov/tier2/
Tier II Data includes such information as:
  - Geographic Information (longitude & latitudes) of facilities and tanks
  - Specific name and CAS number of chemicals stored in each tank
The output of this code is a bar graph showing the frequencies of all chemicals which appear more than
10 times and betweeen 2 and 10 times. Also, an Excel document with all chemicals appearing fewer than 2
times is also produces. 
"""
#%% Import Modules
import pandas as pd
import collections
import matplotlib.pyplot as plt

#%% Load in Tier II Data & Extract Specific Values Needed
neb_tier2_data = pd.read_csv('chemicals.csv', encoding="ISO-8859-1")

chemicals_tier2 = neb_tier2_data['CHMSRT'].tolist()
rptname_tier2 = neb_tier2_data['RPTNAM'].tolist()

# Create a list of chemicals used in the dataset
chemicals_list = []

for k in range(0, len(chemicals_tier2)-1):
    if str(chemicals_tier2[k]).lower().title() == 'Nan':
        # if the chemical name is unavailable, use the RPT name
        chemicals_list.append(str(rptname_tier2[k]).lower().title())
    else:
        chemicals_list.append(str(chemicals_tier2[k]).lower().title())

# Sort a dictionary of chemical names
freq = dict(sorted(collections.Counter(chemicals_list).items(), key=lambda item: item[1], reverse=True))
chem_freq = {}

#&& Manipulate Data to Exclude Unnecessary Artifacts (ie to make the chemical names shorter)
### NEEDS WORKS ###
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
    elif ',' in key:
        temp = ''
        for word in key.split():
            if ',' not in word:
                temp += word
            if ',' in word:
                if ',' == word[-1]:
                    temp += ' '
                    temp += word[:-1]
                    break          
        if temp in chem_freq:
            temp_num = chem_freq[temp]
            chem_freq[temp] = freq[key] + temp_num
        else:
            chem_freq[temp] = freq[key]
    else:
        chem_freq[key] = freq[key]

# Create dictionaries for chemicals with certain frequencies
above_100 = {}
the40sto90s = {}
the30s = {}
the20s = {}
the10s = {}
below_10 = {}
one_and_two_tanks = {}

for chem in list(chem_freq.keys()):
    if chem_freq[chem] <= 2:
        one_and_two_tanks[chem] = chem_freq[chem]
    elif chem_freq[chem] <    10:
        below_10[chem] = chem_freq[chem]
    elif chem_freq[chem] < 20:
        the10s[chem] = chem_freq[chem]
    elif chem_freq[chem] < 30:
        the20s[chem] = chem_freq[chem]
    elif chem_freq[chem] < 40:
        the30s[chem] = chem_freq[chem]
    elif chem_freq[chem] < 100:
        the40sto90s[chem] = chem_freq[chem]
    else:
        above_100[chem] = chem_freq[chem]
        
# Plotting Chemical Frequencies ABOVE 100
plt.figure(1)
plt.figure(figsize=(13,4))
plt.bar(range(len(above_100)), list(dict(sorted(above_100.items(), key=lambda item: item[1], reverse=True)).values()), tick_label = list(above_100.keys()))
plt.title('Frequency of Chemicals in Tier II ASTs, NE (freq > 100)')
plt.xlabel('Chemical Name')
plt.ylabel('Number of Tanks')
plt.xticks(rotation=90)
plt.show()

# Plotting Chemical Frequencies BETWEEN 40 and 90
plt.figure(2)
plt.figure(figsize=(20,4))
plt.bar(range(len(the40sto90s)), list(dict(sorted(the40sto90s.items(), key=lambda item: item[1], reverse=True)).values()), tick_label = list(the40sto90s.keys()))
plt.title('Frequency of Chemicals in Tier II ASTs, NE (freq from 40s to 90s)')
plt.xlabel('Chemical Name')
plt.ylabel('Number of Tanks')
plt.xticks(rotation=90)
plt.show()

# Plotting Chemical Frequencies BETWEEN 30 and 40
plt.figure(3)
plt.figure(figsize=(20,4))
plt.bar(range(len(the30s)), list(dict(sorted(the30s.items(), key=lambda item: item[1], reverse=True)).values()), tick_label = list(the30s.keys()))
plt.title('Frequency of Chemicals in Tier II ASTs, NE (freq in 30s)')
plt.xlabel('Chemical Name')
plt.ylabel('Number of Tanks')
plt.xticks(rotation=90)
plt.show()

# Plotting Chemical Frequencies BETWEEN 20 and 30
plt.figure(4)
plt.figure(figsize=(20,4))
plt.bar(range(len(the20s)), list(dict(sorted(the20s.items(), key=lambda item: item[1], reverse=True)).values()), tick_label = list(the20s.keys()))
plt.title('Frequency of Chemicals in Tier II ASTs, NE (freq in 20s)')
plt.xlabel('Chemical Name')
plt.ylabel('Number of Tanks')
plt.xticks(rotation=90)
plt.show()

# Plotting Chemical Frequencies BETWEEN 10 and 20
plt.figure(5)
plt.figure(figsize=(20,4))
plt.bar(range(len(the10s)), list(dict(sorted(the10s.items(), key=lambda item: item[1], reverse=True)).values()), tick_label = list(the10s.keys()))
plt.title('Frequency of Chemicals in Tier II ASTs, NE (freq in 10s)')
plt.xlabel('Chemical Name')
plt.ylabel('Number of Tanks')
plt.xticks(rotation=90)
plt.show()