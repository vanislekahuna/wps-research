# use fastclust library https://pypi.org/project/fastcluster/ for unsupervised learning on an image (next: object-based version). Tested with python 2.7 on ubuntu
# this adapts our initial work here: https://github.com/franarama/satellite-clustering/blob/hierarchical-clustering/cluster.py

# e.g.
# python py/fast_cluster_tiling.py  data/fran/mS2.bin 10 50 10

from misc import *

def impt(lib):
    try: exec('import ' + lib)
    except:
        raw_input("pls. press ENTER to install " + lib + " (or ctrl-C to exit)" + 
                "\n\nnote: if you get any error, \n" +
                "pls. try to run fast_clust.py once more after.)\n")
        try: os.system('pip install ' + lib)
        except: err("please run application again")

impt('numpy'); import numpy as np
impt('fastcluster'); import fastcluster as fc
impt('matplotlib'); import matplotlib.pyplot as plt 
impt('gdal'); from osgeo import gdal, gdal_array
impt('scipy'); from scipy.cluster.hierarchy import dendrogram, linkage

# Tell GDAL to throw Python exceptions, and register all drivers
gdal.UseExceptions()
gdal.AllRegister()
n_clusters, tile_size, border_size = None, None, None

try: image, n_clusters, tile_size, border_size = args[1], int(args[2]), int(args[3]), int(args[4])
except: err("Usage: python fastcluster.py [image file name .bin] [n clusters desired]" +
            "[square tiles: number of pixels n (tile size: n x n)] " +
            "[border size around tile: number of pixels]")

# Read in raster image
img_ds = gdal.Open(image, gdal.GA_ReadOnly)

# allocate memory to reshape image
img = np.zeros((img_ds.RasterYSize,  # number of rows
                img_ds.RasterXSize,  # number of cols
                img_ds.RasterCount),  # number of bands
                gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType)) # data type code # warning: assumed the raster bands were all the same type (should be true)

# reshape the image band by band (NRow, NCol, NBand)
for b in range(img.shape[2]): img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()

ncol, nrow, nband = img.shape
print "img.shape", nrow, ncol, nband

rx, ry = ncol / tile_size, nrow / tile_size
ntile_x = rx if ncol % tile_size == 0 else rx + 1
ntile_y = ry if nrow % tile_size == 0 else ry + 1

print "ntilex", ntile_x, "ntiley", ntile_y

for x in range(0, ntile_x):
    x_start = x * tile_size
    x_end = min(x_start + tile_size - 1, ncol - 1)
    x_size = x_end - x_start + 1

    for y in range(0, ntile_y):
        y_start = y * tile_size
        y_end = min(y_start + tile_size - 1, nrow - 1)
        y_size = y_end - y_start + 1        
        print "x_size", x_size, "y_size", y_size

        plt.figure()
        img2 = img[int(x_start): int(x_end), int(y_start): int(y_end),:]
        plt.imshow(twop_str(img2))
        plt.tight_layout()
        plt.show()
err("done")

# reshape image again to match expected format for scikit-learn (NRow * NCol, NBand)
new_shape = (img.shape[0] * img.shape[1], img.shape[2])
X = img[:, :, :img.shape[2]].reshape(new_shape)


# use fastcluster.linkage instead of scipy.cluster.hierarchy.linkage
print "calculating linkage.."
Z = fc.linkage(X, 'ward')

print "calculating dendrogram.."
fig = plt.figure(figsize=(10, 10)) # 25, 10
plt.title('hierarchical clustering dendrogram')
rotate = False

plt.ylabel('distance' if (not rotate) else 'index')
plt.xlabel('index' if (not rotate) else 'distance')
dn = dendrogram(Z,
        #truncate_mode='lastp',
        #p = n_clusters,
        leaf_rotation = 0. if rotate else 90.,
        show_contracted=True,
        orientation='right' if rotate else 'top',
        distance_sort='descending',
        show_leaf_counts=True)

print "saving figure.."
plt.savefig(image + "_fastcluster.png")

print "extracting labels.."
from scipy.cluster.hierarchy import fcluster
labels = fcluster(Z, n_clusters, criterion='maxclust') ##criterion='distance')

labels=labels.reshape(img[:, :, 0].shape)
plt.figure(figsize=(20, 20))
print "min, max", np.min(labels), np.max(labels)
plt.imshow(labels) #, cmap ='jet')
#plt.colorbar()
plt.tight_layout() #plt.show()
plot_file = image + "_labels.png"

print "plot written to file: " + plot_file
plt.savefig(plot_file, orientation='portrait')

samples, lines, bands = read_hdr(hdr_fn(args[1]))
write_binary(labels, args[1] + "_fastclust.bin")
write_hdr(args[1] + "_fastclust.hdr", samples, lines, 1)

'''
the below from https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fcluster.html
criterionstr, optional
    The criterion to use in forming flat clusters. This can be any of the following values:

inconsistent: if a cluster node and all its descendants have an inconsistent value less than or equal to t then all its leaf descendants belong to the same flat cluster. When no non-singleton cluster meets this criterion, every node is assigned to its own cluster. (Default)

distance: Forms flat clusters so that the original observations in each flat cluster have no greater a cophenetic distance than t.
        
maxclust: Finds a minimum threshold r so that the cophenetic distance between any two original observations in the same flat cluster is no more than r and no more than t flat clusters are formed.
        
monocrit: Forms a flat cluster from a cluster node c with index i when monocrit[j] <= t.

            For example, to threshold on the maximum mean distance as computed in the inconsistency matrix R with a threshold of 0.8 do:

            MR = maxRstat(Z, R, 3)
            cluster(Z, t=0.8, criterion='monocrit', monocrit=MR)

maxclust_monocrit: Forms a flat cluster from a non-singleton cluster node c when monocrit[i] <= r for all cluster indices i below and including c. r is minimized such that no more than t flat clusters are formed. monocrit must be monotonic. For example, to minimize the threshold t on maximum inconsistency values so that no more than 3 flat clusters are formed, do:

            MI = maxinconsts(Z, R)
            cluster(Z, t=3, criterion='maxclust_monocrit', monocrit=MI)
'''
