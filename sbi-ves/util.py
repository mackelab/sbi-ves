import matplotlib as mpl
import matplotlib.font_manager
import matplotlib.pyplot as plt
import numpy as np
import pickle
import config
import types
import time
import IPython.display as IPd

from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error



def svg(img):
    IPd.display(IPd.HTML('<img src="{}" / >'.format(img, time.time())))

def rmse(sample, gt): 
    return np.sqrt(mean_squared_error(gt, sample))

def avg_rmse(gt, samples):
    rmse = []
    for sample in samples: 
        if not np.isnan(sample).all():
            rmse.append(np.sqrt(mean_squared_error(gt, sample)))
        else:
            continue
        
    return np.average(rmse)



def plot_measurement(electrode_spacing,
                     apparent_resistivities,
                     xlog=True,
                     ylog=True,
                     grid=True,
                     label="",
                     xlabel="AB/2 (m)",
                     ylabel="Apparent Resistivity ($\Omega m$)",
                     ylimit=[10, 1000]):
    # Plot apparent resistivities on sounding curve# Plot apparent resistivities on sounding curve
    fig = plt.figure(figsize=(11, 5))
    ax1 = fig.add_axes([0.1, 0.1, 0.75, 0.85])
    ax1.plot(electrode_spacing, apparent_resistivities, marker='o', label=label)
    ax1.set_ylim(ylimit)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    if xlog:
        ax1.set_xscale('log')
    if ylog:
        ax1.set_yscale('log')
    plt.grid(grid, which="both", ls="-")
    plt.show()


def pickle_objects(objects, filename):
    with open(filename, "wb") as f:
        pickle.dump(objects, f)


def unpickle_objects(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def plot_pygimli_depth_results(
    pygimli_res,
    filename,
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
            ax1.plot(step_profile, depths, color=config.dark_brown, linewidth=3, drawstyle='steps-pre', alpha=1)

        if poly_profile is not None: 
            ax1.plot(poly_profile, depths, color=config.dark_brown, linewidth=3, marker='_',  markersize=10, alpha=1)

        if isinstance(pygimli_res, list):
            for index, (res, n_layer) in enumerate(pygimli_res): 
                pygimli_re_values=res.shape[0]
                pygimli_depth = np.linspace(0, pygimli_re_values/2, num=pygimli_re_values)
                ax1.plot(res, pygimli_depth,  drawstyle='steps-pre', label="{}-Layer Inversion".format(n_layer), linewidth=3.0, color='darkslategray', alpha=1 - 0.2*index)
        else: 
            pygimli_re_values=pygimli_res.shape[0]
            pygimli_depth = np.linspace(0, pygimli_re_values/2, num=pygimli_re_values)
            ax1.plot(pygimli_res, pygimli_depth,  drawstyle='steps-pre', label="{}-Inversion".format(n_layer), linewidth=3.0, color='darkslategray', alpha=0.8)

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
        ax1.spines['bottom'].set_position(('outward', 10)) 
        
        # Move the left spine (y-axis) to the left
        ax1.spines['left'].set_position(('outward', 10)) 
        
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
        return 
    

def plot_depth_profile_with_ci(
    res_samples,
    gt_res, 
    mean_res,
    conf_intervals_res,
    filename,
    pygimli_res=None,
    step=False,
    mean_step=False,
    grid=False,
    legend=False,
    title=False,
    xaxis_label=True,
    yaxis_label=False,
    yaxis_visible=True,
):
    percentiles = config.percentiles
    depths = np.linspace(0, 23.5, num=48)
    electrode_spacing=  np.logspace(np.log10(2), np.log10(100), 23)
    
    with mpl.rc_context(fname="plots/pltstyle.rc"):
        fig = plt.figure(figsize=(5, 7.5))
        ax1 = fig.add_axes([0.1, 0.1, 0.75, 0.85])
        
        #ax1.plot(resistivities_inv_pygimli, depths_pygimli,  drawstyle='steps', color='orange', label="Classic Inversion")
        for idx, percentile in enumerate(percentiles[3:]):
            if idx <= 1: 
                continue
            #ax1.plot(conf_intervals_res[3+idx], depths, color=config.colors_hex[0], linestyle='dashed', label='95% CI', linewidth=3.0, alpha=0.6)
            #ax1.plot(conf_intervals_res[2-idx], depths, color=config.colors_hex[0], linestyle='dashed', linewidth=3.0, alpha=0.6)
            ax1.fill_betweenx(depths, conf_intervals_res[3+idx], conf_intervals_res[2-idx], alpha=0.5, color=config.dark_yellow) #label=f'{percentiles[3+idx]}% CI')
    
        if res_samples is not None: 
            for sample in res_samples[:20]:
                if mean_step and mean_step is not None: 
                    ax1.plot(sample, depths, alpha=0.3, color=config.dark_yellow, drawstyle='steps-pre')
                else: 
                    ax1.plot(sample, depths, alpha=0.3, color=config.dark_yellow)
            ax1.plot([], [], color=config.light_yellow, alpha=0.1, label='Posterior Samples')
            
        

        # Plot resistivity
        if mean_step: 
            ax1.plot(mean_res, depths, label='Mean', color=config.dark_brown, linewidth=3, drawstyle='steps-pre')
        else:
            ax1.plot(mean_res, depths, label='Mean', color=config.dark_brown, linewidth=3,  marker='_',  markersize=10)


        
        # Plot the Ground Truth
        if step and gt_res is not None:
            ax1.plot(gt_res, depths, color=config.bright_red, alpha=0.8, label='GT depth profile', linewidth=3.0, drawstyle='steps-pre')
        elif gt_res is not None:
            ax1.plot(gt_res, depths, color=config.bright_red, alpha=0.8, label='GT depth profile', linewidth=3.0, marker='_',  markersize=10)
        
    
        if pygimli_res is not None: 
            if isinstance(pygimli_res, list):
                for res, n_layer in pygimli_res: 
                    pygimli_re_values=res.shape[0]
                    pygimli_depth = np.linspace(0, pygimli_re_values/2, num=pygimli_re_values)
                    ax1.plot(res, pygimli_depth,  drawstyle='steps-pre', label="{}-Layer Inversion".format(n_layer), linewidth=3.0, color='darkred', alpha=0.6)
            else: 
                pygimli_re_values=pygimli_res.shape[0]
                pygimli_depth = np.linspace(0, pygimli_re_values/2, num=pygimli_re_values)
                ax1.plot(pygimli_res, pygimli_depth,  drawstyle='steps-pre', label="{}-Inversion".format(n_layer), linewidth=3.0, color='darkred', alpha=0.8)
    
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
        return 


def plot_app_res_with_ci(
    app_res_samples,
    gt_app_res,
    mean_app_res,
    conf_intervals_app_res,
    filename,
    pygimli_app_res=None,
    grid=False,
    legend=False,
    title=False,
    yaxis_visible=True,
    xaxis_label=True,
    yaxis_label=False,
):

    percentiles = config.percentiles
    depths = np.linspace(0, 23.5, num=48)
    electrode_spacing=  np.logspace(np.log10(2), np.log10(100), 23)


    with mpl.rc_context(fname="plots/pltstyle.rc"):
        fig = plt.figure(figsize=(5, 7.5))
        ax2 = fig.add_axes([0.1, 0.1, 0.75, 0.85])
    
        
        for idx, percentile in enumerate(percentiles[3:]):
            if idx <= 1: 
                continue
            #ax2.plot(conf_intervals_app_res[3+idx], electrode_spacing, color=config.colors_hex[3], linestyle='dashed', label='95% confidence',alpha=0.6,  linewidth=3.0)
            #ax2.plot(conf_intervals_app_res[2-idx], electrode_spacing, color=config.colors_hex[3], linestyle='dashed', alpha=0.6, linewidth=3.0)
            ax2.fill_betweenx(electrode_spacing, conf_intervals_app_res[3+idx], conf_intervals_app_res[2-idx], alpha=0.5, color=config.light_purple ) #, label=f'{percentiles[3+idx]}% CI')
    
        if app_res_samples is not None: 
            for sample in app_res_samples[:40]:
                ax2.plot(sample, electrode_spacing, alpha=0.2, color=config.light_purple)
            ax2.plot([], [], color=config.dark_blue, alpha=0.2, label='Simulated Posterior Samples')
    
        # Plot mean apparent resistivity
        ax2.plot(mean_app_res, electrode_spacing, label='Mean', alpha=1, linewidth=4.0, color=config.dark_purple)
        
        if pygimli_app_res is not None: 
            if isinstance(pygimli_app_res, list):
                for app_res, n_layer in pygimli_app_res:
                    ax2.plot(app_res, electrode_spacing,  label="{}-Layer Inversion (Response)".format(n_layer), linewidth=3.0, color='darkred', alpha=0.8)
            else: 
                ax2.plot(pygimli_app_res, electrode_spacing,  label="{}-Layer Inversion (Response)".format(n_layer), linewidth=3.0, color='darkred', alpha=0.8)


        # Plot Grount truth apparent resistivity
        ax2.plot(gt_app_res, electrode_spacing,  color=config.bright_red, marker='x', label="GT App. Resistivity", alpha=1, linewidth=4.0, markersize=10)
        
        if xaxis_label:
            ax2.set_xlabel(r"Apparent Resistivity [$\Omega m$]", labelpad=15)
        if yaxis_label:
            ax2.set_ylabel("AB/2 [m]", labelpad=15)
        if title:
            ax2.set_title('Simulated Apparent Resistivity', pad=15)

        
        
        
        
        
        # ******* LEGEENNNNEDARY LEGEND **********
        
        if legend:
            
            legend_elements = [
                # Mean legend
                (
                Line2D([0],[0],  color=config.dark_brown,  linewidth=4, alpha=1),
                Line2D([0],[0],  color=config.dark_purple, linewidth=4, alpha=1)
                ),
                # 95% CI
                (
                Line2D([0],[0],  color=config.dark_yellow, linewidth=8, label='95% confidence',alpha=0.8),
                Line2D([0],[0],  color=config.light_purple, linewidth=8, alpha=0.8)
                ),
                # Simulations
                (
                Line2D([0],[0], color=config.dark_yellow, linewidth=3, alpha=0.8),
                Line2D([0],[0], color=config.light_purple, linewidth=3, alpha=0.8)
                ),
                # Observed App. Res
                (
                Line2D([0],[0], color=config.bright_red, marker='x', alpha=0.8, linewidth=4.0, markersize=8)
                )
            ]
            ax2.legend(
                legend_elements, ['Mean', '95% confidence', '(Predictive) Posterior Samples', 'Observation'],  handler_map={tuple: HandlerTuple(ndivide=None)}, handlelength=4, loc='center')





        
        ax2.set_yscale('log')
        ax2.invert_yaxis()
        ax2.grid(grid)
     
        # Move the bottom spine (x-axis) downwards
        ax2.spines['bottom'].set_position(('outward', 10))  # Move down by x points
        
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
    

 
def plot_depth_profile_and_app_res_with_ci(
    res_samples,
    gt_res, 
    mean_res,
    conf_intervals_res,
    app_res_samples,
    gt_app_res,
    mean_app_res,
    conf_intervals_app_res,
    filename,
    pygimli_res=None,
    pygimli_app_res=None,
    step=False,
    mean_step=False,
    grid=False,
    yaxis_visible=False
):
    percentiles = config.percentiles
    depths = np.linspace(0, 23.5, num=48)
    electrode_spacing=  np.logspace(np.log10(2), np.log10(100), 23)

    with mpl.rc_context(fname="plots/pltstyle.rc"):
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 7.5))
        
        #ax1.plot(resistivities_inv_pygimli, depths_pygimli,  drawstyle='steps', color='orange', label="Classic Inversion")
        for idx, percentile in enumerate(percentiles[3:]):
            if idx <= 1: 
                continue
            ax1.plot(conf_intervals_res[3+idx], depths, color='orange', linestyle='dashed', label='95% confidence')
            ax1.plot(conf_intervals_res[2-idx], depths, color='orange', linestyle='dashed')
            ax1.fill_betweenx(depths, conf_intervals_res[3+idx], conf_intervals_res[2-idx], alpha=0.2, color='orange',label=f'{percentiles[3+idx]}% CI')
    
        if res_samples is not None: 
            for sample in res_samples[:20]:
                if step and step is not None: 
                    ax1.plot(sample, depths, alpha=0.1, color='orange', drawstyle='steps-pre')
                else: 
                    ax1.plot(sample, depths, alpha=0.1, color='orange')
    
        # Plot the Ground Truth
        if step and gt_res is not None:
            ax1.plot(gt_res, depths, color=config.posterior_colors[0], alpha=0.8, label='GT depth profile', linewidth=3.0, drawstyle='steps-pre')
        elif gt_res is not None:
            ax1.plot(gt_res, depths, color=config.posterior_colors[0], alpha=0.8, label='GT depth profile', linewidth=3.0, marker='_', markersize=10)
        
        # Plot resistivity
        if mean_step: 
            ax1.plot(mean_res, depths, label='Mean', color=config.posterior_colors[1], linewidth=2.5, drawstyle='steps-pre')
        else:
            ax1.plot(mean_res, depths, label='Mean', color=config.posterior_colors[1], linewidth=2.0,  marker='_', markersize=10)
    
        if pygimli_res is not None: 
            pygimli_re_values=pygimli_res.shape[0]
            pygimli_depth = np.linspace(0, pygimli_re_values/2, num=pygimli_re_values)
            ax1.plot(pygimli_res, pygimli_depth,  drawstyle='steps-pre', label="Classical Inversion", linewidth=3.0, color='darkred', alpha=0.8)
    
        
        ax1.set_xlabel("Resistivity  [$\Omega m$]", labelpad=15)
        ax1.set_ylabel("Depth [m]", labelpad=15)
        ax1.set_title("Resistivity Depth Profile", pad=15)
        #ax1.legend()
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
        
    
        # Plot mean apparent resistivity
        ax2.plot(mean_app_res, electrode_spacing, label='Mean', alpha=0.8, linewidth=4.0, color=config.simulation_colors[0])
        
        # Plot Grount truth apparent resistivity
        ax2.plot(gt_app_res, electrode_spacing,  color='firebrick', marker='x', label="GT App. Resistivity", alpha=0.8, linewidth=2.0, markersize=8)
    
        
        for idx, percentile in enumerate(percentiles[3:]):
            if idx <= 1: 
                continue
            ax2.plot(conf_intervals_app_res[3+idx], electrode_spacing, color=config.simulation_colors[0], linestyle='dashed', label='95% confidence',alpha=0.2,)
            ax2.plot(conf_intervals_app_res[2-idx], electrode_spacing, color=config.simulation_colors[0], linestyle='dashed', alpha=0.2,)
            ax2.fill_betweenx(electrode_spacing, conf_intervals_app_res[3+idx], conf_intervals_app_res[2-idx], alpha=0.2, color=config.simulation_colors[0], label=f'{percentiles[3+idx]}% CI')
    
        if app_res_samples is not None: 
            for sample in app_res_samples[:40]:
                ax2.plot(sample, electrode_spacing, alpha=0.1, color='darkblue')
        
    
        if pygimli_app_res is not None: 
            ax2.plot(pygimli_app_res, electrode_spacing,  label="Classical Inversion", linewidth=3.0, color='darkred', alpha=0.8)
    
        
        ax2.set_xlabel(r"Apparent Resistivity [$\Omega m$]", labelpad=15)
        ax2.set_ylabel("AB/2 [m]", labelpad=15)
        ax2.set_title('Simulated Apparent Resistivity', pad=15)
        ax2.set_yscale('log')
        #ax2.legend( loc='best')
        ax2.invert_yaxis()
        ax2.grid(grid)
        
        # Move the bottom spine (x-axis) downwards
        ax2.spines['bottom'].set_position(('outward', 10))  # Move down by x points
        
        # Move the left spine (y-axis) to the left
        ax2.spines['left'].set_position(('outward', 10))   # Move left by x points
        
        # Hide the top and right spines
        ax2.spines['top'].set_color('none')
        ax2.spines['right'].set_color('none')
        
        # Optionally, adjust the ticks
        ax2.xaxis.set_ticks_position('bottom')
        ax2.yaxis.set_ticks_position('left')
        ax2.get_yaxis().set_visible(yaxis_visible)
        
        
        plt.subplots_adjust(wspace=0.3)  # Increase the width space between the subplots
        
        plt.savefig('plots/{}'.format(filename))
        return 



