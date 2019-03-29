import pdb
from py_utilities import tw_filehandling as fh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from py_utilities import fp_library2 as fpl
###
#now plot the means over time in the region of interest
####

#here I don't plot 10th-13th frame b/c that's when stimulation occurs.

#data_path= '/Volumes/LaCie/2pdata/march26/animal9/'
#file_names=['---Streaming Phasor Capture - 2 - 2_XY0_Z0_T0000_C0.tif']
#file_names=['---Streaming Phasor Capture - 5_XY0_Z0_T0000_C0.tif','---Streaming Phasor Capture - 5 - 1_XY0_Z0_T0000_C0.tif']




#file_names= ['Streaming Phasor Capture - 3_XY0_Z0_T0000_C0.tif','Streaming Phasor Capture - 4_XY0_Z0_T0000_C0.tif',
#'Streaming Phasor Capture - 5_XY0_Z0_T0000_C0.tif','Streaming Phasor Capture - 6_XY0_Z0_T0000_C0.tif','Streaming Phasor Capture - 7_XY0_Z0_T0000_C0.tif']

def just_plotting2(meta_dt):
    file_names=meta_dt['file_names']

    fig=plt.figure()
    gs=GridSpec(11,6,figure=fig)
    ax1=fig.add_subplot(gs[0:3,0])
    ax2=fig.add_subplot(gs[4:7,0])
    ax3=fig.add_subplot(gs[8:11,0])
    ROWCT=0
    for ind,crfile in enumerate(file_names):
        pdb.set_trace()
        dt=fh.open_pickle(meta_dt['data_path']+crfile+'.pck')
        stim_height=500
        stim_len=0.1
        
        colors=['c','g','m','b']
        
        #tmlapse_in_s=.11963


        
        #plot mean image and rois
        if ind==0:
            pdb.set_trace()
            ax1.imshow(dt['im_mean'],origin='lower')
            fpl.adjust_spines(ax1,[])
        CT=0
        for crax in [ax1,ax2,ax3]:
            pdb.set_trace()
            plt.sca(crax)
            try:
                for cr_roi in dt['roi']:
                    cr_roi.display_roi()
            except:
                pdb.set_trace()
            if CT>0:
                
                crax.imshow(dt['stim_edges'][CT-1],origin='lower')
            CT=CT+1


        for crind in meta_dt['roi_to_plot']:
            crax=fig.add_subplot(gs[ROWCT+1,2:5])
            fpl.adjust_spines(crax,[])
            ROWCT=ROWCT+1
            crax.plot(dt['frame_tms'],dt['mn_roi'][crind],colors[crind],linewidth=0.3)
            stim_tms=np.unique(dt['stim_tms'])
        #add stimulation events to subplot
            
            for crtime in stim_tms:
                crax.plot([crtime,crtime+stim_len],[stim_height,stim_height],'r')
            
            for crind,cr_depth in enumerate(np.array(dt['stim_depths'][::2])):
            
                crax.text(stim_tms[crind],stim_height+50,str(int(cr_depth)),fontsize=3,color='r')

    #fpl.adjust_spines(ax1,['bottom','left'])
            fpl.adjust_spines(crax,['bottom','left'])
            crax.set_aspect(0.02)
            crax.set_xlim((0,160))
            crax.set_ylim((300,900))
    plt.savefig(meta_dt['data_path']+crfile+'.eps')
        



###
#now plot the means over time in the region of interest
####

#here I don't plot 10th-13th frame b/c that's when stimulation occurs.

