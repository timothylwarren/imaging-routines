
import pdb
from py_utilities import tw_filehandling as fh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from py_utilities import fp_library2 as fpl
import plot_utilities as plt_util
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams["font.family"] = "Arial"
matplotlib.rcParams["font.size"] = 7 
data_path='/Volumes/LaCie/2pdata/march28/unc-5/animal4/'
files_to_plot=['---Streaming Phasor Capture - 3_XY0_Z0_T000_C0.tif','---Streaming Phasor Capture - 2_XY0_Z0_T000_C0.tif']
stim_frame={}
stim_frame['on']=[80,80]
stim_frame['off']=[159,159]
stim_ind={}
stim_ind['on']=0
stim_ind['off']=1
pre_time_in_sec=4
post_time_in_sec=4
roi_ind=1
TIME_BETWEEN_FRAMES=.12642225
stim_duration=0.1
microns_per_pixel=1.47441
on_target_centers=[[67,30],[78,42]]
off_target_centers=[[63,39],[69,23]]
###


def main():
    make_traces()
    make_image()

def make_traces():
    fig=plt.figure(figsize=(1.5,1.5))
    gs=GridSpec(2,2,figure=fig)
    ax={}
    ax['on']=[]
    ax['off']=[]
    ax['on'].append(fig.add_subplot(gs[0,0]))
    ax['on'].append(fig.add_subplot(gs[1,0]))
    ax['off'].append(fig.add_subplot(gs[0,1]))
    ax['off'].append(fig.add_subplot(gs[1,1]))
    for crind,crfile in enumerate(files_to_plot):
        dt=fh.open_pickle(data_path+crfile+'.pck')
        pre_time_in_frames=int(np.ceil(pre_time_in_sec/TIME_BETWEEN_FRAMES))
        post_time_in_frames=int(np.ceil(post_time_in_sec/TIME_BETWEEN_FRAMES))
        for key in ['on','off']:
            if key is 'on':
                col='k'
            else:
                col='r'
            crax=ax[key][crind]
            st_frame=stim_frame[key][crind]
            
            crax.plot(np.arange(pre_time_in_frames-1),dt['mn_roi'][roi_ind][st_frame-pre_time_in_frames:st_frame-1],color=col,linewidth=0.5)
            stim_duration_in_frames=stim_duration/TIME_BETWEEN_FRAMES

            #crax.plot(np.arange(2)+pre_time_in_frames-1,dt['mn_roi'][roi_ind][st_frame-1:st_frame+1])
            crax.plot([pre_time_in_frames-1,pre_time_in_frames-1+stim_duration_in_frames],[700,700],color='c',linewidth=2)
            
            pre_f=dt['deltaf_vls']['pre_f'][roi_ind][stim_ind[key]]
            pst_f=dt['deltaf_vls']['pst_f'][roi_ind][stim_ind[key]]
            crax.plot(39,pre_f,'<')
            crax.plot(50,pst_f,'<')
            crax.plot(np.arange(post_time_in_frames)+pre_time_in_frames+1,dt['mn_roi'][roi_ind][st_frame+1:st_frame+1+post_time_in_frames],color=col,linewidth=0.5)
            
            fpl.adjust_spines(crax,['left'])
            crax.set_ylim(300,1200)
            crax.set_yticks([300,1200])
            if crind==0:
                if key is 'on':
                    crax.plot([10,10+1/TIME_BETWEEN_FRAMES],[350,350],'k')



def make_image():
    fig=plt.figure(figsize=(1,2))
    ax=fig.add_subplot(111)
    plt.set_cmap('viridis')
    crfile=files_to_plot[0]
    dt=fh.open_pickle(data_path+crfile+'.pck')
    ax.imshow(dt['im_mean'],origin='lower')
    #fpl.adjust_spines(ax,[])
        
        #for axind,crax in enumerate([ax1,ax2,ax3]):
            
    plt.sca(ax)
           
    cr_roi=dt['roi'][roi_ind]
    
    cr_roi.display_roi()
    ax.set_ylim(10,70)
    ax.set_xlim(20,90)
    ten_microns_in_pixels=10/microns_per_pixel
    plt.plot([30,30+ten_microns_in_pixels],[20,20],'r')
    #ax.imshow(dt['stim_mask'][0],cmap='Greens',alpha=0.5,origin='lower')
    #ax.imshow(dt['stim_mask'][1],cmap='Reds',alpha=0.5,origin='lower')
    cr_center=on_target_centers[0]
    circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='k',facecolor='None')
    ax.add_patch(circ)
    cr_center=on_target_centers[1]
    circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='k',facecolor='None')
    ax.add_patch(circ)
    cr_center=off_target_centers[0]
    circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='r',facecolor='None')
    ax.add_patch(circ)
    cr_center=off_target_centers[1]
    circ=plt.Circle((cr_center[0],cr_center[1]),radius=5/microns_per_pixel,edgecolor='r',facecolor='None')
    ax.add_patch(circ)
    fpl.adjust_spines(ax,[])
if __name__== "__main__":
  main()



