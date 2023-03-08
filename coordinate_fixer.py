# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 12:15:46 2023

@author: domin
"""

import geopandas

data = geopandas.read_file("Cass_Parcels.shp")
# change CRS to epsg 4326
data = data.to_crs(epsg=4326)
# write shp file
data.to_file("Cass_Parcels_4326.shp")