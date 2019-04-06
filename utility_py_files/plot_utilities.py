
import matplotlib.pyplot as plt

import numpy as np
import  pdb

from py_utilities import fp_library2 as fpl
import matplotlib as ml
ml.rcParams['pdf.fonttype'] = 42
ml.rcParams['ps.fonttype'] = 42
ml.rcParams["font.family"] = "Arial"
ml.rcParams["font.size"] = 7    
###take a series of on-target depths, plot vertically with distinct colors
###take a series of off-target depths

def plot_raw_vert(ax,fvldt,norm_flag=True,max_value=0):
    if norm_flag:
        fvlkey='fvl_norm'
    else:
        fvlkey='fvl_raw'
    colors=['k','r']
    for crtypeind,crtype in enumerate(fvldt.keys()):
        
        if max_value:
            fvl=fvldt[crtype][fvlkey]/max_value
        else:
            fvl=fvldt[crtype][fvlkey]
        ax.scatter(fvl,fvldt[crtype]['depth'],s=20,facecolor='none',edgecolor=colors[crtypeind])
    fpl.adjust_spines(ax,['bottom','left'])

def plot_raw(ax,fvldt,norm_flag=True,max_value=0,line_flag=False):
    if norm_flag:
        fvlkey='fvl_norm'
    else:
        fvlkey='fvl_raw'
    colors=['k','r']
    for crtypeind,crtype in enumerate(fvldt.keys()):
        
        if max_value:
            fvl=fvldt[crtype][fvlkey]/max_value
        else:
            fvl=fvldt[crtype][fvlkey]
        col=ml.colors.colorConverter.to_rgba(colors[crtypeind], alpha=.5)
        #rcol=ml.colors.colorConverter.to_rgba('r', alpha=.5)
        ax.scatter(fvldt[crtype]['depth'],fvl,s=15,facecolor='none',edgecolor=col)
        
        if line_flag:
            ax.plot(fvldt[crtype]['depth'],fvl,linewidth=0.2,color=colors[crtypeind])

    fpl.adjust_spines(ax,['bottom','left'])    




