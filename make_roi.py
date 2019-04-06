##
##make_roi.py 
##
##Used to create rois and extract fluorescene daa from slidebook files
##Python 3.7

import matplotlib.pyplot as plt
import file_utilities as util
import skimage.io
import numpy as np
#source for RoiPoly module 
#https://github.com/jdoepfert/roipoly.py
from roipoly import RoiPoly
from py_utilities import tw_filehandling as fh
import pdb

#plt.ion()

#PARAMETERS_TO_SET
STIM_FLAG=True
PLOT_STIM_REGION=False

#Analyze with ROI set previously in ROI file described below
USE_PREVIOUS_ROI=True

#if USE_META_DT is true, then tif files to analyze are set in meta_dt_file
USE_META_DT_FILE=True
UNIQUE_STIM_EVENTS=2
TIME_BETWEEN_FRAMES=.12625
PREVIOUS_ROI_FILE='---Streaming Phasor Capture - 8_XY0_Z0_T0000_C0.tif'
#specific to configuration
data_path= '/Volumes/LaCie/tstdir/'
meta_dt_file='anim5_plotdata.pck'
stim_meta_dir='photomanipulation_data/'
#file_names= ['---Streaming Phasor Capture - 1_XY0_Z0_T000_C0.tif']
file_names=['---Streaming Phasor Capture - 8_XY0_Z0_T0000_C0.tif']
preframes=20
postframes=5
stim_region={}
colors=['c','g','m','b']

#read in tif file
if USE_META_DT_FILE:
    meta_dt=fh.open_pickle(data_path+meta_dt_file)
    file_names=meta_dt['file_names']
    PREVIOUS_ROI_FILE=file_names[0]

#im is a dictionary with tifstack and metadata about imaging from PMT
for file_name in file_names:
    (im,stim)=util.read_in_tif_and_get_metadata(data_path + file_name)

    if STIM_FLAG:
        logfile=file_name.split('_')[0]+'.txt'
        stimfile=data_path + stim_meta_dir + logfile
        (stim_depths,erroneous_stim_times)=util.get_stim_depths(stimfile)
        
        roi_file=stimfile.split('.txt')[0] + '-points.txt'
        (stim_region['xlist'],stim_region['ylist'])=util.get_stim_region(roi_file,unique_events=UNIQUE_STIM_EVENTS)

        
    #take mean of file across all time points

    im_mean=np.mean(im['tifstack'],axis=0)
    fig=plt.figure()
    plt.imshow(im_mean,origin='lower')
    if not USE_PREVIOUS_ROI:
        xtxt=input("Enter desired zoom Xvls e.g. 100,200 ")
        ytxt=input("Enter desired zoom Yvls e.g. 100,200 ")

        xvls=(int(xtxt.split(',')[0]),int(xtxt.split(',')[1]))
        yvls=(int(ytxt.split(',')[0]),int(ytxt.split(',')[1]))
    else:
        print('using previous ROI')
        sumdt=fh.open_pickle(data_path+PREVIOUS_ROI_FILE + '.pck')
        xvls=sumdt['zoom_vls']['xvls']
        yvls=sumdt['zoom_vls']['yvls']
    plt.xlim(xvls)
    plt.ylim(yvls)
    plt.close('all')
    plt.figure()

    im_zoom_mean=im_mean[int(yvls[0]):int(yvls[1]),int(xvls[0]):int(xvls[1])]
    im_zoom=im['tifstack'][:,int(yvls[0]):int(yvls[1]),int(xvls[0]):int(xvls[1])]
    plt.imshow(im_zoom_mean,origin='lower')

    if not USE_PREVIOUS_ROI:

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
    else:
        my_roi=sumdt['roi']
        mn_roi={}
        num_rois=len(my_roi)
        masks=sumdt['roi_masks']
    fig=plt.figure()
    ax1=fig.add_subplot(311)
    plt.imshow(im_zoom_mean,origin='lower')
    for cr_roi in my_roi:
        cr_roi.display_roi()

    stim_edges=[]
    stim_mask=[]
    for crind in np.arange(len(stim_region['xlist'])):
        
        stim_xvls=np.array(stim_region['xlist'][crind])-xvls[0]
        stim_yvls=np.array(stim_region['ylist'][crind])-yvls[0]
        
        y=np.zeros(np.shape(im_zoom_mean))
        
        y[stim_yvls,stim_xvls]=1
        y=np.ma.masked_where(y==0,y)
        stim_mask.append(y)

        stim_edges.append(util.make_edges(stim_xvls,stim_yvls,im_zoom_mean))

    for crind in [0,1]:
        try:
            fig.add_subplot(3,1,crind+2)
            for cr_roi in my_roi:
                cr_roi.display_roi()
            plt.imshow(stim_edges[crind],origin='lower')
        except:
            tst=1

    num_frames=len(im['tifstack'][:,0,0])

    for crind in np.arange(int(num_rois)):
        mn_roi[crind]=[]
        for crframe in np.arange(num_frames):
            
            mn_roi[crind].append(np.mean(im_zoom[crframe,masks[crind]]))

    if not USE_PREVIOUS_ROI:
        sumdt={}
        sumdt['roi']=my_roi
        sumdt['zoom_vls']={}
        sumdt['zoom_vls']['xvls']=xvls
        sumdt['zoom_vls']['yvls']=yvls

    (stim_tms,stim_frame_nums)=util.convert_stim_times(stim['stim_frame_nums'],frame_flag=True,time_between_frames=TIME_BETWEEN_FRAMES)
    frame_tms=[float(i) for i in im['time_stamps']]
    deltaf_vls=util.get_delta_f(mn_roi,stim_frame_nums,preframes,postframes,pre_frame_buffer=2)

    sumdt['im_mean']=im_zoom_mean
    sumdt['stim_mask']=stim_mask
    sumdt['mn_roi']=mn_roi
    sumdt['roi_masks']=masks
    sumdt['frame_nums']=[int(i) for i in im['frame_nums']]
    sumdt['frame_tms']=frame_tms
    sumdt['stim_tms']=stim_tms
    sumdt['deltaf_vls']=deltaf_vls
    sumdt['stim_depths']=[float(i) for i in stim_depths]
    sumdt['stim_region']=stim_region
    sumdt['stim_edges']=stim_edges
    sumdt['stim_frame_nums']=stim_frame_nums
    
    fh.save_to_pickle(data_path+file_name + '.pck', sumdt)




