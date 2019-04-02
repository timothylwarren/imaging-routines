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
data_path= '/Volumes/LaCie/march29/'

#file_names= ['2x 10 micron diam z-stack0space seperation _XY1553116043_Z000_T0_C0.tif']
#'2x 10 micron diam z-stack4space seperation _XY1553116200_Z000_T0_C0.tif','2x 10 micron diam z-stack8space seperation _XY1553116392_Z000_T0_C0.tif',
#file_names'2x 10 micron diam z-stack12space seperation _XY1553116511_Z000_T0_C0.tif','2x 10 micron diam z-stack16space seperation _XY1553116631_Z000_T0_C0.tif',
#file_names=['2x 10 micron diam z-stack16space seperation _XY1553116631_Z000_T0_C0.tif']
file_names=['2x 10um spots 26um separation _XY1553873438_Z000_T0_C0.tif']
#file_names=['2x 10um spots 20um separation _XY1553872413_Z000_T0_C0.tif']
#file_name=['2x 10 micron diam z-stack20space seperation  - 1_XY1553116792_Z000_T0_C0.tif']
microns_per_pixel=0.313495


fig=plt.figure(figsize=(2,4))
gs=GridSpec(8,14,figure=fig)
ax=fig.add_subplot(gs[0:5,0:5])
ax_rthist=fig.add_subplot(gs[5:7,0:4])
ax2=fig.add_subplot(gs[1:3,6:12])
ax2_rthist=fig.add_subplot(gs[1:3,12:])
ax2_bthist=fig.add_subplot(gs[7:,6:12])
for crind in np.arange(len(file_names)):
    plt.set_cmap('viridis')
    dt=util.read_in_tif(data_path+file_names[crind])
    #dt=fh.open_pickle(data_path+file_names[crind]+'.pck')
    mean_xy=np.mean(dt['tifstack'],axis=0)
    mean_z=np.mean(dt['tifstack'],axis=1)
    imshowobj=ax.imshow(mean_xy)
    imshowobj.set_clim(20,28)
    fpl.adjust_spines(ax,[])
    ax.set_xlim(950,1150)
    ax.set_ylim(725,850)
    microns_mean_z=np.shape(mean_z)[1]*microns_per_pixel
    aspect_ratio=microns_mean_z/100.
    #ax2.hist(sample, bins=30, orientation="horizontal");
    imshowobj2=ax2.imshow(mean_z)
    imshowobj2.set_clim(14.6,16.5)
    fpl.adjust_spines(ax2,[])
    ax2.set_aspect(aspect_ratio)
    ax2.set_xlim(950,1150)
    ax2.set_ylim(0,100)
    mean_meanz=np.mean(mean_z,axis=0)
    ax2_bthist.plot(mean_meanz)
    ax.plot([970,970+20/microns_per_pixel],[775,775],'w')
    ax2.plot([970,970+20/microns_per_pixel],[20,20],'w')
    fpl.adjust_spines(ax2_bthist,[])
    ax2_bthist.set_xlim(950,1150)

    rtmean_meanz=np.mean(mean_z,axis=1)

    ax2_rthist.plot(rtmean_meanz,np.arange(len(rtmean_meanz)))
    fpl.adjust_spines(ax2_rthist,[])
    ax2_rthist.set_ylim(0,100)

    rtmean_meanxy=np.mean(mean_xy,axis=1)
    ax_rthist.plot(rtmean_meanxy,np.arange(len(rtmean_meanxy)))
    fpl.adjust_spines(ax_rthist,[])
    ax_rthist.set_ylim(725,850)
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

