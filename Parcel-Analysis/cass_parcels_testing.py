# -*- coding: utf-8 -*-
"""
Created on Wed Mar 8 09:27:33 2023
Last Updated on Thur Mar 9 2023

@author: Dominic Van Cleave-Schottland
"""
"""
This code was just testing the capabilities of shapely to find parcels with 
Labeled ASTs in them
"""
#%% Import Librariess
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

#%% Get polygons (parcels) and points (tank locations)
cass_parcels = gpd.GeoDataFrame.from_file('Cass_Parcels_4326.shp')

all_tanks = gpd.GeoDataFrame.from_file('tile_level_annotations.shp')

pointInPolys = gpd.tools.sjoin(all_tanks, cass_parcels)

cass_refined = pd.DataFrame({'OwnerName' : []})
cass_refined["OwnerName"] = pointInPolys.loc[:,"OwnerName1"]
cass_refined["CenterLat"] = pointInPolys.loc[:,"centroid_1"]
cass_refined["CenterLon"] = pointInPolys.loc[:,"centroid_l"]

# Load in Tier II Data with Chemicals & Facility Name
neb_tier2_data = pd.read_csv('Nebraska_TierII_data.csv', encoding="ISO-8859-1", low_memory=False)
neb_facnam_normal = neb_tier2_data['FACNAM'].tolist()
neb_facnam = [x.lower() for x in neb_facnam_normal]
neb_chem = neb_tier2_data['CHMSRT'].tolist()
neb_rpt = neb_tier2_data['RPTNAM'].tolist()
neb_lat = neb_tier2_data['Lat'].tolist()
neb_lon = neb_tier2_data['Long'].tolist()

cass_chemicals = []
owner_indicies = []
match = False

for j in range(0, len(cass_refined)):
    cass_tank_lat = cass_refined['CenterLat'].tolist()[j]
    cass_tank_lon = cass_refined['CenterLon'].tolist()[j]
    cass_tank_fac = cass_refined["OwnerName"].tolist()[j].lower()
    #print(cass_tank_fac)
    owner_indicies = [i for i, x in enumerate(neb_facnam) if x == cass_tank_fac]
    if len(owner_indicies) > 0:
        for index in owner_indicies:
            match = False
            if ((cass_tank_lat - 0.001) <= neb_lat[index] <= (cass_tank_lat + 0.001)) and ((cass_tank_lon - 0.001) <= neb_lon[index] <= (cass_tank_lon + 0.001)) and (match == False):
                if pd.isna(neb_chem[index]):
                    cass_chemicals.append(neb_rpt[index])
                else:
                    cass_chemicals.append(neb_chem[index])
                neb_chem.pop(index)
                neb_facnam.pop(index)
                neb_lat.pop(index)
                neb_lon.pop(index)
                neb_rpt.pop(index)
                match = True