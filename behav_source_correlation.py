import numpy as np
import mne
import pandas as pd
import random
from scipy import stats
from mayavi import mlab
import matplotlib.pyplot as plt
plt.ion()

from sklearn.linear_model import LinearRegression

from mne.stats.cluster_level import _setup_connectivity, _find_clusters, \
    _reshape_clusters

# setup files and folders, subject lists

mri_dir = "D:/freesurfer/subjects/"
meg_dir  = "D:/SOMA Daten/data MNE/"
behav_dir= "C:/Users\muellena/Desktop/Desktop/Experiment Somatosensorik/Verhaltensdaten/"
save_dir= "C:/Users\muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Results/alpha05 loud corr/"
sub_dict = {"SOM_10":"WOO07","SOM_13":"KIO12","SOM_15":"SAG13","SOM_17":"TGH11","SOM_19":"fsaverage","SOM_22":"BLE94","SOM_23":"KER27","SOM_24":"EAM11",
           "SOM_25":"MUN79","SOM_26":"KIL72","SOM_27":"DEN59","SOM_29":"fsaverage","SOM_30":"HIU14","SOM_31":"FOT12",
           "SOM_32":"BII41","SOM_33":"WAL70","SOM_34":"NAG83","SOM_35":"EAM67","SOM_36":"fsaverage"}

# get the behavioral data array ready & choose the variable
Diff_behav = pd.read_csv('{}loud_SOMA_relaxMinusTense.csv'.format(behav_dir),header=None)
#Diff_behav = pd.read_csv('{}how_SOMA_relaxMinusTense.csv'.format(behav_dir),header=None)
Behav = np.array(Diff_behav[0])

# prepare the data arrays / objects needed
all_diff = []  # list for averaging and plotting group STC
X_diff = []  #  list for collecting data for cluster stat analyses
for meg,mri in sub_dict.items():
    # load the STC data
    stc_fsavg_diff = mne.read_source_estimate("{}{}-stc_fsavg_diff_alpha2".format(meg_dir,meg), subject='fsaverage')  ## loads both lh and rh
    # collect the individual stcs into lists for averaging later
    all_diff.append(stc_fsavg_diff)
    X_diff.append(stc_fsavg_diff.data.transpose(1,0))

# create group average stc for plotting later
stc_sum = all_diff.pop()
for stc in all_diff:
    stc_sum = stc_sum + stc
SOMA_all_stc_diff = stc_sum / len(sub_dict)

# make data array for cluster permutation stats RELAX-TENSE stc vals
X_diff = np.array(X_diff).squeeze()
# calculate Pearson's r for each vertex to Behavioral variable of the subject
X_Rval = np.empty(X_diff.shape[1])
X_R_Tval = np.empty(X_diff.shape[1])
for vert_idx in range(X_diff.shape[1]):
    X_Rval[vert_idx], p = stats.pearsonr(X_diff[:,vert_idx],Behav)
# calculate an according t-value for each r
X_R_Tval = (X_Rval * np.sqrt((len(sub_dict)-2))) / np.sqrt(1 - X_Rval**2)
# setup for clustering -- t-thresholds
n_subjects=len(sub_dict)
p_threshold = 0.05
t_threshold = -stats.distributions.t.ppf(p_threshold / 2., n_subjects - 1)
src = mne.read_source_spaces("{}fsaverage-src.fif".format(mri_dir))
connectivity = mne.spatial_src_connectivity(src)
# find clusters in the T-vals
clusters, cluster_stats = _find_clusters(X_R_Tval,threshold=t_threshold,
                                                  connectivity=connectivity,
                                                  tail=0)
# plot uncorrected correlation t-values on fsaverage
X_R_Tval = np.expand_dims(X_R_Tval, axis=1)
SOMA_all_stc_diff.data = X_R_Tval
SOMA_all_stc_diff.plot(subjects_dir=mri_dir,subject='fsaverage',surface='white',hemi='both',time_viewer=True,colormap='coolwarm',clim={'kind':'value','pos_lims':(0,1.5,3)})

# do the random sign flip permutation
# setup
n_perms = 500
cluster_H0 = np.zeros(n_perms)
# here comes the loop
for i in range(n_perms):
    if i in [10,20,50,100,200,300,400]:
        print("{} th iteration".format(i))
    # permute the behavioral values over subjects
    Beh_perm = random.sample(list(Behav),k=len(sub_dict))
    # calculate Pearson's r for each vertex to Behavioral variable of the subject
    XP_Rval = np.empty(X_diff.shape[1])
    XP_R_Tval = np.empty(X_diff.shape[1])
    for vert_idx in range(X_diff.shape[1]):
        XP_Rval[vert_idx], p = stats.pearsonr(X_diff[:,vert_idx],Beh_perm)
    # calculate an according t-value for each r
    XP_R_Tval = (XP_Rval * np.sqrt((len(sub_dict)-2))) / np.sqrt(1 - XP_Rval**2)
    # now find clusters in the T-vals
    perm_clusters, perm_cluster_stats = _find_clusters(XP_R_Tval,threshold=t_threshold,
                                                      connectivity=connectivity,
                                                      tail=0)
    if len(perm_clusters):
        cluster_H0[i] = perm_cluster_stats.max()
    else:
        cluster_H0[i] = np.nan
# get lower CI bound from cluster mass H0
clust_threshold = np.quantile(cluster_H0[~np.isnan(cluster_H0)], [.05])
# good cluster inds
good_cluster_inds = np.where(np.abs(cluster_stats) > clust_threshold)[0]
# then plot good clusters
if len(good_cluster_inds):
    for n,idx in enumerate(np.nditer(good_cluster_inds)):
        temp_data = np.zeros((SOMA_all_stc_diff.data.shape[0],1))
        #temp_data[clusters[idx],n] = SOMA_all_stc_diff.data[clusters[idx],0]
        temp_data[clusters[idx],0] = SOMA_all_stc_diff.data[clusters[idx],0]
        temp_data[np.abs(temp_data)>0] = 1
        stc_clu = SOMA_all_stc_diff.copy()
        stc_clu.data = temp_data
        stc_clu.plot(subjects_dir=mri_dir,subject='fsaverage',surface='white',hemi='both',time_viewer=True,colormap='coolwarm',clim={'kind':'value','pos_lims':(0,0.5,1)})
        # plot and save figs on inflated brain with annotation
        fig = mlab.figure(size=(300, 300))
        brain = stc_clu.plot(subjects_dir=mri_dir,subject='fsaverage',surface='inflated',hemi='both',colormap='coolwarm',clim={'kind':'value','pos_lims': (0,0.5,1)},figure=fig)
        brain.add_annotation('HCPMMP1_combined', borders=1, alpha=0.9)
        mlab.view(0, 90, 450, [0, 0, 0])
        mlab.savefig('{d}_corr_clu_{n}_rh.png'.format(d=save_dir,n=n), magnification=4)
        mlab.view(180, 90, 450, [0, 0, 0])
        mlab.savefig('{d}_corr_clu_{n}_lh.png'.format(d=save_dir,n=n), magnification=4)
        mlab.view(180, 0, 450, [0, 10, 0])
        mlab.savefig('{d}_corr_clu_{n}_top.png'.format(d=save_dir,n=n), magnification=4)
        mlab.view(180, 180, 480, [0, 10, 0])
        mlab.savefig('{d}_corr_clu_{n}_bottom.png'.format(d=save_dir,n=n), magnification=4)
        mlab.close(fig)
    else: print("No sign. clusters found")
