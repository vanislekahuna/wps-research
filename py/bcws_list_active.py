'''list active fires listed by BCWS over 100 ha '''
import os
import math
import json
import shutil
import zipfile
import datetime
import webbrowser  # https://docs.python.org/3/library/webbrowser.html
import urllib.request
from osgeo import ogr
from bounding_box import bounding_box
from misc import exists, err

# <<<<<<< HEAD
MIN_FIRE_SIZE_HA = 5.
TOP_N = 20 # 150
#=======
#MIN_FIRE_SIZE_HA = 25.
#TOP_N = 20
#>>>>>>> ecd60f74a9bf2e0156b9d247b89a1780e6b61205

selected = []

if __name__ == '__main__':
    # timestamp for archive      
    #t = datetime.datetime.now().strftime("%Y%m%d")  # %H%M%S")  # timestamped backup
    t = datetime.datetime.now().strftime("%Y%m%d%H")  # timestamped backup
    #t = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # timestamped backup
    # save fire polygons
    fn = 'prot_current_fire_polys.zip'
    dl_path = 'https://pub.data.gov.bc.ca/datasets/cdfc2d7b-c046-4bf0-90ac-4897232619e1/' + fn
    urllib.request.urlretrieve(dl_path, fn)
    shutil.copyfile(fn, 'prot_current_fire_polys_' + t + '.zip')
    zipfile.ZipFile(fn).extractall()

    # save fire point locations
    fn = 'prot_current_fire_points.zip'  # download fire data
    dl_path = 'https://pub.data.gov.bc.ca/datasets/2790e3f7-6395-4230-8545-04efb5a18800/' + fn
    urllib.request.urlretrieve(dl_path, fn)
    shutil.copyfile(fn, 'prot_current_fire_points_' + t + '.zip')
    zipfile.ZipFile(fn).extractall()

    # Open Shapefile
    Shapefile = ogr.Open('prot_current_fire_points.shp') # print(Shapefile)
    layer = Shapefile.GetLayer()
    layerDefinition = layer.GetLayerDefn()
    feature_count = layer.GetFeatureCount()
    spatialRef = layer.GetSpatialRef()

    def records(layer):
        for i in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(i)
            yield json.loads(feature.ExportToJson())

    features = records(layer)
    feature_names, feature_ids = [], []
    for f in features:
        for key in f.keys():
            if key == 'properties':
                fk = f[key]
                fire_size = float(fk['CURRENT_SI'])
                
                if False:  # out and larger than MIN_FIRE_SIZE_HA
                    if fk['FIRE_STATU'].lower() != 'out' and fire_size >= MIN_FIRE_SIZE_HA:  # > biggest_size
                        selected.append([fk['CURRENT_SI'], fk])  # selected fires
                        #print(fk)
                if False:
                    if fk['FIRE_STATU'].lower() == 'out':
                        selected.append([fk['CURRENT_SI'], fk])
                if True:  # fire of note
                    if fk['FIRE_STATU'] ==  'Fire of Note':
                        selected.append([fk['CURRENT_SI'], fk])

                if True:  # out of control
                    if fk['FIRE_STATU'] == 'Out of Control':
                        selected.append([fk['CURRENT_SI'], fk])

                if True:  # being held
                    if fk['FIRE_STATU'] == 'Being Held':
                        selected.append([fk['CURRENT_SI'], fk])

selected = list(selected)

# remove duplicates
selected = [json.loads(s) for s in list(set([json.dumps(s) for s in selected]))]

# sort by order of size, largest first
ix = [[selected[i][0], i] for i in range(len(selected))]
ix.sort(reverse=True)
print("ix", ix)
selected = [selected[i[1]] for i in ix]

# select the top TOP_N by size
selected = selected[0: TOP_N]
print(selected)

browser, ci = webbrowser.get('google-chrome'), 0
for s in selected:
    r = s[1]
    lat, lon, size_ha, fire_number = r['LATITUDE'], r['LONGITUDE'], r['CURRENT_SI'], r['FIRE_NUMBE']
    print()
    print(r['CURRENT_SI'], ci + 1, "(" + str(fire_number) + ")", r['GEOGRAPHIC']) #  + '(' + str(r['CURRENT_SI']) + ')')
    # print('\t', type(s[0]), ci, s)

    view_str = ('https://apps.sentinel-hub.com/sentinel-playground/?source=S2L2A&lat=' +
                str(lat) + '&lng=' +
                str(lon) +
                '&zoom=13&preset=CUSTOM&layers=B12,B11,B8A&maxcc=100'
                + '&evalscript=cmV0dXJuIFtCMTIqMi41LEIxMSoyLjUsQjhBKjIuNV0%3D')

    print(view_str)
    # browser.open_new_tab(view_str)

    # A hectare is equal to 10,000 square meters
    # def bounding_box(latitudeInDegrees, longitudeInDegrees, halfSideInKm):
    sq_m = size_ha * 10000.  # square metres area!
    sq_len = math.sqrt(sq_m) # assuming (wrongly) the fire is square, the length/width of the fire
    print("length of square", sq_len)
    sq_len_km = sq_len / 1000. # length of square in km

    bb = bounding_box(lat, lon, 5. * sq_len_km)
    print(bb)
    fp = 'Intersects(POLYGON((-4.53 29.85, 26.75 29.85, 26.75 46.80,-4.53 46.80,-4.53 29.85)))'
    # (57.6532417690325, -127.91022013221782, 57.7504922309675, -127.72821386778217)
    # Intersects(59.76,-129.45)

    fp = [str(bb[1]) + ' ' + str(bb[0]),
          str(bb[1]) + ' ' + str(bb[2]),
          str(bb[3]) + ' ' + str(bb[2]),
          str(bb[3]) + ' ' + str(bb[0]),
          str(bb[1]) + ' ' + str(bb[0])]
    fp = 'Intersects(POLYGON((' + ','.join(fp) + ')))'
    print(fp)
    path = '/media/' + os.popen('whoami').read().strip() + '/disk4/active/'
    if not exists(path):
        path = '/media/' + os.popen('whoami').read().strip() + '/disk2/active/'

    if not exists(path):
        err("path not found:", path)
    
    path += fire_number.strip() + '/'
  
    if True:
        if not os.path.exists(path):
            os.mkdir(path)

        browser.open_new_tab(view_str)

        path += 'fpf'
        if not exists(path):
            print('+w', path)
            open(path,'wb').write(fp.encode())

    ci += 1

    # need to add in OUT of CONTROL fires as well.
