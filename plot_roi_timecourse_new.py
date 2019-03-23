import matplotlib.pyplot as plt
import file_utilities as util
import skimage.io
import numpy as np
from roipoly import RoiPoly
from py_utilities import tw_filehandling as fh
import pdb



plt.ion()
#this needs to be set to be location of your tif file.
STIM_FLAG=True
#logfile='photo12.txt'
data_path= '/Volumes/LaCie/2pdata/march21/'
stim_meta_dir='photomanipulation_data/'
file_name= '---Streaming Phasor Capture - 5_XY0_Z0_T000_C0.tif'
timelapse_interval=.12579
stim_times=[10,20,30,40,50,60]
heights=[82,161,240,319,399,478]
stim_region={}
colors=['c','g','m','b']
#read in tif file


#im is a dictionary with tifstack and metadata about imaging from PMT

(im,stim)=util.read_in_tif_and_get_metadata(data_path + file_name)

if STIM_FLAG:
    logfile=file_name.split('_')[0]+'.txt'
    stimfile=data_path + stim_meta_dir + logfile
    (stim_depths,stim_times)=util.get_stim_depths(stimfile)
    roi_file=stimfile.split('.txt')[0] + '-points.txt'
    (stim_region['xlist'],stim_region['ylist'])=util.get_stim_region(roi_file)
    
#take mean of file across all time points

im_mean=np.mean(im['tifstack'],axis=0)
fig=plt.figure()
plt.imshow(im_mean,origin='lower')
xtxt=input("Enter desired zoom Xvls e.g. 100,200 ")
ytxt=input("Enter desired zoom Yvls e.g. 100,200 ")

xvls=(float(xtxt.split(',')[0]),float(xtxt.split(',')[1]))
yvls=(float(ytxt.split(',')[0]),float(ytxt.split(',')[1]))

plt.xlim(xvls)
plt.ylim(yvls)
#plt.colormap('hot')
plt.close('all')
#plt.draw()
plt.figure()

im_zoom_mean=im_mean[int(yvls[0]):int(yvls[1]),int(xvls[0]):int(xvls[1])]
im_zoom=im['tifstack'][:,int(yvls[0]):int(yvls[1]),int(xvls[0]):int(xvls[1])]
plt.imshow(im_zoom_mean,origin='lower')


num_rois=input("Enter number of ROIs ")

my_roi=[]
masks=[]
mn_roi={}
for crind in np.arange(int(num_rois)):
    plt.imshow(im_zoom_mean,origin='lower')
    print('press ENTER when ROI completed')
    my_roi.append(RoiPoly(color=colors[crind]))

    input()
    my_roi[-1].display_roi()

for crind in np.arange(int(num_rois)):
    masks.append(my_roi[crind].get_mask(im_zoom_mean))

#im_cut_all=im[:,150:250,150:250]
    

    num_frames=len(im['tifstack'][:,0,0])
    mn_roi[crind]=[]
    for crframe in np.arange(num_frames):
        
        mn_roi[crind].append(np.mean(im_zoom[crframe,masks[-1]]))

#to save to pickle file
#mean_of_Tif
#mn_roi
#masks
sumdt={}
sumdt['im_mean']=im_zoom_mean
sumdt['roi']=my_roi
sumdt['mn_roi']=mn_roi
sumdt['roi_masks']=masks
sumdt['frame_nums']=[int(i) for i in im['frame_nums']]
sumdt['frame_tms']=[float(i) for i in im['time_stamps']]
sumdt['stim_tms']=[float(i.split(':')[-1]) for i in stim_times]
sumdt['stim_depths']=[float(i) for i in stim_depths]
sumdt['stim_region']=stim_region
fh.save_to_pickle(data_path+file_name + '.pck', sumdt)





#Load GCAMP tif...
#im_gcamp=skimage.io.imread(data_path+'A08aGCaMP_SuccessfulStim_AcquisitionPlane_XY0_Z0_T0_C0.tif')
#im_chrimson=skimage.io.imread(data_path+'dbdChrimson_SuccessfulStim_StimPlane_XY0_Z0_T0_C0.tif')

#first plot average pixel intensity


#then plot variance of pixel intensity