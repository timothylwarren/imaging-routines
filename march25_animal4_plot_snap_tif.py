import pdb
from py_utilities import tw_filehandling as fh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from py_utilities import fp_library2 as fpl
import file_utilities as util
import matplotlib as mpl
###
#now plot the means over time in the region of interest
####

#here I don't plot 10th-13th frame b/c that's when stimulation occurs.
data_path= '/Volumes/LaCie/2pdata/march25/animal4/'

#file_names= ['2x 10 micron diam z-stack0space seperation _XY1553116043_Z000_T0_C0.tif']
#'2x 10 micron diam z-stack4space seperation _XY1553116200_Z000_T0_C0.tif','2x 10 micron diam z-stack8space seperation _XY1553116392_Z000_T0_C0.tif',
#file_names'2x 10 micron diam z-stack12space seperation _XY1553116511_Z000_T0_C0.tif','2x 10 micron diam z-stack16space seperation _XY1553116631_Z000_T0_C0.tif',
#file_names=['2x 10 micron diam z-stack16space seperation _XY1553116631_Z000_T0_C0.tif']
file_names=['Snap image - 3_XY0_Z0_T0_C0.tif','Snap image - 4_XY0_Z0_T0_C0.tif']
pck_name='---Streaming Phasor Capture - 2 - 1_XY0_Z0_T0000_C0.tif.pck'
#file_name=['2x 10 micron diam z-stack20space seperation  - 1_XY1553116792_Z000_T0_C0.tif']
microns_per_pixel=1.47441

UNIQUE_STIM_EVENTS=1
fig=plt.figure()
ax=[]
ax.append(fig.add_subplot(221))
ax.append(fig.add_subplot(222))
ax.append(fig.add_subplot(223))
ax.append(fig.add_subplot(224))

stim_region={}
for crind in np.arange(len(file_names)):
    dt=util.read_in_tif(data_path+file_names[crind])
    savedt=fh.open_pickle(data_path+pck_name)
    stim_region=savedt['stim_region']
    #dt=fh.open_pickle(data_path+file_names[crind]+'.pck')

    imobj=ax[crind].imshow(dt['tifstack'])
    #imobj.set_clim(200,2000)
    ax[crind].set_xlim(120,260)
    ax[crind].set_ylim(120,260)
    imobj.set_clim(0,600)
    imobj=ax[crind+2].imshow(dt['tifstack'])
    imobj.set_clim(0,600)
    #imobj.set_clim(200,2000)
    ax[crind+2].set_xlim(120,260)
    ax[crind+2].set_ylim(120,260)

    y=np.zeros(np.shape(dt['tifstack']))
    
    xvls=np.array(stim_region['xlist'][0])
    yvls=np.array(stim_region['ylist'][0])
    y[yvls,xvls]=1
    y=np.ma.masked_where(y==0,y)
    ax[crind].imshow(y,cmap='Reds',alpha=0.6,interpolation='nearest')
    ax[crind].plot([160,160+10/microns_per_pixel],[150,150],'r')
    xvls=np.array(stim_region['xlist'][1])
    yvls=np.array(stim_region['ylist'][1])
    y[yvls,xvls]=1
    y=np.ma.masked_where(y==0,y)
    ax[crind].imshow(y,cmap='Greens',alpha=0.3,interpolation='nearest')

    #xvls=np.array(stim_region['xlist'][1])
    #yvls=np.array(stim_region['ylist'][1])
    #zero_im[yvls,xvls]=1
    #ax[crind].imshow(zero_im,alpha=0.5)

    #imshowobj=ax.imshow(mean_xy)
    #imshowobj.set_clim(20,45)
    #ax.set_xlim(925,1050)
    #ax.set_ylim(660,785)
    #imshowobj2=ax2.imshow(mean_z)
    #imshowobj2.set_clim(14.6,16.5)
    #ax2.set_xlim(925,1050)
    #ax2.plot([940,940+10/microns_per_pixel],[20,20],'r')


    #stim_len=0.1
    #ax=fig.add_subplot(6,1,crind+1)
    #ax.plot(dt['mn_roi'][0],'k')
    #ax.plot(dt['mn_roi'][1],'r')
    #ax.text(0,50,file_names[crind].split('stack')[1],fontsize=5)
    #if crind<5:
     #   fpl.adjust_spines(ax,['left'])
    #else:
     #   fpl.adjust_spines(ax,['bottom','left'])
    #plt.xlim(0,100)



###
#now plot the means over time in the region of interest
####

#here I don't plot 10th-13th frame b/c that's when stimulation occurs.

