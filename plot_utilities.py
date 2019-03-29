
import matplotlib.pyplot as plt

import numpy as np
import  pdb

from py_utilities import fp_library2 as fpl
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams["font.family"] = "Arial"
matplotlib.rcParams["font.size"] = 7    
###take a series of on-target depths, plot vertically with distinct colors
###take a series of off-target depths

def plot_raw_vert(ax,fvldt,max_value=0):
    colors=['k','r']
    for crtypeind,crtype in enumerate(fvldt.keys()):
        if max_value:
            fvl=fvldt[crtype]['fvl']/max_value
        else:
            fvl=fvldt[crtype]['fvl']
        ax.scatter(fvl,fvldt[crtype]['depth'],s=20,facecolor='none',edgecolor=colors[crtypeind])
    fpl.adjust_spines(ax,['bottom','left'])
    




