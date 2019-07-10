#plotting fluorescence measured with substage camera

import pdb
from py_utilities import tw_filehandling as fh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from py_utilities import fp_library2 as fpl
from imaging import file_utilities as util
plt.ion()

data_path= '/Volumes/LaCie/2pdata_elife/may20/'
file_names=['Z stack_XY1558372740_Z000_T0_C0.tif']
microns_per_pixel=0.313495

fig=plt.figure(figsize=(2,4))
gs=GridSpec(2,1,figure=fig)
ax=[]

#ax_rthist=fig.add_subplot(gs[5:7,0:4])
#ax2_rthist=fig.add_subplot(gs[1:3,12:])
#ax2_bthist=fig.add_subplot(gs[7:,6:12])
frames_to_plot=[49,50]
for ind,crframe in enumerate(frames_to_plot):
    try:
        ax.append(fig.add_subplot(gs[ind,0]))
    except:
        pdb.set_trace()


for crind in np.arange(len(file_names)):
    plt.set_cmap('viridis')
    dt=util.read_in_tif(data_path+file_names[crind])
    for ind,crframe in enumerate(frames_to_plot):
        #mean_xy=np.mean(dt['tifstack'],axis=0)
    #mean_z=np.mean(dt['tifstack'],axis=1)
        imshowobj=ax[ind].imshow(dt['tifstack'][crframe,:,:])
        #imshowobj.set_clim(20,28)
        fpl.adjust_spines(ax[ind],[])
        ax[ind].set_xlim(200,1150)
        ax[ind].set_ylim(50,200)
        #microns_mean_z=np.shape(mean_z)[1]*microns_per_pixel
        #ax.plot([970,970+20/microns_per_pixel],[775,775],'w')
    #aspect_ratio=microns_mean_z/100.
    #imshowobj2=ax2.imshow(mean_z)
    #imshowobj2.set_clim(14.6,16.5)
    #fpl.adjust_spines(ax2,[])
    #ax2.set_aspect(aspect_ratio)
    #ax2.set_xlim(950,1150)
    #ax2.set_ylim(0,100)
    #mean_meanz=np.mean(mean_z,axis=0)
    #ax2_bthist.plot(mean_meanz)
    
    #ax2.plot([970,970+20/microns_per_pixel],[20,20],'w')
    #fpl.adjust_spines(ax2_bthist,[])
    #ax2_bthist.set_xlim(950,1150)

    #rtmean_meanz=np.mean(mean_z,axis=1)

    #ax2_rthist.plot(rtmean_meanz,np.arange(len(rtmean_meanz)))
    #fpl.adjust_spines(ax2_rthist,[])
    #ax2_rthist.set_ylim(0,100)

    #rtmean_meanxy=np.mean(mean_xy,axis=1)
    #ax_rthist.plot(rtmean_meanxy,np.arange(len(rtmean_meanxy)))
    #fpl.adjust_spines(ax_rthist,[])
    #ax_rthist.set_ylim(725,850)
    

