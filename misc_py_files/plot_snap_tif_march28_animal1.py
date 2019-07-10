import pdb
from py_utilities import tw_filehandling as fh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from py_utilities import fp_library2 as fpl
import file_utilities as util
import matplotlib as mpl

data_path= '/Volumes/LaCie/2pdata_elife/march28/wt/animal1/'

#file_names= ['2x 10 micron diam z-stack0space seperation _XY1553116043_Z000_T0_C0.tif']
#'2x 10 micron diam z-stack4space seperation _XY1553116200_Z000_T0_C0.tif','2x 10 micron diam z-stack8space seperation _XY1553116392_Z000_T0_C0.tif',
#file_names'2x 10 micron diam z-stack12space seperation _XY1553116511_Z000_T0_C0.tif','2x 10 micron diam z-stack16space seperation _XY1553116631_Z000_T0_C0.tif',
#file_names=['2x 10 micron diam z-stack16space seperation _XY1553116631_Z000_T0_C0.tif']
file_names=['Stream to disk_XY0_Z0_T0_C0.tif','Stream to disk - 1_XY0_Z0_T0_C0.tif']
pck_name='---Streaming Phasor Capture - 6_XY0_Z0_T000_C0.tif.pck'
#file_name=['2x 10 micron diam z-stack20space seperation  - 1_XY1553116792_Z000_T0_C0.tif']
microns_per_pixel=1.47441
off_target_centers=[[182,195],[190,189]]
on_target_centers=[[179,186],[187.5,202]]
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
    pdb.set_trace()
    plt.set_cmap('hot')
    imobj=ax[crind].imshow(dt['tifstack'])
    ax[crind].set_xlim(140,240)
    ax[crind].set_ylim(125,240)
    if crind==0:
        imobj.set_clim(200,500)
    if crind==1:
        imobj.set_clim(200,500)
    imobj=ax[crind+2].imshow(dt['tifstack'])
    imobj.set_clim(100,900)
    ax[crind+2].set_xlim(130,250)
    ax[crind+2].set_ylim(130,250)

    y=np.zeros(np.shape(dt['tifstack']))
    
    xvls=np.array(stim_region['xlist'][0])
    yvls=np.array(stim_region['ylist'][0])
    y[yvls,xvls]=1
    y=np.ma.masked_where(y==0,y)
    
    if crind==0:
        ax[crind].plot([160,160+10/microns_per_pixel],[150,150],'r')
        cr_center=on_target_centers[0]
        circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='g',facecolor='None')
        ax[crind].add_patch(circ)
        cr_center=on_target_centers[1]
        circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='g',facecolor='None')
        ax[crind].add_patch(circ)
    if crind==1:
        cr_center=off_target_centers[0]
        circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='c',facecolor='None')
        ax[crind].add_patch(circ)

        cr_center=off_target_centers[1]
        circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='c',facecolor='None')
        ax[crind].add_patch(circ)

    xvls=np.array(stim_region['xlist'][1])
    yvls=np.array(stim_region['ylist'][1])
    y=np.zeros(np.shape(dt['tifstack']))
    y[yvls,xvls]=1
    y=np.ma.masked_where(y==0,y)
    
    ax[crind].plot([200,200+10/microns_per_pixel],[170,170],'c')
    fpl.adjust_spines(ax[crind],[])
    
    