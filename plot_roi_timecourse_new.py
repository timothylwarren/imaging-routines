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
PLOT_STIM_REGION=False
USE_PREVIOUS_ROI=False
UNIQUE_STIM_EVENTS=2
PREVIOUS_ROI_FILE='---Streaming Phasor Capture - 1_XY0_Z0_T000_C0.tif'
#logfile='photo12.txt'
data_path= '/Volumes/LaCie/2pdata/march28/wt/animal1/'
stim_meta_dir='photomanipulation_data/'
#file_name= '---Streaming Phasor Capture - 5_XY0_Z0_T0000_C0.tif'
file_names=['---Streaming Phasor Capture - 1_XY0_Z0_T000_C0.tif']
timelapse_interval=.12579
stim_times=[10,20,30,40,50,60]
heights=[82,161,240,319,399,478]
stim_region={}
colors=['c','g','m','b']
PREF_WINDOW=[1,0.4]
POSTF_WINDOW=[0, .6]
#read in tif file


#im is a dictionary with tifstack and metadata about imaging from PMT
for file_name in file_names:
    (im,stim)=util.read_in_tif_and_get_metadata(data_path + file_name)

    if STIM_FLAG:
        logfile=file_name.split('_')[0]+'.txt'
        stimfile=data_path + stim_meta_dir + logfile
        (stim_depths,stim_times)=util.get_stim_depths(stimfile)
        
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
    #plt.colormap('hot')
    plt.close('all')
    #plt.draw()
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


    #im_cut_all=im[:,150:250,150:250]
        
    #lines = cv2.HoughLines(stim_edges[0], 1, np.pi / 180, 190)
    num_frames=len(im['tifstack'][:,0,0])

    for crind in np.arange(int(num_rois)):
        mn_roi[crind]=[]
        for crframe in np.arange(num_frames):
            
            mn_roi[crind].append(np.mean(im_zoom[crframe,masks[crind]]))

    #to save to pickle file
    #mean_of_Tif
    #mn_roi
    #masks
    if not USE_PREVIOUS_ROI:
        sumdt={}
        sumdt['roi']=my_roi
        sumdt['zoom_vls']={}
        sumdt['zoom_vls']['xvls']=xvls
        sumdt['zoom_vls']['yvls']=yvls


    stim_tms=util.convert_stim_times(stim_times)
    frame_tms=[float(i) for i in im['time_stamps']]
    deltaf_vls=util.get_delta_f(stim_tms,mn_roi,frame_tms,PREF_WINDOW,POSTF_WINDOW)

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

    fh.save_to_pickle(data_path+file_name + '.pck', sumdt)





#Load GCAMP tif...
#im_gcamp=skimage.io.imread(data_path+'A08aGCaMP_SuccessfulStim_AcquisitionPlane_XY0_Z0_T0_C0.tif')
#im_chrimson=skimage.io.imread(data_path+'dbdChrimson_SuccessfulStim_StimPlane_XY0_Z0_T0_C0.tif')

#first plot average pixel intensity


#then plot variance of pixel intensity