# -*- coding: utf-8 -*-
"""
Created on Fri Mar  24 09:27:33 2023
Last Updated on Fri Mar 24 2023

@author: Dominic Van Cleave-Schottland
"""
"""
Parcel Analysis in Cass County with TRI data points
"""
#%% Import Librariess
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

#%% Get parcel data, labeled tank data, and TRI data
parcels = gpd.GeoDataFrame.from_file('Cass_Parcels_4326.shp')

# Cleaning up the Parcel Data
parcels_filt_pd = pd.DataFrame({'ParID':parcels.OBJECTID, 
                             'ParCity':parcels.SitusCity,
                             'ParStrAdd':parcels.SitusAddre,
                             'ParFullAdd':parcels.FullSitusA,
                             'ParOwner':parcels.OwnerName1,
                             'ParLeng':parcels.SHAPE_Leng,
                             'ParArea':parcels.SHAPE_Area,
                             'ParGeom':parcels.geometry})
parcels_filt = gpd.GeoDataFrame(parcels_filt_pd, geometry='ParGeom')

all_tanks = gpd.GeoDataFrame.from_file('tile_level_annotations.shp')
all_tanks['full_fip'] = all_tanks.state_fips + all_tanks.county_fip
cass_tanks = all_tanks[all_tanks['full_fip']=='31025'] 
    #31025 is the code for Nebraska (31) and Cass County (025)
    
# Cleaning up the Tank Data
cass_tanks.rename(columns={'diameter (':'diameter'}, inplace=True)
cass_filt_pd = pd.DataFrame({'TileName':cass_tanks.tile_name, 
                             'TankID':(pd.Series(np.linspace(1, len(cass_tanks), len(cass_tanks)))).to_numpy(),
                             #'TankCenLat':cass_tanks.centroid_1,
                             #'TankCenLon':cass_tanks.centroid_l,
                             'TankCen':list(zip(cass_tanks.centroid_l, cass_tanks.centroid_1)),
                             'TankType':cass_tanks.object_cla,
                             'TankDiam':cass_tanks.diameter,
                             'TankGeom':cass_tanks.geometry})
cass_filt = gpd.GeoDataFrame(cass_filt_pd, geometry='TankGeom')

cass_tri_data = pd.read_csv('tri_2020_cass.csv')
cass_tri_pd = pd.DataFrame({'TRIid':cass_tri_data['2. TRIFD'],
                            'TRIFacName':cass_tri_data['4. FACILITY NAME'],
                            'TRIAdd':str(cass_tri_data['5. STREET ADDRESS']) + ' ' 
                                        + cass_tri_data['6. CITY'] + ' '
                                        + cass_tri_data['8. ST'] + ' '
                                        + str(cass_tri_data['9. ZIP']),
                            'TRICent':list(zip(cass_tri_data['13. LONGITUDE'], cass_tri_data['12. LATITUDE'])),
                            'TRIParCo':cass_tri_data['15. PARENT CO NAME'],
                            'TRISector':cass_tri_data['20. INDUSTRY SECTOR'],
                            'TRIChem':cass_tri_data['34. CHEMICAL']})
cass_tri_pd['TRIGeom'] = cass_tri_pd['TRICent'].apply(Point)
cass_tri = gpd.GeoDataFrame(cass_tri_pd, geometry='TRIGeom', crs=parcels.crs)

cass_tri_lon = cass_tri_data['13. LONGITUDE'].tolist()
cass_tri_lat = cass_tri_data['12. LATITUDE'].tolist()

#%% Sjoin the Parcel data with the Labeled Tank data to find all Parcels with tanks (contained full within)
cass_parcels_tanks = gpd.tools.sjoin(parcels_filt, cass_filt, predicate="contains", how="inner")
        # "Contains" --> 111 tanks
        # "Intersects" --> 126 tanks
        # len(cass_filt) --> 119 tanks !!!!
cass_parcels_tanks.rename(columns={'index_right':'MatchTankID'}, inplace=True)

cass_partank = gpd.GeoDataFrame(cass_parcels_tanks, geometry='ParGeom')

# Add a buffer to the parcels with tanks in them
cass_partank.buffer(0.0002)

#%% Spatial join to match ParTank df and TierII Points
cass_tri_partank = gpd.tools.sjoin(cass_partank, cass_tri, predicate="contains", how='inner')
    # left = geometry to keep (parcel)
cass_tri_partank.rename(columns={'index_right':'MatchFacIndex'}, inplace=True)

#%% Plotting (purely to check work)
# Cass County Tanks
cass_tanks_x = []
cass_tanks_y = []
for coord in list(cass_filt.TankCen):
    cass_tanks_x.append(coord[0])
    cass_tanks_y.append(coord[1])
    
# # Matching Tier II Facilities
# tierii_x = []
# tierii_y = []
# for coord in list(cass_tierii_partank.TierIICoords):
#     if coord[0] not in tierii_x and coord[1] not in tierii_y:
#         tierii_x.append(coord[0])
#         tierii_y.append(coord[1])
    
# Plot
plt.figure(figsize=(100,50))
base = parcels.boundary.plot(linewidth=0.1, edgecolor="black", alpha = 0.5)
plt.scatter(cass_tanks_x, cass_tanks_y, c='blue', s=1)
plt.scatter(cass_tri_lon, cass_tri_lat, c='red', alpha=0.75, s=5)
#plt.scatter(tierii_x, tierii_y, c='green', s=2)

# base.set_xlim([-96.448, -96.44])
# base.set_ylim([40.96, 40.97])
plt.show()