'''20230605 sentinel2_extract_swir.py'''
from envi import envi_header_cleanup
from misc import err, args, exist, run
from osgeo import gdal
import numpy as np
import sys
import os

if not exist(args[1]): err('could not open input file: ' + d)
if not args[1][-4:] == '.zip': err('zip expected')

w = args[1].split('_')  # split filename on '_'
ds = w[2].split('T')[0]  # date string
stack_fn = args[1][:-4] + '.bin' # output stack filename

def ignore_warnings(x, y, z): pass 
gdal.PushErrorHandler(ignore_warnings)  # suppress warnings

d = gdal.Open(args[1])
subdatasets =  d.GetSubDatasets()
desired_metadata = [{"BANDNAME": "B12"},
                    {"BANDNAME": "B11"},
                    {"BANDNAME": "B9"}]
sbs={}
arrays = {}
selected_bands = []
for subdataset in d.GetSubDatasets():  # select bands
    subdataset_path = subdataset[0]
    subdataset_dataset = gdal.Open(subdataset_path)

    for i in range(1, subdataset_dataset.RasterCount + 1):
        band = subdataset_dataset.GetRasterBand(i)
        band_metadata = band.GetMetadata()

        for k in band_metadata:
            for j in desired_metadata:
                try:
                    if band_metadata[k] == j[k]:  # print("Selected: ", band_metadata)
                        selected_bands += [[band, band_metadata, subdataset_dataset]]
                        sbs[band_metadata['BANDNAME']] = selected_bands[-1]
                        arrays[str(band_metadata)] = band.ReadAsArray().astype(np.float32)
                except: pass

selected_bands = [sbs['B12'], sbs['B11'], sbs['B9']]  # reorder band selection

resampled_bands = []
target_sub_ds = selected_bands[0][2]
geo_xform = target_sub_ds.GetGeoTransform()
target_xs, target_ys = geo_xform[1], geo_xform[5]
driver = gdal.GetDriverByName('ENVI')
stack_ds = driver.Create(stack_fn, target_sub_ds.RasterXSize, target_sub_ds.RasterYSize, 3, gdal.GDT_Float32)
stack_ds.SetProjection(target_sub_ds.GetProjection())
stack_ds.SetGeoTransform(target_sub_ds.GetGeoTransform())

bi = 1
for [band, m, sub_dataset] in selected_bands:
    band_name = m['BANDNAME']
    geotransform = sub_dataset.GetGeoTransform()
    px_sx, px_sy = geotransform[1], geotransform[5]
   
    if band_name == "B9":
        mem_driver = gdal.GetDriverByName('MEM')
        input_ds = mem_driver.Create('', band.XSize, band.YSize, 1, gdal.GDT_Float32)
        input_ds.SetGeoTransform(sub_dataset.GetGeoTransform())
        input_ds.SetProjection(sub_dataset.GetProjection())
        input_ds.GetRasterBand(1).WriteArray(arrays[str(m)]) 
        
        resampled_geotransform = list(input_ds.GetGeoTransform())
        resampled_geotransform[1] = target_xs
        resampled_geotransform[5] = target_ys
        resampled_ds = mem_driver.Create('', target_sub_ds.RasterXSize, target_sub_ds.RasterYSize, 1, gdal.GDT_Float32) 
        resampled_ds.SetGeoTransform(resampled_geotransform)
        resampled_ds.SetProjection(input_ds.GetProjection())

        gdal.Warp(resampled_ds, input_ds, xRes=target_xs, yRes=target_ys, resampleAlg='bilinear')
        arrays[str(m)] = resampled_ds.GetRasterBand(1).ReadAsArray() 
        resampled_ds = None
        input_ds = None

    rb = stack_ds.GetRasterBand(bi)
    rb.WriteArray(arrays[str(m)])
    rb.SetDescription(' '.join([ds,  # dates string
                                str(int(px_sx)) + 'm:',  # resolution
                                band_name,   # band name and wavelength
                                str(m['WAVELENGTH']) + str(m['WAVELENGTH_UNIT'])]))
    arrays[str(m)] = None 
    bi += 1 

stack_ds = None
hdr_f =  args[1][:-4] + '.hdr'
envi_header_cleanup([None, hdr_f])
xml_f = stack_fn + '.aux.xml'
hdr_b = hdr_f + '.bak'
for f in [xml_f, hdr_b]:
    if os.path.exists(f):
        os.remove(f)
run('raster_zero_to_nan ' + stack_fn)
