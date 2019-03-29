import pdb
from py_utilities import tw_filehandling as fh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from py_utilities import fp_library2 as fpl
import file_utilities as util
###
#now plot the means over time in the region of interest
####

#here I don't plot 10th-13th frame b/c that's when stimulation occurs.
data_path= '/Volumes/LaCie/2pdata/march20/sep_to_convergence/'

#file_names= ['2x 10 micron diam z-stack0space seperation _XY1553116043_Z000_T0_C0.tif']
#'2x 10 micron diam z-stack4space seperation _XY1553116200_Z000_T0_C0.tif','2x 10 micron diam z-stack8space seperation _XY1553116392_Z000_T0_C0.tif',
#file_names'2x 10 micron diam z-stack12space seperation _XY1553116511_Z000_T0_C0.tif','2x 10 micron diam z-stack16space seperation _XY1553116631_Z000_T0_C0.tif',
file_names=['2x 10 micron diam z-stack16space seperation _XY1553116631_Z000_T0_C0.tif']
file_name=['2x 10 micron diam z-stack20space seperation _XY1553115882_Z000_T0_C0.tif']
#file_name=['2x 10 micron diam z-stack20space seperation  - 1_XY1553116792_Z000_T0_C0.tif']
microns_per_pixel=0.313495


fig=plt.figure()
ax=fig.add_subplot(211)
ax2=fig.add_subplot(212)
for crind in np.arange(len(file_names)):
    dt=util.read_in_tif(data_path+file_names[crind])
    #dt=fh.open_pickle(data_path+file_names[crind]+'.pck')
    mean_xy=np.mean(dt['tifstack'],axis=0)
    mean_z=np.mean(dt['tifstack'],axis=1)
    imshowobj=ax.imshow(mean_xy)
    imshowobj.set_clim(20,45)
    ax.set_xlim(925,1050)
    ax.set_ylim(660,785)
    imshowobj2=ax2.imshow(mean_z)
    imshowobj2.set_clim(14.6,16.5)
    ax2.set_xlim(925,1050)
    ax2.plot([940,940+10/microns_per_pixel],[20,20],'r')


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

