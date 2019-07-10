#plotting fluorescence measured with substage camera

import pdb
from py_utilities import tw_filehandling as fh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from py_utilities import fp_library2 as fpl
from imaging import file_utilities as util

tst='10um dia spot Non-FT_XY1557952225_Z000_T0_C0.tif'
data_path= '/users/tim/data/2ptmp/may20/'
file_names=['Z stack_XY1558372740_Z000_T0_C0.tif']
save_names=['temporal_focusing_on.pdf','temporal_focusing_off.pdf']
save_path='/users/tim/Dropbox/2pfigs/'
microns_per_pixel=0.313495

plt.ion()
fig=plt.figure(figsize=(2,4))
ax=[]
gs=GridSpec(4,1,figure=fig)
ax.append(fig.add_subplot(gs[0,0]))
ax.append(fig.add_subplot(gs[1,0]))
ax.append(fig.add_subplot(gs[2,0]))
#ax_rthist=fig.add_subplot(gs[5:7,0:4])
#ax2=fig.add_subplot(gs[1:3,6:12])
#ax2_rthist=fig.add_subplot(gs[1:3,12:])
#ax2_bthist=fig.add_subplot(gs[7:,6:12])

for crind in np.arange(len(file_names)):
    
    plt.set_cmap('viridis')
    dt=util.read_in_tif(data_path+file_names[crind])
    
    imshowobj=ax[0].imshow(dt['tifstack'][60,:,:])
    imshowobj.set_clim(300,800)
    imshowobj=ax[1].imshow(dt['tifstack'][40,:,:])
    imshowobj.set_clim(300,800)
    imshowobj=ax[2].imshow(dt['tifstack'][20,:,:])
    imshowobj.set_clim(300,800)
    #for crax in ax:
     #   crax.set_xlim([100,300])
      #  crax.set_ylim([100,300])
    pdb.set_trace()    
    mean_xy=np.mean(dt['tifstack'],axis=0)
    mean_z=np.mean(dt['tifstack'],axis=1)
    imshowobj=ax.imshow(mean_xy)
    #imshowobj.set_clim(20,28)
    fpl.adjust_spines(ax,[])
    ax.set_xlim(600,1200)
    ax.set_ylim(600,1200)
    microns_mean_z=np.shape(mean_z)[1]*microns_per_pixel
    aspect_ratio=microns_mean_z/100.
    imshowobj2=ax2.imshow(mean_z)
    imshowobj2.set_clim(14.6,16.5)
    fpl.adjust_spines(ax2,[])
    ax2.set_aspect(aspect_ratio)
    ax2.set_xlim(600,1200)
    ax2.set_ylim(0,100)
    mean_meanz=np.mean(mean_z,axis=0)
    ax2_bthist.plot(mean_meanz)
    ax.plot([970,970+20/microns_per_pixel],[775,775],'w')
    ax2.plot([970,970+20/microns_per_pixel],[20,20],'w')
    fpl.adjust_spines(ax2_bthist,[])
    ax2_bthist.set_xlim(600,1200)

    rtmean_meanz=np.mean(mean_z,axis=1)

    ax2_rthist.plot(rtmean_meanz,np.arange(len(rtmean_meanz)))
    fpl.adjust_spines(ax2_rthist,[])
    ax2_rthist.set_ylim(0,100)

    rtmean_meanxy=np.mean(mean_xy,axis=1)
    ax_rthist.plot(rtmean_meanxy,np.arange(len(rtmean_meanxy)))
    fpl.adjust_spines(ax_rthist,[])
    ax_rthist.set_ylim(725,850)
    plt.savefig(save_path+save_names[crind],transparent=True)
    
    fig=plt.figure(figsize=(2,4))
