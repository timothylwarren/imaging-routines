import pdb
from py_utilities import tw_filehandling as fh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from py_utilities import fp_library2 as fpl
import plot_utilities as plt_util

colors=['k','r','c','g','m']
summary_data_location='/Users/tim/data/2p_summary_data/'
summary_data_files_to_load=['march25_animal4.pck','march25_animal11.pck','march26_animal4.pck','march26_animal9.pck','march26_animal10.pck','march26_animal10.pck']

fig=plt.figure()
gs=GridSpec(2,2,figure=fig)

axraw={}
axnorm={}

axraw['on']=fig.add_subplot(gs[0,0])
axraw['off']=fig.add_subplot(gs[0,1])

axnorm=fig.add_subplot(gs[1,0])
#axnorm['off']=fig.add_subplot(gs[1,1])


for file_ind,crfile in enumerate(summary_data_files_to_load):
    dt=fh.open_pickle(summary_data_location+crfile)
    #pdb.set_trace()
    delta_f=dt['delta_f']

    ##raw plot
    #for target_key in delta_f.keys():
     #   for depth_key in delta_f[target_key].keys():
      #      num_vls=len(delta_f[target_key][depth_key])
       #     axraw[target_key].plot(depth_key*np.ones(num_vls),delta_f[target_key][depth_key],'o',color=colors[file_ind])

    ##normalized_plot
    fvls_array={}
    for target_key in ['on','off']:
        fvls_sum=[]
        fvls_array[target_key]={}
        for exp_key in delta_f.keys():
            
            fvls_sum.append([delta_f[exp_key][target_key]['fvl']/dt['max_value'][exp_key]])
        
        shape1=np.shape(fvls_sum)[0]
        shape2=np.shape(fvls_sum)[2]
        fvls_array[target_key]['fvl']=np.mean(np.reshape(np.array(fvls_sum),(shape1,shape2)),axis=0)
        pdb.set_trace()
        fvls_array[target_key]['depth']=delta_f[exp_key][target_key]['depth']
    plt_util.plot_raw_vert(axnorm,fvls_array)

                #for crind in np.arange(len(delta_f[target_key][depth_key])):
                #axnorm[target_key].plot(depth_key,delta_f[target_key][depth_key]/dt['max_value'][crind],'o',color=colors[file_ind])

