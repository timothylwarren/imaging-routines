#example traces in elife submission

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
data_path='/Volumes/LaCie/2pdata/march28/wt/animal1/'
files_to_plot=['---Streaming Phasor Capture - 1_XY0_Z0_T000_C0.tif']
stim_frame={}
stim_frame['on']=[80,80]
stim_frame['off']=[159,159]
stim_time_in_sec={}
stim_time_in_sec['on']=[9.95,9.95]
stim_time_in_sec['off']=[19.95,19.95]
stim_ind={}
stim_ind={}
stim_ind['on']=0
stim_ind['off']=1
pre_time_in_sec=4
post_time_in_sec=4
roi_ind=2
TIME_BETWEEN_FRAMES=.12625
stim_duration=0.15
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
        pdb.set_trace()
        pre_time_in_frames=int(np.ceil(pre_time_in_sec/TIME_BETWEEN_FRAMES))
        post_time_in_frames=int(np.ceil(post_time_in_sec/TIME_BETWEEN_FRAMES))
        for key in ['on','off']:
            if key is 'on':
                col='k'
            else:
                col='r'
            crax=ax[key][crind]

            st_time=stim_time_in_sec[key][crind]
            
            st_frame=int(np.ceil(st_time/TIME_BETWEEN_FRAMES)-1)
            modvl=np.mod(st_time/TIME_BETWEEN_FRAMES,np.floor(st_time/TIME_BETWEEN_FRAMES))
            crax.plot(np.arange(pre_time_in_frames),dt['mn_roi'][roi_ind][st_frame-pre_time_in_frames:st_frame],color=col,linewidth=0.5)
            stim_duration_in_frames=stim_duration/TIME_BETWEEN_FRAMES
            st_time_in_frames=pre_time_in_frames-1+modvl
            crax.plot([st_time_in_frames,st_time_in_frames+stim_duration_in_frames],[700,700],color='c',linewidth=2)
          
            pre_f=dt['deltaf_vls']['pre_f'][roi_ind][stim_ind[key]]
            pst_f=dt['deltaf_vls']['pst_f'][roi_ind][stim_ind[key]]
            crax.plot(39,pre_f,'<')
            crax.plot(50,pst_f,'<')
            crax.plot(np.arange(post_time_in_frames)+pre_time_in_frames+3,dt['mn_roi'][roi_ind][st_frame+3:st_frame+3+post_time_in_frames],color=col,linewidth=0.5)
            
            fpl.adjust_spines(crax,['left'])
            crax.set_ylim(300,900)
            crax.set_yticks([300,900])
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
                
    plt.sca(ax)
           
    cr_roi=dt['roi'][roi_ind]
    
    cr_roi.display_roi()
    ax.set_ylim(10,70)
    ax.set_xlim(20,90)
    ten_microns_in_pixels=10/microns_per_pixel
    plt.plot([30,30+ten_microns_in_pixels],[20,20],'r')
   
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



