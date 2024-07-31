import numpy as np
import ot
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
import seaborn as sn
import pandas as pd
from pathlib import Path
from sklearn.utils import check_random_state
from sklearn.datasets import make_moons
# User functions
from utils import BaseTransport, GaussianTransport, get_trajectories_for_plotting, get_desiderata, W2_dist
from IPython.display import Markdown

# Setting so that the plots look normal even when using dark-reader
sn.set_style("whitegrid")
#plt.style.use('seaborn-white')
sn.set_context(context="paper")
pal = sn.color_palette("Set1")

# Setting up specifics for plotting + saving
save_figures = True
add_legend = False
add_title = False
add_axis = False
point_alpha_value = 1
trajectory_parms = {'alpha': 0.15, 'linewidth': 2, 'zorder':10}
mpl.rcParams['lines.markersize'] = 8  # a global parameter for marker sizes
X_parms = {'color': pal[1], 'alpha':point_alpha_value, 'marker':'D', 'zorder':20}
Y_parms = {'color': pal[0], 'alpha':point_alpha_value, 'marker':'v', 'zorder':0}
Z_parms = {'color': pal[2], 'alpha':point_alpha_value, 'marker':'^', 'zorder':30}
save_parms = {'format': 'pdf','bbox_inches':'tight', 'pad_inches':0, 'transparent':True}
contour_parms = {'linewidths':3}
cluster_markers = list('8s*Xd.HP')  # a list of keywords for matploblib markers
if save_figures:
    figure_dir = Path('.') / 'figures' / 'main-figure'  # saves all figures in a figure directory in the local directory
    if not figure_dir.exists():
        figure_dir.mkdir(parents=True)
#%%
def col_print(s, col):
    color = ''
    for c in col:
        color += str(hex(int(c*255)))[2:]
    display (Markdown(f'<span style="color: #{color}">{s}</span>'))
#%%
# ergonomic blank space : )
point_alpha_value = 1
rng = np.random.RandomState(42)

X_parms = {'color': pal[1], 'alpha':point_alpha_value, 'marker':'D', 'zorder':20}
Y_parms = {'color': pal[0], 'alpha':point_alpha_value, 'marker':'v', 'zorder':0}
Z_parms = {'color': pal[2], 'alpha':point_alpha_value, 'marker':'^', 'zorder':30}

n_samples_showing = 100
mixture_points_to_show = rng.choice(X.shape[0], size=n_samples_showing, replace=False)

T = BaseTransport(X, Y)
Z_OT = T.forward(X, Y)
for n_clusters in range(1, max_clusters + 1):
    plt.scatter(*Y[mixture_points_to_show].T, label='Y', **Y_parms)
    Z_clusters, labels = T.cluster_forward(X, n_clusters, unconstrained_Z=Z_OT, return_labels=True)
    for cluster_idx in range(n_clusters):
        # plotting
        cluster_points_to_show = mixture_points_to_show[labels[mixture_points_to_show] == cluster_idx]
        #         plt.scatter(*X[cluster_points_to_show].T, label=f'$X_{cluster_idx}$',
        #                     color=pal[cluster_idx+1], alpha=X_parms['alpha'], marker=cluster_markers[cluster_idx])
        plt.scatter(*X[cluster_points_to_show].T, label=f'$X_{cluster_idx}$', **X_parms)
        plt.scatter(*Z_clusters[cluster_points_to_show].T, label=f'$T(C_{{X_{cluster_idx}}})$',
                    color=pal[cluster_idx + 2], alpha=Z_parms['alpha'], marker=cluster_markers[cluster_idx])
        #         plt.scatter(*Z_clusters[cluster_points_to_show].T, label=f'$T(C_{{X_{cluster_idx}}})$',
        #                     color=Z_parms['color'], alpha=Z_parms['alpha'], marker=cluster_markers[cluster_idx])
        cluster_trajactories = get_trajectories_for_plotting(X[cluster_points_to_show],
                                                             Z_clusters[cluster_points_to_show])
        plt.plot(*cluster_trajactories, color=pal[cluster_idx + 2], **trajectory_parms)
        #         plt.plot(*cluster_trajactories, color=Z_parms['color'], **trajectory_parms)
        with np.printoptions(precision=2):
            cluster_mean_shift = Z_clusters[cluster_points_to_show].mean(axis=0) - X[cluster_points_to_show].mean(
                axis=0)
            col_print(f'C_src_{cluster_idx} has shifted by {cluster_mean_shift}', pal[cluster_idx + 2])

    if add_title: plt.title(f'Mean Shift Transport of Clusters, $k={n_clusters}$')
    if not add_axis: plt.axis('off')
    if add_legend: plt.legend()
    if save_figures: plt.savefig(
        figure_dir / f'main-figure-cluster-transport-{n_clusters}-clusters-{max_clusters}-mixtures.{save_parms["format"]}',
        **save_parms)
    plt.show()
    # getting desiderata information
    get_desiderata(X, Y, Z_clusters, inter=n_clusters)
    print('\n\n')