from cuda_slic import slic
from skimage import data

# 2D RGB image
img = data.astronaut() 
labels = slic(img, n_segments=100) # , compactness=10)

# 3D gray scale
#vol = data.binary_blobs(length=50, n_dim=3, seed=2)
#labels = slic(vol, n_segments=100, multichannel=False, compactness=0.1)

# 3D multi-channel
# volume with dimentions (z, y, x, c)
# or video with dimentions (t, y, x, c)
#vol = data.binary_blobs(length=33, n_dim=4, seed=2)
#labels = slic(vol, n_segments=100, multichannel=True, compactness=1)

import matplotlib.pyplot as plt
plt.imshow(img)
plt.savefig("img.png")
plt.imshow(labels)
plt.savefig("labels.png")
