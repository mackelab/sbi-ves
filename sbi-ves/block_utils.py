import matplotlib as mpl
import matplotlib.font_manager
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
import pickle
import config
import torch


def plot_block_depth_results(
    res_samples,
    gt_res, 
    mean_res,
    conf_intervals_res,
    filename,
    step=False,
    mean_step=False,
    legend=False,
    title=False,
    xaxis_label=True,
    yaxis_label=False,
    yaxis_visible=True,
    
):
    percentiles = config.percentiles
    electrode_spacing=  np.logspace(np.log10(2), np.log10(100), 23)
    depths = np.linspace(0, mean_res.shape[0]*0.1, num=mean_res.shape[0], endpoint=False)
    gt_depth = np.linspace(0, 23.5, num=48)
    
    with mpl.rc_context(fname="plots/pltstyle.rc"):
        fig = plt.figure(figsize=(5, 7.5))
        ax1 = fig.add_axes([0.1, 0.1, 0.75, 0.85])

        for idx, percentile in enumerate(percentiles[3:]):
            if idx <= 1: 
                continue
           # ax1.plot(conf_intervals_res[3+idx], depths, color='orange', linestyle='dashed', label='95% CI', linewidth=3.0, alpha=0.6)
            #ax1.plot(conf_intervals_res[2-idx], depths, color='orange', linestyle='dashed', linewidth=3.0, alpha=0.6)
            ax1.fill_betweenx(depths, conf_intervals_res[3+idx], conf_intervals_res[2-idx], alpha=0.5, color=config.dark_yellow) #label=f'{percentiles[3+idx]}% CI')

        if res_samples is not None: 
            for sample in res_samples[:20]:
                if mean_step and mean_step is not None: 
                    ax1.plot(sample, depths, alpha=0.3, color=config.dark_yellow, drawstyle='steps-pre')
                else: 
                    ax1.plot(sample, depths, alpha=0.3, color=config.dark_yellow)
            ax1.plot([], [], color='orange', alpha=0.3, label='Posterior Samples')

        
        # Plot resistivity
        if mean_step: 
            ax1.plot(mean_res, depths, label='Mean', color=config.dark_brown, linewidth=3, drawstyle='steps-pre')
        else:
            ax1.plot(mean_res, depths, label='Mean', color=config.dark_brown, linewidth=3,  marker='_',  markersize=10)

        
        # Plot the Ground Truth
        if step and gt_res is not None:
            ax1.plot(gt_res, gt_depth, color=config.bright_red, alpha=0.8, label='GT depth profile', linewidth=3.0, drawstyle='steps-pre')
        elif gt_res is not None:
            ax1.plot(gt_res, gt_depth, color=config.bright_red, alpha=0.8, label='GT depth profile', linewidth=3.0, marker='_',  markersize=10)

        if xaxis_label:
            ax1.set_xlabel("Resistivity  [$\Omega m$]", labelpad=15)
        if yaxis_label:
            ax1.set_ylabel("Depth [m]", labelpad=15)
        if title:
            ax1.set_title("Resistivity Depth Profile", pad=15)
        if legend:
            ax1.legend()
        ax1.grid(False)
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
        return 
    

def split_params(res_n_depth):
    ''' 
    Split a block sample into its resistivity values and the layer thicknesses
    '''
    number_of_layers = int( (len(res_n_depth)+1) /2)
    # First half of parameters is resistivities
    resistivities = res_n_depth[:number_of_layers]
    # Second half of parameters are thicknesses
    thicknesses = res_n_depth[number_of_layers:]
    return resistivities, thicknesses


def thickness_to_depth(t):
    ''' 
    Convert the individual layer thicknesses to a depth profile as the layers are stacked on top of each other
    '''
    last_layer_tickness = torch.tensor([1.0])
    thickness_to_depth = np.cumsum(torch.cat((t, last_layer_tickness)))
    return thickness_to_depth


def transfrom_and_find_max_reached_depth(block_samples):
    """
    Transforms block samples to their depth pfoiles and finds the maximum reached depth of the samples. 
    The maximal depth is needed to later extend all samples to the same max. depth, to make conversion easier later on.

    Returns:
        - inv_res_thick_depth (list of tuples): A list containing tuples of resistivity, thickness, and depth.
        - max_depth (float): The maximum depth reached among all samples
    """

    
    inv_res_thick_depth = []
    max_depth = 0
    for sample in block_samples: 
        res, thick = split_params(sample)
        depth = thickness_to_depth(thick)
        inv_res_thick_depth.append((res, thick, depth))

        if depth[-1] >= max_depth:
            max_depth = depth[-1]
        
    return inv_res_thick_depth, torch.round(max_depth ,decimals=1)




def map_resistivities_to_depth (res_thick_depth, max_depth):
    '''
    Takes the inputs of transfrom_and_find_max_reached_depth.
    This function maps all depth profiles of the samples to the same max. depth of the deepest sample at a resolutoin of 0.1m, to make comparison and conversion easier among samples. 

    Returns 
        - mapped high resolutional depth profiles of each sample.
    '''
    
    
    step_size = 0.1
    num_steps = max_depth/step_size
    samples = []
    for res, thick, depth in res_thick_depth:
        transformed_sample = []
        for ind, r  in enumerate(res):
            # when last layer is reached, fill until the max. reached depth with the last resistiviy value
            if (ind == 3):
                remaining_steps = int(num_steps - len(transformed_sample))
                transformed_sample.extend(r.repeat(1,remaining_steps).tolist()[0])
            else: 
                layer_steps = int(torch.round(thick[ind], decimals=1) /step_size)
                transformed_sample.extend(r.repeat(1,layer_steps).tolist()[0])
        samples.append(transformed_sample)
    return samples





def transform_to_lower_res_samples(samples):
    '''
    Transform a high resolutional depth profile into a lower resolutional depth profile to compare against GT's from other priors. 
    As the resolution of a block sample is at higher resolutional steps of 0.1m I sample every fifth value from that profile to compare with the dephts of other priors until a depht of 24m. 
    '''
    trans_samples = []
    for sample in samples: 
        t_sample = sample[::5][:48]
        trans_samples.append(t_sample)
    return trans_samples






