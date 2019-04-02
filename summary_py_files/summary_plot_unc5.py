import pdb
from py_utilities import tw_filehandling as fh
import matplotlib.pyplot as plt
import matplotlib as ml
import numpy as np
from matplotlib.gridspec import GridSpec
from py_utilities import fp_library2 as fpl
import plot_utilities as plt_util
import scipy
ROUND_TO_NEAREST=10

colors=['k','r','c','g','m']
summary_data_location='/Users/tim/data/2p_summary_data/'
summary_data_files_to_load=['march27_unc-5_animal4.pck','march27_unc-5_animal3.pck','march27_unc-5_animal7.pck','unc-5_animal5.pck','unc-5_animal4.pck']

fig=plt.figure(figsize=(.5,1.5))
gs=GridSpec(3,6,figure=fig)

axraw={}
axnorm={}

#axraw['on']=fig.add_subplot(gs[0,0])
#axraw['off']=fig.add_subplot(gs[0,1])

axnorm=fig.add_subplot(gs[0:2,0:3])
axsum=fig.add_subplot(gs[0:2,4])
depth_for_analysis={}
depth_for_analysis['on']=0
depth_for_analysis['off']=-20
#axnorm['off']=fig.add_subplot(gs[1,1])

def main():
    mn_by_animal={}
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
            if file_ind==0:
                mn_by_animal[target_key]=[]
            fvls_sum={}

            fvls_sum['raw']=[]
            fvls_sum['norm']=[]
            fvls_array[target_key]={}
            for expind,exp_key in enumerate(delta_f.keys()):
                #in this file there is an erroneous extra depth in one of the runs
                #if crfile == 'wt_animal3.pck':
                try:
                    fvls_to_add=delta_f[exp_key][target_key]['fvl']
                except:
                    fvls_to_add=delta_f[exp_key][target_key]['fvl_raw']
                norm_fvls_to_add=fvls_to_add/dt['max_value'][exp_key]
                #else:
                 #   fvls_to_add=delta_f[exp_key][target_key]['fvl']
                  #  norm_fvls_to_add=fvls_to_add/dt['max_value'][exp_key]

                fvls_sum['norm'].append(norm_fvls_to_add)
                if expind>0:
                    crlen=len(fvls_sum['raw'][0])
                    if len(fvls_to_add)>crlen:
                        pdb.set_trace()
                        fvls_to_add=fvls_to_add[0:crlen]
                fvls_sum['raw'].append(fvls_to_add)
            
                shape1=np.shape(fvls_sum['norm'])[0]
            if len(np.shape(fvls_sum['norm']))==2:
                shape=np.shape(fvls_sum['norm'])
           
            
            fvls_array[target_key]['fvl_norm']=np.mean(np.array(fvls_sum['norm']),axis=0)
            try:
                fvls_array[target_key]['fvl_raw']=np.mean(np.array(fvls_sum['raw']),axis=0)
            except:
                pdb.set_trace()
            tmp_depth=delta_f[0][target_key]['depth']
            if ROUND_TO_NEAREST:
                fvls_array[target_key]['depth']=myround(np.array(tmp_depth),base=ROUND_TO_NEAREST)
            else:
                fvls_array[target_key]['depth']=np.array(tmp_depth)
            
          
            mn_by_animal[target_key].append(calc_mean_for_animal_over_depth_range(fvls_array[target_key],target_key))
            
           
            norm_flag=False
            #round=True
            
            
            plt_util.plot_raw(axnorm,fvls_array,norm_flag,line_flag=True)
        fpl.adjust_spines(axnorm,['left','bottom'])
        axnorm.set_ylim(-.25,0.75)
        axnorm.set_yticks([-.25,0,0.25,0.5,0.75])
        axnorm.set_xlim(-62,42)    
    plot_sum_for_each_animal(axsum,mn_by_animal)

def calc_mean_for_animal_over_depth_range(fin,target_key):
    depth=fin['depth']
    
    crdepth=depth_for_analysis[target_key]
    inds=np.where((depth==crdepth))[0]
    try:
        return np.mean(fin['fvl_raw'])
    except:
        pdb.set_trace()
    
def plot_sum_for_each_animal(axsum,mn_by_animal):
    kcol=ml.colors.colorConverter.to_rgba('k', alpha=.5)
    rcol=ml.colors.colorConverter.to_rgba('r', alpha=.5)
    axsum.scatter(np.zeros(len(mn_by_animal['on'])),mn_by_animal['on'],s=15,facecolor='none',edgecolor=kcol)

    axsum.scatter(np.ones(len(mn_by_animal['off']))-.5,mn_by_animal['off'],s=15,facecolor='none',edgecolor=rcol)
    for crind, cr_on in enumerate(mn_by_animal['on']):
        cr_off=mn_by_animal['off'][crind]
        axsum.plot([0,0.5],[cr_on,cr_off],color='k',linewidth=0.2)

    mn_on=np.mean(mn_by_animal['on'])
    mn_off=np.mean(mn_by_animal['off'])
    rel_stats=scipy.stats.ttest_rel(mn_by_animal['on'],mn_by_animal['off'])
    off_target_rel_to_zero_stats=scipy.stats.ttest_1samp(mn_by_animal['off'],0)
    
    plt.plot(1.1,mn_on,'<',Markersize=3,MarkerEdgeColor=None,color='k')
    plt.plot(1.1,mn_off,'<',Markersize=3,MarkerEdgeColor=None,color='r')
    axsum.set_ylim(-.25,1.25)
    axsum.set_aspect(4)
    axsum.set_yticks([-.25,0,.25,.5,.75])
    axsum.set_xlim(-.2,1.2)
    fpl.adjust_spines(axsum,['left'])
    #pdb.set_trace()
    axsum.set_ylim(-.25,1.25)
    axsum.set_aspect(4)
    axsum.set_yticks([-.25,0,.25,.5,.75,1.0,1.25])
    axsum.set_xlim(-.2,1.2)



    



def myround(x, base=10):
    
    return base * np.round(x/base)
if __name__== "__main__":
  main()
   
                #for crind in np.arange(len(delta_f[target_key][depth_key])):
                #axnorm[target_key].plot(depth_key,delta_f[target_key][depth_key]/dt['max_value'][crind],'o',color=colors[file_ind])

