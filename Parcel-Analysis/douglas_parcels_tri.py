# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 16:30:42 2023
Last Updated on Sat Apr  8 2023

@author: Dominic Van Cleave-Schottland
"""
"""
Parcel Analysis in Douglas County with TRI data points
"""
#%% Import Librariess
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

#%% Get parcel data, labeled tank data, and TRI data
parcels = gpd.GeoDataFrame.from_file('Douglas_Parcels_4326.shp')

# Cleaning up the Parcel Data
parcels_filt_pd = pd.DataFrame({'ParID':parcels.OBJECTID, 
                             'ParCity':parcels.OWNER_CITY,
                             'ParStrAdd':parcels.ADDRESS2,
                             'ParFullAdd':parcels.PROPERTY_A,
                             'ParOwner':parcels.OWNER_NAME,
                             'ParLeng':parcels.SHAPESTLen,
                             'ParArea':parcels.SHAPESTAre,
                             'ParGeom':parcels.geometry})
parcels_filt = gpd.GeoDataFrame(parcels_filt_pd, geometry='ParGeom')

all_tanks = gpd.GeoDataFrame.from_file('tile_level_annotations.shp')
all_tanks['full_fip'] = all_tanks.state_fips + all_tanks.county_fip
douglas_tanks = all_tanks[all_tanks['full_fip']=='31055'] 
    #31025 is the code for Nebraska (31) and Douglas County (055)
    
# Cleaning up the Tank Data
douglas_tanks.rename(columns={'diameter (':'diameter'}, inplace=True)
douglas_filt_pd = pd.DataFrame({'TileName':douglas_tanks.tile_name, 
                             'TankID':(pd.Series(np.linspace(1, len(douglas_tanks), len(douglas_tanks)))).to_numpy(),
                             #'TankCenLat':douglas_tanks.centroid_1,
                             #'TankCenLon':douglas_tanks.centroid_l,
                             'TankCen':list(zip(douglas_tanks.centroid_l, douglas_tanks.centroid_1)),
                             'TankType':douglas_tanks.object_cla,
                             'TankDiam':douglas_tanks.diameter,
                             'TankGeom':douglas_tanks.geometry})
douglas_filt = gpd.GeoDataFrame(douglas_filt_pd, geometry='TankGeom')

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
douglas_parcels_tanks = gpd.tools.sjoin(parcels_filt, douglas_filt, predicate="intersects", how="inner")
        # "Contains" --> 177 tanks
        # "Intersects" --> 187 tanks
        # len(douglas_filt) --> 155 tanks ???????
douglas_parcels_tanks.rename(columns={'index_right':'MatchTankID'}, inplace=True)

douglas_partank = gpd.GeoDataFrame(douglas_parcels_tanks, geometry='ParGeom')

# Add a buffer to the parcels with tanks in them
douglas_partank['TierIIGeom'] = douglas_partank.buffer(0.002) 
        # 0.002 = roughly 0.279 km

#%% Spatial join to match ParTank df and TierII Points
douglas_tri_partank = gpd.tools.sjoin(douglas_partank, ne_tri, predicate="contains", how='inner')
#douglas_tri_partank = gpd.tools.sjoin(parcels_filt, ne_tri, predicate="contains", how='inner')
    # left = geometry to keep (parcel)
    # 42 overlapping TRI tanks when douglas_parcels is "intersects" and "contains"
douglas_tri_partank.rename(columns={'index_right':'MatchFacIndex'}, inplace=True)

#%% Plotting (purely to check work)
# douglas County Tanks
douglas_tanks_x = []
douglas_tanks_y = []
for coord in list(douglas_filt.TankCen):
    douglas_tanks_x.append(coord[0])
    douglas_tanks_y.append(coord[1])
    
# # Matching Tier II Facilities
# tierii_x = []
# tierii_y = []
# for coord in list(douglas_tierii_partank.TierIICoords):
#     if coord[0] not in tierii_x and coord[1] not in tierii_y:
#         tierii_x.append(coord[0])
#         tierii_y.append(coord[1])
    
# Plot
plt.figure(figsize=(100,50))
base = parcels.boundary.plot(linewidth=0.1, edgecolor="black", alpha = 0.5)
plt.scatter(douglas_tanks_x, douglas_tanks_y, c='blue', s=1)
#plt.scatter(douglas_tri_lon, douglas_tri_lat, c='red', alpha=0.75, s=5)
#plt.scatter(tierii_x, tierii_y, c='green', s=2)

# base.set_xlim([-96.448, -96.44])
# base.set_ylim([40.96, 40.97])
plt.show()



