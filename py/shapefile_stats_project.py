'''20230630 
Given two shapefile (A) and (B) which are assumed to have the same (mostly the same) attributes and for this application, (A) is in fact a small clipped area of the larger one (B):

Produce a third shapefile (C) which has a numerical value expresssing closeness between the same polygonal footprint's attributes vs. the aggregated attributes over the shapefile (A)
'''
import matplotlib.pyplot as plt
from misc import err, exists
from osgeo import ogr
import numpy as np
import sys
import os

shapefile_path1 = sys.argv[1] # A) open shapefile
shapefile_path2 = sys.argv[2] # B) 

if not exists(shapefile_path1):
    err("could not find input file:", shapefile_path1)
if not exists(shapefile_path2):
    err("could not find input file:", shapefile_path2)

driver = ogr.GetDriverByName('ESRI Shapefile')
dataset = driver.Open(shapefile_path1, 0)  # 0 means read-only mode

types, values = set(), {}
layer = dataset.GetLayer()
feature = layer.GetNextFeature()  # iterate features for shapefile 1.
while feature is not None:  # attributes of the feature
    attributes = feature.items()
    for k in attributes:
        types.add(type(attributes[k]))
        v = attributes[k]
        if k not in values:
            values[k] = {}
        if v not in values[k]:
            values[k][v] = 0
        values[k][v] += 1
    # geometry = feature.GetGeometryRef() # print(geometry.ExportToWkt()) 
    feature = layer.GetNextFeature()  # next feature
dataset = None # close shapefile

# normalize the counts to add to 1 for each attribute
for k in values:
    total = 0.
    for v in values[k]:
        total += values[k][v]
    # make it add to 1.
    for v in values[k]:
        values[k][v] /= total

# open the second shapefile
dataset2 = driver.Open(shapefile_path2, 0)  # 0 means read-only mode
layer2 = dataset2.GetLayer()
feature2 = layer2.GetNextFeature()  # iterate features for shapefile 1.

while feature2 is not None:  # attributes of the features
    values2 = {}  # vector for this feature only, not aggregate
    attributes2 = feature2.items()
    for k in attributes2:
        v = attributes2[k]
        if k not in values2:
            values2[k] = {}
        if v not in values2[k]:
            values2[k][v] = 0
        values2[k][v] += 1
    # geometry = feature.GetGeometryRef() # print(geometry.ExportToWkt()) 
    feature2 = layer2.GetNextFeature()  # next feature

    # print(values)
    # print(values2)

    metric, n_terms = 0., 0.
    for k in values:
        if k in values2:
            for v in values2[k]:
                if v in values[k]:
                    metric += values[k][v] * values2[k][v]   # always <= 1.
                    n_terms += 1.
                    if values2[k][v] != 1.:
                        err("this quantity should always be 1.")
    metric /= n_terms  # total value should be <= 1.
    print("metric", metric)

    # do the dot-producty bit here:
    # don't penalize for stuff we don't have. Only add on for stuff we do have!
    # want 1. if we have the same proportion for everything. Otherwise, less than that.


    # add the numerical value into the new shapefile!
# Close the shapefile
dataset2 = None




'''



for k in values:
    print(values[k])

    labels = list(values[k].keys())
    n_keys = len(labels)

    has_none = False
    stuff = [[labels[i], values[k][labels[i]]] for i in range(len(labels))]
    for i in range(len(stuff)):
        if labels[i] == None:
            has_none = True

    if has_none:
        for i in range(len(stuff)):
            stuff[i][0] = str(stuff[i][0])
'''
