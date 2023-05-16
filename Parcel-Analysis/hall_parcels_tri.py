# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 09:42:11 2023
Last Updated on Fri Apr  7 2023

@author: Dominic Van Cleave-Schottland
"""
"""
Parcel Analysis in Hall County with TRI data points
"""
#%% Import Librariess
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

#%% Get parcel data, labeled tank data, and TRI data
parcels = gpd.GeoDataFrame.from_file('Hall_Parcels_4326.shp')

# Cleaning up the Parcel Data
parcels_filt_pd = pd.DataFrame({'ParID':parcels.OBJECTID, 
                             'ParAdd':parcels.SITUS,
                             'ParOwner':parcels.CURRENT_OW,
                             'ParLat':parcels.LATITUDE,
                             'ParLon':parcels.LONGITUDE,
                             'ParLeng':parcels.Shape__Len,
                             'ParArea':parcels.Shape__Are,
                             'ParGeom':parcels.geometry})
parcels_filt = gpd.GeoDataFrame(parcels_filt_pd, geometry='ParGeom')

all_tanks = gpd.GeoDataFrame.from_file('tile_level_annotations.shp')
all_tanks['full_fip'] = all_tanks.state_fips + all_tanks.county_fip
hall_tanks = all_tanks[all_tanks['full_fip']=='31079'] 
    #31025 is the code for Nebraska (31) and Hall County (079)
    
# Cleaning up the Tank Data
hall_tanks.rename(columns={'diameter (':'diameter'}, inplace=True)
hall_filt_pd = pd.DataFrame({'TileName':hall_tanks.tile_name, 
                             'TankID':(pd.Series(np.linspace(1, len(hall_tanks), len(hall_tanks)))).to_numpy(),
                             #'TankCenLat':hall_tanks.centroid_1,
                             #'TankCenLon':hall_tanks.centroid_l,
                             'TankCen':list(zip(hall_tanks.centroid_l, hall_tanks.centroid_1)),
                             'TankType':hall_tanks.object_cla,
                             'TankDiam':hall_tanks.diameter,
                             'TankGeom':hall_tanks.geometry})
hall_filt = gpd.GeoDataFrame(hall_filt_pd, geometry='TankGeom')

ne_tri_data = pd.read_csv('tri_2020_ne.csv')
ne_tri_pd = pd.DataFrame({'TRIid':ne_tri_data['2. TRIFD'],
                            'TRIFacName':ne_tri_data['4. FACILITY NAME'],
                            'TRIAdd':str(ne_tri_data['5. STREET ADDRESS']) + ' ' 
                                        + ne_tri_data['6. CITY'] + ' '
                                        + ne_tri_data['8. ST'] + ' '
                                        + str(ne_tri_data['9. ZIP']),
                            'TRICent':list(zip(ne_tri_data['13. LONGITUDE'], ne_tri_data['12. LATITUDE'])),
                            'TRIParCo':ne_tri_data['15. PARENT CO NAME'],
                            'TRISector':ne_tri_data['20. INDUSTRY SECTOR'],
                            'TRIChem':ne_tri_data['34. CHEMICAL']})
ne_tri_pd['TRIGeom'] = ne_tri_pd['TRICent'].apply(Point)
ne_tri = gpd.GeoDataFrame(ne_tri_pd, geometry='TRIGeom', crs=parcels.crs)

ne_tri_lon = ne_tri_data['13. LONGITUDE'].tolist()
ne_tri_lat = ne_tri_data['12. LATITUDE'].tolist()

#%% Sjoin the Parcel data with the Labeled Tank data to find all Parcels with tanks (contained full within)
hall_parcels_tanks = gpd.tools.sjoin(parcels_filt, hall_filt, predicate="intersects", how="inner")
        # "Contains" --> 269 tanks
        # "Intersects" --> 276 tanks
        # len(hall_filt) --> 271 tanks !!!!
hall_parcels_tanks.rename(columns={'index_right':'MatchTankID'}, inplace=True)

hall_partank = gpd.GeoDataFrame(hall_parcels_tanks, geometry='ParGeom')

# Add a buffer to the parcels with tanks in them
hall_partank['TierIIGeom'] = hall_partank.buffer(0.002) 
        # 0.002 = roughly 0.279 km

#%% Spatial join to match ParTank df and TierII Points
#hall_tri_partank = gpd.tools.sjoin(hall_partank, ne_tri, predicate="contains", how='inner')
hall_tri_partank = gpd.tools.sjoin(parcels_filt, ne_tri, predicate="contains", how='inner')
    # left = geometry to keep (parcel)
    # NO overlap betweel tank parcels and TRI parcels in Hall County
hall_tri_partank.rename(columns={'index_right':'MatchFacIndex'}, inplace=True)

#%% Plotting (purely to check work)
# hall County Tanks
hall_tanks_x = []
hall_tanks_y = []
for coord in list(hall_filt.TankCen):
    hall_tanks_x.append(coord[0])
    hall_tanks_y.append(coord[1])
    
# # Matching Tier II Facilities
# tierii_x = []
# tierii_y = []
# for coord in list(hall_tierii_partank.TierIICoords):
#     if coord[0] not in tierii_x and coord[1] not in tierii_y:
#         tierii_x.append(coord[0])
#         tierii_y.append(coord[1])
    
# Plot
plt.figure(figsize=(100,50))
base = parcels.boundary.plot(linewidth=0.1, edgecolor="black", alpha = 0.5)
plt.scatter(hall_tanks_x, hall_tanks_y, c='blue', s=1)
#plt.scatter(hall_tri_lon, hall_tri_lat, c='red', alpha=0.75, s=5)
#plt.scatter(tierii_x, tierii_y, c='green', s=2)

# base.set_xlim([-96.448, -96.44])
# base.set_ylim([40.96, 40.97])
plt.show()
