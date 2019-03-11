import matplotlib.pyplot as plt
import skimage.io
import numpy as np
from roipoly import RoiPoly
plt.ion()
#this needs to be set to be location of your tif file.
data_path= '/Users/tim/python_packages/2p_imaging/example_data/'

#read in tif file
im=skimage.io.imread(data_path + 'Streaming Phasor Capture - 5_XY0_Z0_T00_C0.tif')

#take mean of file across all time points
im_mean=np.mean(im,axis=0)

#plt.colormap('hot')
plt.figure()
#restrict the area to relevant 100x100 pixel region
im_cut=im_mean[150:250,150:250]
plt.imshow(im_cut)
zoom_xlim=[150,230]
zoom_ylim=[250,140]

#plot scale bar
microns_per_pixel=1.47441
pixels_in_50_microns=50./microns_per_pixel
init_scale_height=80
init_scale_x=60
plt.plot([init_scale_x,init_scale_x+pixels_in_50_microns],[init_scale_height, init_scale_height])


#choose roi
print('press ENTER when ROI completed')
my_roi=RoiPoly(color='c')

input()
my_roi.display_roi()

mask1=my_roi.get_mask(im_cut)

im_cut_all=im[:,150:250,150:250]


num_frames=len(im_cut_all[:,0,0])
mn_roi1=[]
for crframe in np.arange(num_frames):
	mn_roi1.append(np.mean(im_cut_all[crframe,mask1]))
	

###
#now plot the means over time in the region of interest
####

#here I don't plot 10th-13th frame b/c that's when stimulation occurs.
plt.figure()
tmlapse_in_s=.11963
xvls=np.arange(0,40*tmlapse_in_s,tmlapse_in_s)
plt.plot(xvls[0:9],mn_roi1[0:9],'c')
plt.plot(xvls[14:],mn_roi1[14:],'c')
#plt.plot(xvls[0:9],mn_roi2[0:9],'g')
#plt.plot(xvls[14:],mn_roi2[14:],'g')
plt.ylim([0,5000])
plt.xlim([0,5])


#Load GCAMP tif...
#im_gcamp=skimage.io.imread(data_path+'A08aGCaMP_SuccessfulStim_AcquisitionPlane_XY0_Z0_T0_C0.tif')
#im_chrimson=skimage.io.imread(data_path+'dbdChrimson_SuccessfulStim_StimPlane_XY0_Z0_T0_C0.tif')

#first plot average pixel intensity


#then plot variance of pixel intensity