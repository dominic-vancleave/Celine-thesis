# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 13:01:50 2023
Last Updated on Thu Mar 30 2023

@author: Dominic Van Cleave-Schottland
"""
"""
This (unfinished) script aimed to go about Parcel Analysis another way. It is 
unclear if this method is much different than the others. 
"""
#%% Import Librariess
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry import mapping

#%% Get parcel data, labeled tank data, and Tier II data
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

cass_tierii_data = pd.read_csv('Cass_TierII_data.csv')
cass_tierii_lat = cass_tierii_data['LAT'].tolist()
cass_tierii_lon_pos = cass_tierii_data['LON'].tolist()
cass_tierii_lon = [ -x for x in cass_tierii_lon_pos]
cass_tierii_facid = cass_tierii_data['FACID'].tolist()
cass_tierii_facname = cass_tierii_data['FACNAME'].tolist()

#%% Create a Data Frame with the Tier II Data
tierii = pd.DataFrame({'TierIIFacid':(pd.Series(cass_tierii_facid)).to_numpy(), 'TierIIFacname':(pd.Series(cass_tierii_facname)).to_numpy()})
#df = pd.DataFrame({'lon':(pd.Series(cass_tierii_lon)).to_numpy(), 'lat':(pd.Series(cass_tierii_lat)).to_numpy()})
tierii['TierIICoords'] = list(zip(pd.Series(cass_tierii_lon).to_numpy(),pd.Series(cass_tierii_lat).to_numpy()))
tierii['TierIIGeom'] = tierii['TierIICoords'].apply(Point)
cass_tierii = gpd.GeoDataFrame(tierii, geometry='TierIIGeom', crs=parcels.crs)

#%% Add a buffer to the parcels with tanks in them
cass_tierii['TierIIGeom'] = cass_tierii.buffer(0.011) 
        # 0.011 = roughly 1.5 km

#%% Sptial Join the Tier II Buffer geometry with Parcel data to find all Parcels intersecting the buffer region of Tier II facs
cass_tieriibuf_parc = gpd.tools.sjoin(parcels_filt, cass_tierii, predicate="intersects", how="inner")
        # "Contains" --> 11,684 parcels
        # "Intersects" --> 13,329 parcels
        # len(parcels) --> 20,277 parcels
cass_tieriibuf_parc.rename(columns={'index_right':'MatchParcelID'}, inplace=True)

#%% Sptial Join the Parcel data with the Labeled Tank data to find all Parcels with tanks (contained full within)
cass_parcels_tanks = gpd.tools.sjoin(parcels_filt, cass_filt, predicate="contains", how="inner")
        # "Contains" --> 111 tanks
        # "Intersects" --> 126 tanks
        # len(cass_filt) --> 119 tanks !!!!
cass_parcels_tanks.rename(columns={'index_right':'MatchTankID'}, inplace=True)

cass_partank = gpd.GeoDataFrame(cass_parcels_tanks, geometry='ParGeom')

# #%% Spatial join to match ParTank df and TierII Points
# cass_tierii_partank = gpd.tools.sjoin(cass_partank, cass_tierii, predicate="contains", how='inner')
#     # left = geometry to keep (parcel)
# cass_tierii_partank.rename(columns={'index_right':'MatchFacIndex'}, inplace=True)

# #%% Plotting (purely to check work)
# # Cass County Tanks
# cass_tanks_x = []
# cass_tanks_y = []
# for coord in list(cass_filt.TankCen):
#     cass_tanks_x.append(coord[0])
#     cass_tanks_y.append(coord[1])
    
# # Matching Tier II Facilities
# tierii_x = []
# tierii_y = []
# for coord in list(cass_tierii_partank.TierIICoords):
#     if coord[0] not in tierii_x and coord[1] not in tierii_y:
#         tierii_x.append(coord[0])
#         tierii_y.append(coord[1])
    
# # Plot
# plt.figure(figsize=(100,50))
# base = parcels.boundary.plot(linewidth=0.1, edgecolor="black", alpha = 0.5)
# #plt.scatter(cass_tanks_x, cass_tanks_y, c='blue', alpha=0.5, s=1)
# plt.scatter(cass_tierii_lon, cass_tierii_lat, c='red', s=10)
# #plt.scatter(tierii_x, tierii_y, c='green', s=5)

# # base.set_xlim([-95.93, -95.85])
# # base.set_ylim([40.96, 41.02])
# plt.show()