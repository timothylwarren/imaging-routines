#plot_example_trace.py
#rewritten to read in .pck (pickle file)
#which is based on previous ROI calculation from make_roi_example.py

#script plots time series from meta data
#plot is from (start_time_in_sec - pre_time_in_sec) until (start_time_in_sec+post_time_in_sec)
import filehandling as fh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams["font.family"] = "Arial"
matplotlib.rcParams["font.size"] = 7 
data_path= '/users/tim/python_packages/imaging/datafiles/'
files_to_plot=['stream_ex_dt.tif']

start_time_in_sec=10
pre_time_in_sec=5
post_time_in_sec=5
roi_ind=0
TIME_BETWEEN_FRAMES=.12625
microns_per_pixel=1.47441


def main():
    make_traces()
    #make_image()

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
            st_time=start_time_in_sec
            st_frame=int(np.ceil(st_time/TIME_BETWEEN_FRAMES)-1)
            modvl=np.mod(st_time/TIME_BETWEEN_FRAMES,np.floor(st_time/TIME_BETWEEN_FRAMES))
            
            crax.plot(np.arange(pre_time_in_frames+post_time_in_frames),dt['mn_roi'][roi_ind][st_frame-pre_time_in_frames:st_frame+post_time_in_frames],color=col,linewidth=0.5)
            
           
            

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



