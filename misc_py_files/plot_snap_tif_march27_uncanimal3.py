#2-p imaging of mcherry channel from elife submission
import pdb
from py_utilities import tw_filehandling as fh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from py_utilities import fp_library2 as fpl
import file_utilities as util
import matplotlib as mpl

data_path= '/Volumes/LaCie/2pdata/march27_unc-5/animal3/'
file_names=['Snap image - 1_XY0_Z0_T0_C0.tif','Snap image - 2_XY0_Z0_T0_C0.tif']
pck_name='---Streaming Phasor Capture - 2 - 1_XY0_Z0_T000_C0.tif.pck'
microns_per_pixel=1.47441
on_target_centers=[[168,171],[114,178]]
off_target_centers=[[145,166],[152,180]]
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
    plt.set_cmap('hot')
    imobj=ax[crind].imshow(dt['tifstack'])
    ax[crind].set_xlim(0,600)
    ax[crind].set_ylim(0,600)
    if crind==0:
        imobj.set_clim(200,400)
    if crind==1:
        imobj.set_clim(200,400)
    imobj=ax[crind+2].imshow(dt['tifstack'])
    imobj.set_clim(100,900)
    ax[crind+2].set_xlim(0,600)
    ax[crind+2].set_ylim(0,600)

    y=np.zeros(np.shape(dt['tifstack']))
    
    xvls=np.array(stim_region['xlist'][0])
    yvls=np.array(stim_region['ylist'][0])
    y[yvls,xvls]=1
    y=np.ma.masked_where(y==0,y)
   
    if crind==0:
        ax[crind].plot([160,160+10/microns_per_pixel],[150,150],'r')
        cr_center=on_target_centers[0]
        circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='c',facecolor='None')
        ax[crind].add_patch(circ)
        cr_center=on_target_centers[1]
        circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='c',facecolor='None')
        ax[crind].add_patch(circ)
    if crind==1:
        cr_center=off_target_centers[0]
        circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='g',facecolor='None')
        ax[crind].add_patch(circ)

        cr_center=off_target_centers[1]
        circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='g',facecolor='None')
        ax[crind].add_patch(circ)

    xvls=np.array(stim_region['xlist'][1])
    yvls=np.array(stim_region['ylist'][1])
    y=np.zeros(np.shape(dt['tifstack']))
    y[yvls,xvls]=1
    y=np.ma.masked_where(y==0,y)
    ax[crind].set_xlim(80,220)
    ax[crind].set_ylim(120,240)
    ax[crind].plot([200,200+10/microns_per_pixel],[190,190],'c')
   
    fpl.adjust_spines(ax[crind],'')
    
    