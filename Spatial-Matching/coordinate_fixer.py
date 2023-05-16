# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 12:15:46 2023
Last Updated on May 16 2023

@author: domin
"""
"""
Very simply, the code below ensures the shp files used in the other scripts 
use the same EPSG Geodetic Parameter Dataset. EPSG 4326 is a common code and
is used in Global Positioning Systems (GPS) around the world. 
"""

import geopandas

# import data from shape file
data = geopandas.read_file("YOUR_SHP_FILE.shp")
# change CRS to epsg 4326
data = data.to_crs(epsg=4326)
# write shp file
data.to_file("YOUR_SHP_FILE_4326.shp")