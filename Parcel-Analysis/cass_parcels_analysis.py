# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 09:27:33 2023
Last Updated on Wed Mar 8 2023

@author: Dominic Van Cleave-Schottland
"""
"""
The below code matches Labeled ASTs with Tier II tanks based on the parcels each
tank are in (in Cass County, Nebraska). It is a first version of Parcel Analysis;
other scripts produced much better results. 
"""
#%% Import Librariess
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry import mapping

#%% Get polygons (parcels) and points (tank locations)
parcels = gpd.GeoDataFrame.from_file('Cass_Parcels_4326.shp')

cass_label_data_xlsx = pd.read_excel('Cass.xlsx')
cass_label_data_xlsx.to_csv('Cass.csv', index = None, header = True)
cass_label_data = pd.read_csv('Cass.csv')

# Extracting only tanks in Douglas County
cass_tanks_lat = cass_label_data['0']
cass_tanks_long = cass_label_data['1']
           
# Create a Data Frame with the tank points (ie center of tanks)
df = pd.DataFrame({'lon':(pd.Series(cass_tanks_long)).to_numpy(), 'lat':(pd.Series(cass_tanks_lat)).to_numpy()})
df['coords'] = list(zip(df['lon'],df['lat']))
df['coords'] = df['coords'].apply(Point)
tanks = gpd.GeoDataFrame(df, geometry='coords', crs=parcels.crs)

# Perform spatial join to match points and polygons
pointInPolys = gpd.tools.sjoin(tanks, parcels, predicate="within", how='left')

# Plot
base = parcels.boundary.plot(linewidth=0.1, edgecolor="black", alpha = 0.5)
tanks.plot(ax=base, color="blue", markersize=1)
# base.set_xlim([-95.95, -95.85])
# base.set_ylim([40.94, 41.02])
plt.show()

# Extract Columns
    # Want 'lon', 'lat', 'OwnerName1'
cass_refined = pointInPolys.loc[:,"lon":"lat"]
cass_refined["OwnerName"] = pointInPolys.loc[:,"OwnerName1"]
    # TEMP FIX # 
cass_refined["OwnerName"][100] = "FRONTIER COOPERATIVE CO"

# Load in Tier II Data with Chemicals & Facility Name
neb_tier2_data = pd.read_csv('Nebraska_TierII_data.csv', encoding="ISO-8859-1", low_memory=False)
neb_facnam_normal = neb_tier2_data['FACNAM'].tolist()
neb_facnam = [x.lower() for x in neb_facnam_normal]
neb_chem = neb_tier2_data['CHMSRT'].tolist()
neb_rpt = neb_tier2_data['RPTNAM'].tolist()
neb_lat = neb_tier2_data['Lat'].tolist()
neb_lon = neb_tier2_data['Long'].tolist()

# Initialize Sets
cass_chemicals = []
owner_indicies = []
match = False

# Go through all parcels with tanks in them and see if any Tier II tank locations
# are in or around these parcels, indicating a match
for j in range(0, len(cass_refined)):
    cass_tank_lat = cass_refined['lat'][j]
    cass_tank_lon = cass_refined['lon'][j]
    cass_tank_fac = cass_refined["OwnerName"][j].lower()
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