# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 19:26:46 2023
Last Updated on Wed Feb 15 2023

@author: Dominic Van Cleave-Schottland
"""
"""
The below code attempts (but fails) to tackle the spatial matching problem
with Vornoi Tessellation. Here, I try to use the example found in the following
article:
    
https://towardsdatascience.com/how-to-create-voronoi-regions-with-geospatial-data-in-python-adbb6c5f2134

More on Vornoi Tessellation in Python can be found here:
    
https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html

"""
import fiona
import shapely.geometry as geometry
import pylab as pl
import matplotlib.pyplot as plt
import scipy
from shapely.ops import voronoi_diagram

input_shapefile = 'tile_level_annotations.shp'
shapefile = fiona.open(input_shapefile)
points = [geometry.shape(point['geometry']) for point in shapefile]
print("We have {0} points!".format(len(points)))

xs = [point.xy[0] for point in points]
ys = [point.xy[1] for point in points]
#plt.scatter(xs, ys)

scipy.spatial.Voronoi(points)