# Fall 2022 Thesis Work (Borsuk Lab)
Thesis work under Celine Robinson's PhD dissertation. 
Please direct all questions to either myself (dav12@duke.edu) or Celine Robinson (celine.robinson@duke.edu)

## LabelImg Data
Due to the limits of uploading on GitHub, I am unable to upload both the original .json file and the fixed .json file. As of writing this (May 2023), I am unsure on whether or not this file is even public information. These files are only used in two of the python scripts above but are an essential part of said files.

## Spatial Matching
This folder contains all scripts used for the Spatial Matching method of analysis, wherein Labeled ASTs were matched to other datasets via the distance from these ASTs and the coordinates given for the other datasets. On limitation of this method is that sometimes the coordinates and street addresses of these other datasets do not align and therefore the accuracy of this method is questionable without manually checking the results in ArcGIS or Google Maps. 

## Parcel Analysis
This folder contains all scripts used for the Parcel Analysis method, wherein Labeled ASTs were matched to other datasets via the parcels these ASTs resided in. This method is much more robust than the Spatial Matching method, however for Nebraska, the results are quite limited. 
<br> The Parcel Analysis method would benefit from more data on where tanks are supposed to be, specifically data from major oil and gas companies about their facilities and what chemicals they house. This line of analysis was only briefly pursued as of May 2023 but using ArcGIS, it is obvious this method would help a great deal. 
