# -*- coding: utf-8 -*-
"""
Created on Tues May 16    2023 09:27:33 2023
Last Updated on Tues May 16 2023

@author: Dominic Van Cleave-Schottland
"""
"""
Parcel Analysis in X County with Y data points
"""
#%% Import Librariess
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

#%% Get parcel data, labeled tank data, and TRI data
parcels = gpd.GeoDataFrame.from_file('YOUR_PARCEL_DATA_4326.shp')
    ### PLEASE USE COORDINATE FIXER FILE TO ENSURE CORRECT ESPG ###

# Cleaning up the Parcel Data
parcels_filt_pd = pd.DataFrame({'ParData1':parcels.ParData11, 
                             'ParData2':parcels.ParData22,
                                    ...
                             'ParGeom':parcels.geometry})
        ## TO FIND WHAT DATA FROM THE PARCELS YOU NEED, YOU SHOULD SEPARATELY
        ## IMPORT THE PARCEL DATA IN THE CONSOLE USING :
        ##
        ## import geopandas as gpd
        ## parcel_data = gpd.GeoDataFrame.from_file('YOUR_PARCEL_DATA_4326.shp')
        ## parcel_data.columns
        ## 
        ## AND SEE WHAT THE COLUMNS NAMES ARE CALLED

# Making sure the geometry lines up
parcels_filt = gpd.GeoDataFrame(parcels_filt_pd, geometry='ParGeom')

# Import Labeled Tank Data
all_tanks = gpd.GeoDataFrame.from_file('YOUR_LABELED_TANK_DATA.shp')

# Filtering Tank data by FIP
### PLEASE ONLY DO THIS IF YOUR TANK DATA HAS FIPS DATA
all_tanks['full_fip'] = all_tanks.state_fips + all_tanks.county_fip
county_tanks = all_tanks[all_tanks['full_fip']=='XXYYY'] 
    #XXYYY is the code for <insert state> (XX) and <insert county> (YYY)
    # fips data by county can be found in the repo
    
# Cleaning up the Tank Data
### USE SAME METHOD AS ABOVE TO DETERMINE WHAT DATA/COLUMNS TO KEEP
county_filt_pd = pd.DataFrame({'TileName':county_tanks.tile_name, 
                                  ...
                             'TankGeom':county_tanks.geometry})
county_filt = gpd.GeoDataFrame(county_filt_pd, geometry='TankGeom')

# Cleaning up Imported Tank Data Set
county_tri_data = pd.read_csv('tri_2020_county.csv') # may be different if not using csv
county_tri_pd = pd.DataFrame({'TRIid':county_tri_data['2. TRIFD'],
                              ....
                              })
county_tri_pd['TRIGeom'] = county_tri_pd['TRICent'].apply(Point)
county_tri = gpd.GeoDataFrame(county_tri_pd, geometry='TRIGeom', crs=parcels.crs)

county_tri_lon = county_tri_data['13. LONGITUDE'].tolist()
county_tri_lat = county_tri_data['12. LATITUDE'].tolist()

#%% Sjoin the Parcel data with the Labeled Tank data to find all Parcels with tanks (contained full within)
county_parcels_tanks = gpd.tools.sjoin(parcels_filt, county_filt, predicate="contains", how="inner")
        # "Contains" --> fully within
        # "Intersects" --> geometries only intersect
county_parcels_tanks.rename(columns={'index_right':'MatchTankID'}, inplace=True)

county_partank = gpd.GeoDataFrame(county_parcels_tanks, geometry='ParGeom')

# Add a buffer to the parcels with tanks in them
county_partank.buffer(0.0002)

#%% Spatial join to match ParTank df and TierII Points
county_tri_partank = gpd.tools.sjoin(county_partank, county_tri, predicate="contains", how='inner')
    # left = geometry to keep (parcel)
county_tri_partank.rename(columns={'index_right':'MatchFacIndex'}, inplace=True)

#%% Plotting (purely to check work)
# county County Tanks
county_tanks_x = []
county_tanks_y = []
for coord in list(county_filt.TankCen):
    county_tanks_x.append(coord[0])
    county_tanks_y.append(coord[1])
    
# # Matching Tier II Facilities
# tierii_x = []
# tierii_y = []
# for coord in list(county_tierii_partank.TierIICoords):
#     if coord[0] not in tierii_x and coord[1] not in tierii_y:
#         tierii_x.append(coord[0])
#         tierii_y.append(coord[1])
    
# Plot
plt.figure(figsize=(100,50))
base = parcels.boundary.plot(linewidth=0.1, edgecolor="black", alpha = 0.5)
plt.scatter(county_tanks_x, county_tanks_y, c='blue', s=1)
plt.scatter(county_tri_lon, county_tri_lat, c='red', alpha=0.75, s=5)
#plt.scatter(tierii_x, tierii_y, c='green', s=2)

# base.set_xlim([-96.448, -96.44])
# base.set_ylim([40.96, 40.97])
plt.show()