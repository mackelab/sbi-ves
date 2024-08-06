import math
import numpy as np
import matplotlib as mpl
import matplotlib.font_manager
import matplotlib.pyplot as plt
import torch
import config
import types
import time
import IPython.display as IPd


from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple


def process_gimli_results(model):
    '''
    Inversion results of pygimli are represented as a single array containing layer thicknesses and resistivity values. 
    The first half of the array represent the layer thicknesses, whereas the second half of values are the resistivitiy values to that layer thicknesses. 

    The array is initially split and transformed to the depth profile representation choosen for the priors.
    They are extenden to a depth of at least 24m, if the inferred depth profile is too short. 
    As the last layer is assumed to reach to infinity, the last resistivity layers are appendend to complete the depth profile. 
    The layers are mapped to the depth profile representation of small steps of 0.5m. Therefore the layer thicknesses are mapped towards that representation. 

    Returns the in steps of 0.5m from the pygimili inversion. 
    
    '''
    splitpoint = math.floor(model.shape[0]/2)
    thicknesses_pygimli = model[:splitpoint]
    resistivities_pygimli = model[splitpoint:]

    resistivities_inv_pygimli = torch.empty((0,))
    for index, res in enumerate(resistivities_pygimli):
        if (index != (resistivities_pygimli.shape[0]-1)):
            t = thicknesses_pygimli[index]
            meters = int(math.ceil(t * 2) / 2)
            if meters > 1:
                steps = meters*2
            else: 
                steps = 1
            r = torch.linspace(res, res, steps)
            resistivities_inv_pygimli = torch.cat((resistivities_inv_pygimli, r), dim=0)
        else: 
            n_res_values = resistivities_inv_pygimli.shape[0]
            if n_res_values < 48:
                r = torch.linspace(res, res, (48 - n_res_values ))
                resistivities_inv_pygimli = torch.cat((resistivities_inv_pygimli, r), dim=0)
            else:
                r = torch.linspace(res, res, 2)
                resistivities_inv_pygimli = torch.cat((resistivities_inv_pygimli, r), dim=0)
        
    return resistivities_inv_pygimli



def plot_pygimli_depth_results(
    pygimli_res,
    filename,
    gt_res=None,
    gt_step=True,
    step_profile=None, 
    poly_profile=None,
    grid=False,
    legend=False,
    title=False,
    xaxis_label=True,
    yaxis_label=False,
    yaxis_visible=True,
):
     depths = np.linspace(0, 23.5, num=48)
    
     with mpl.rc_context(fname="plots/pltstyle.rc"):
        fig = plt.figure(figsize=(5, 7.5))
        ax1 = fig.add_axes([0.1, 0.1, 0.75, 0.85])

        if step_profile is not None: 
            ax1.plot(step_profile, depths, color=config.posterior_colors[1], linewidth=3, drawstyle='steps-pre', alpha=0.6)

        if poly_profile is not None: 
            ax1.plot(poly_profile, depths, color=config.posterior_colors[1], linewidth=3, marker='_',  markersize=10, alpha=0.6)

        if isinstance(pygimli_res, list):
            for index, (res, n_layer) in enumerate(pygimli_res): 
                pygimli_re_values=res.shape[0]
                pygimli_depth = np.linspace(0, pygimli_re_values/2, num=pygimli_re_values)
                ax1.plot(res, pygimli_depth,  drawstyle='steps-pre', label="{}-Layer Inversion".format(n_layer), linewidth=3.0, color='darkslategray', alpha=1 - 0.2*index)
        else: 
            pygimli_re_values=pygimli_res.shape[0]
            pygimli_depth = np.linspace(0, pygimli_re_values/2, num=pygimli_re_values)
            ax1.plot(pygimli_res, pygimli_depth,  drawstyle='steps-pre', label="{}-Inversion".format(n_layer), linewidth=3.0, color='darkslategray', alpha=0.8)

        if gt_step and gt_res is not None:
            ax1.plot(gt_res, depths, color=config.bright_red, alpha=0.8, label='GT depth profile', linewidth=3.0, drawstyle='steps-pre')
        elif gt_res is not None:
            ax1.plot(gt_res, depths, color=config.bright_red, alpha=0.8, label='GT depth profile', linewidth=3.0, marker='_',  markersize=10)
        
         
        if xaxis_label:
            ax1.set_xlabel("Resistivity  [$\Omega m$]", labelpad=15)
        if yaxis_label:
            ax1.set_ylabel("Depth [m]", labelpad=15)
        if title:
            ax1.set_title("Resistivity Depth Profile", pad=15)
        if legend:
            ax1.legend()
        ax1.grid(grid)
        ax1.invert_yaxis()
        
        
        # Move the bottom spine (x-axis) downwards
        ax1.spines['bottom'].set_position(('outward', 10))  # Move down by 5 points
        
        # Move the left spine (y-axis) to the left
        ax1.spines['left'].set_position(('outward', 10))  # Move left by 5 points
        
        # Hide the top and right spines
        ax1.spines['top'].set_color('none')
        ax1.spines['right'].set_color('none')
        
        # Optionally, adjust the ticks
        ax1.xaxis.set_ticks_position('bottom')
        ax1.yaxis.set_ticks_position('left')
        ax1.get_yaxis().set_visible(yaxis_visible)
        ax1.spines['left'].set_visible(yaxis_visible)
    
        plt.savefig('plots/{}'.format(filename))
        plt.show()
        return 


def plot_pygimli_responses(
    pygimli_app_res,
    gt_app_res,
    filename,
    grid=False,
    legend=False,
    title=False,
    xaxis_label=True,
    yaxis_label=False,
    yaxis_visible=True
):
    electrode_spacing=  np.logspace(np.log10(2), np.log10(100), 23)

    with mpl.rc_context(fname="plots/pltstyle.rc"):
        fig = plt.figure(figsize=(5, 7.5))
        ax2 = fig.add_axes([0.1, 0.1, 0.75, 0.85])
         
        if isinstance(pygimli_app_res, list):
            for index, (app_res, n_layer) in enumerate(pygimli_app_res):
                ax2.plot(app_res, electrode_spacing,  label="{}-Layer Inversion (Response)".format(n_layer), linewidth=3.0, color='darkslategray', alpha=1 - 0.2*index)
        else: 
            ax2.plot(pygimli_app_res, electrode_spacing,  label="{}-Layer Inversion (Response)".format(n_layer), linewidth=3.0, color='darkslategray', alpha=0.8)

         # Plot Grount truth apparent resistivity
        ax2.plot(gt_app_res, electrode_spacing,  color=config.bright_red, marker='x', alpha=0.8, linewidth=3.0, markersize=8)
        
        if xaxis_label:
                ax2.set_xlabel(r"Apparent Resistivity [$\Omega m$]", labelpad=15)
        if yaxis_label:
            ax2.set_ylabel("AB/2 [m]", labelpad=15)
        if title:
            ax2.set_title('Simulated Apparent Resistivity', pad=15)
        
        if legend:
            ax2.legend( loc='best')
        
        ax2.set_yscale('log')
        ax2.invert_yaxis()
        ax2.grid(grid)
        
        # Move the bottom spine (x-axis) downwards
        ax2.spines['bottom'].set_position(('outward', 10)) # Move down by x points
        
        # Move the left spine (y-axis) to the left
        ax2.spines['left'].set_position(('outward', 10))  # Move left by x points
        
        # Hide the top and right spines
        ax2.spines['top'].set_color('none')
        ax2.spines['right'].set_color('none')
        
        # Optionally, adjust the ticks
        ax2.xaxis.set_ticks_position('bottom')
        ax2.yaxis.set_ticks_position('left')
        ax2.get_yaxis().set_visible(yaxis_visible)
        ax2.spines['left'].set_visible(yaxis_visible)
        
        plt.savefig('plots/{}'.format(filename))
        plt.show()
        return 
    