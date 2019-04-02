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
###
#now plot the means over time in the region of interest
####

#here I don't plot 10th-13th frame b/c that's when stimulation occurs.

#data_path= '/Volumes/LaCie/2pdata/march26/animal9/'
#file_names=['---Streaming Phasor Capture - 2 - 2_XY0_Z0_T0000_C0.tif']
#file_names=['---Streaming Phasor Capture - 5_XY0_Z0_T0000_C0.tif','---Streaming Phasor Capture - 5 - 1_XY0_Z0_T0000_C0.tif']




#file_names= ['Streaming Phasor Capture - 3_XY0_Z0_T0000_C0.tif','Streaming Phasor Capture - 4_XY0_Z0_T0000_C0.tif',
#'Streaming Phasor Capture - 5_XY0_Z0_T0000_C0.tif','Streaming Phasor Capture - 6_XY0_Z0_T0000_C0.tif','Streaming Phasor Capture - 7_XY0_Z0_T0000_C0.tif']
SUMMARY_DATA_LOCATION='/Users/tim/data/2p_summary_data/'

datpath='/Volumes/LaCie/2pdata/march28/wt/animal1/'
microns_per_pixel=1.47441

def main():
    meta_dt={}
    meta_dt['data_path']= datpath
    meta_dt['meta_file_name']='anim1_plotdata.pck'


    save_dat_file_name=datpath.split('/')[-3] +'_' + datpath.split('/')[-2] + '.pck'
    save_fig_file_name=datpath.split('/')[-3] +'_' + datpath.split('/')[-2] + '.eps'
    meta_dt=fh.open_pickle(meta_dt['data_path']+meta_dt['meta_file_name'])
    
    file_names=meta_dt['file_names']

    if meta_dt['on_depths'] is 'odd':
        odd_key='on'
        even_key='off'
    else:
        odd_key='off'
        even_key='on'
    deltaf_out={} 

    dt=fh.open_pickle(meta_dt['data_path']+file_names[0]+'.pck')
    

    max_value=[]
    for file_ind,crfile in enumerate(file_names):
            deltaf_out[file_ind]={}
            for key in ['on','off']:
                deltaf_out[file_ind][key]={}
                #deltaf_out[file_ind][key]['fvl']={}
                deltaf_out[file_ind][key]['depth']=[]
                deltaf_out[file_ind][key]['fvl_raw']=[]
        

    fig=plt.figure()
    gs=GridSpec(11,6,figure=fig)
    ax1=fig.add_subplot(gs[0:6,0:2])
    #ax2=fig.add_subplot(gs[3:6,0])
    #ax3=fig.add_subplot(gs[6:9,0])
    ROWCT=0
    plt.set_cmap('viridis')

    for file_ind,crfile in enumerate(file_names):
        if file_ind>0:
            dt=fh.open_pickle(meta_dt['data_path']+crfile+'.pck')
        all_depths=np.array(dt['stim_depths'])[::2]
        stim_height=500
        stim_len=0.1
        
        colors=['c','g','m','b']
        
        #tmlapse_in_s=.11963


        
        #plot mean image and rois
        if file_ind==0:
            
            imobj=ax1.imshow(dt['im_mean'],origin='lower')
            #fpl.adjust_spines(ax1,[])
        
        #for axind,crax in enumerate([ax1,ax2,ax3]):
            
        plt.sca(ax1)
       
        for cr_roi in dt['roi']:
            cr_roi.display_roi(linewidth=0.2)
            
        try:       
            ax1.imshow(dt['stim_mask'][0],cmap='Greens',alpha=0.5,origin='lower')
            ax1.imshow(dt['stim_mask'][1],cmap='Reds',alpha=0.5,origin='lower')
        except:
            tst=1
        #crax.imshow(dt['stim_edges'][CT-1],origin='lower')
            #if axind==1:
             #   crax.set_title('on target')
            #if axind==2:
             #   crax.set_title('off target',color='r')
        imobj.set_clim(300,1100)
        ax1.set_xlim(30,120)
        ax1.set_ylim(20,80)
        ax1.plot([40,40+10/microns_per_pixel],[30,30],'w')
        #fpl.adjust_spines(ax1,[])

        #for crind in np.array(meta_dt['roi_to_plot']):
        roi_ind=meta_dt['roi_to_plot']
        crax=fig.add_subplot(gs[ROWCT:ROWCT+2,2:5])
        fpl.adjust_spines(crax,[])
        ROWCT=ROWCT+2
        
        crax.plot(dt['frame_tms'],dt['mn_roi'][roi_ind],'k',linewidth=0.3)
        stim_tms=np.unique(dt['stim_tms'])
    #add stimulation events to subplot

        for stim_ind,crtime in enumerate(stim_tms):
            crax.plot([crtime,crtime+stim_len],[stim_height,stim_height],'r')
            
            crax.plot(crtime-.5,dt['deltaf_vls']['pre_f'][roi_ind][stim_ind],'<',markersize=2,color='c')
            crax.plot(crtime+.5,dt['deltaf_vls']['pst_f'][roi_ind][stim_ind],'<',markersize=2,color='m')
        
        for depth_ind,cr_depth in enumerate(all_depths):

            crax.text(stim_tms[depth_ind],stim_height+50,str(int(cr_depth)),fontsize=5,color='k')

    #fpl.adjust_spines(ax1,['bottom','left'])
        fpl.adjust_spines(crax,['bottom','left'])
        crax.set_aspect(0.05)
        crax.set_xlim((0,180))
        crax.set_ylim((300,900))
        #crax.get_yaxis().set_ticks([-np.pi,0,np.pi,2*np.pi, 3*np.pi])
        if file_ind==(len(file_names)-1):
            crax.get_xaxis().set_ticklabels(['0','20','40','60','80','100','120','140','160'])
            crax.get_xaxis().set_ticks([0,20,40,60,80,100,120,140,160])
            crax.set_xlabel('time (s)')
        crax.set_ylabel('raw fluorescence')
        #crax.get_yaxis().set_ticklabels(['-180','0','180','360','180'],fontsize=6)
        for stim_ind,crtime in enumerate(stim_tms):
            delta_f=(dt['deltaf_vls']['pst_f'][roi_ind][stim_ind]-dt['deltaf_vls']['pre_f'][roi_ind][stim_ind])/dt['deltaf_vls']['pre_f'][roi_ind][stim_ind]
            target_depth=meta_dt['on_target_depth']
            try:
                
                crdepth=target_depth-all_depths[stim_ind]
            except:
                pdb.set_trace()
                     
            if np.mod(stim_ind,2) == 1:
                crkey=odd_key
            else:
                crkey=even_key

            

            deltaf_out[file_ind][crkey]['fvl_raw'].append(delta_f)
            deltaf_out[file_ind][crkey]['depth'].append(crdepth)
            

        max_value.append(get_max_value(deltaf_out,file_ind))
    
    for file_ind,crfile in enumerate(file_names):
        if file_ind==0:
            axraw=fig.add_subplot(gs[7:,2])
            axnorm=fig.add_subplot(gs[7:,4])
        plt_util.plot_raw_vert(axraw,deltaf_out[file_ind],norm_flag=False)
        axraw.set_xlabel('deltaF/F')
        axraw.set_ylabel('depth relative to dbd plane \n microns')
        #plt_util.plot_raw_vert(axnorm,deltaf_out[file_ind],nmax_value=max_value[file_ind])
        axnorm.set_xlabel('normalized deltaF/F')
        axnorm.set_ylabel('depth relative to dbd plane \n microns')
    outdt={}
    outdt['delta_f']=deltaf_out
    outdt['max_value']=max_value
    crdepths=outdt['delta_f'][0]['on']['depth']
    unq_depths=np.unique(crdepths)
    if len(unq_depths)<len(crdepths):
        deltaf_out=correct_non_unique_depths(deltaf_out,crdepths)
                 
    plt.suptitle(save_fig_file_name)
    plt.savefig(SUMMARY_DATA_LOCATION+save_fig_file_name)

    summary_file=SUMMARY_DATA_LOCATION +save_dat_file_name
    
    fh.save_to_pickle(summary_file, outdt)


def get_max_value(deltaf_out,file_ind):
    
    max_list=[]
    for keyind,key in enumerate(['on','off']):
        max_list.append(np.max(deltaf_out[file_ind][key]['fvl_raw']))
    return np.max(max_list)
    


def correct_non_unique_depths(df,crdepths):
    
    duplicate=[idx for idx, item in enumerate(crdepths) if item in crdepths[:idx]]
    dup=duplicate[0]
    for crkey in df.keys():
        for targkey in df[crkey].keys():
            crdt=df[crkey][targkey]
            comb_inds=np.where(crdt['depth']==crdt['depth'][dup])[0]
            
            df[crkey][targkey]['depth']=crdt['depth'][0:comb_inds[0]] + [crdt['depth'][dup]] +crdt['depth'][comb_inds[1]+1:]
            df[crkey][targkey]['fvl_raw']=crdt['fvl_raw'][0:comb_inds[0]] + [np.mean([crdt['fvl_raw'][dup-1],crdt['fvl_raw'][dup]])] + crdt['fvl_raw'][comb_inds[1]+1:]
    
    return df


# def prep_for_plotting(deltaf_out,max_value):
#     df=deltaf_out
#     flist={}
#     for target_key in deltaf_out:
#         depths=deltaf_out.keys()
#         flist[target_key]=[]
#         for crdepth in depths:
#             flist[target_key].append(flist)



if __name__== "__main__":
  main()

###deltaf['on']['depth']
#deltaf['off']['depth']
####to save, series of depths, relative to target - and raw deltafs....




###
#now plot the means over time in the region of interest
####

#here I don't plot 10th-13th frame b/c that's when stimulation occurs.

