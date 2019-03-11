##pollen grain

import matplotlib.pyplot as plt
import skimage.io
data_path= '/Users/tim/Dropbox/12_17_18_pollen_grain/'
im=skimage.io.imread(data_path + 'Capture 5_XY1545076009_Z0_T000_C0.tif')
plt.figure()
plt.imshow(im)
microns_per_pixel=1.47066
pixels_in_50_microns=50./microns_per_pixel
init_scale_height=130
init_scale_x=160


snp2=plt.imread(data_path+'Snap image - 3_XY0_Z0_T0_C0.tif')
plt.imshow(snp2)
microns_per_pixel=0.241749
pixels_in_50_microns=50./microns_per_pixel
init_scale_height=250
init_scale_x=1200
plt.plot([init_scale_x,init_scale_x+pixels_in_50_microns],[init_scale_height, init_scale_height])

