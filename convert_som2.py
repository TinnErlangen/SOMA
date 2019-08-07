import mne
import numpy as np
import os
#from mne.io import concatenate_raws, read_raw_edf
from mne.io import concatenate_raws

# für VPs mit 4 runs
# Convert from BTI format to MNE-Python and do filtering and resampling

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
raw_dir = base_dir+"raw/"
proc_dir = base_dir+"proc/"

#l_freq=None
#h_freq=None
notches = [50, 100, 150, 200]

subjs=["SOM_10","SOM_16"]
runs=str(2)
##run 2 und 3 entsprechen run 2 bei anderen

for sub in subjs:
    for run_idx,run in enumerate(runs):
        #workdir = raw_dir+"nc_"+sub+"/Tinn1.0/Data/"+"4"+"/"
        workdir1 = raw_dir+"nc_"+sub+"/Tinn1.0/Data/"+"2"+"/"
        workdir2 = raw_dir+"nc_"+sub+"/Tinn1.0/Data/"+"3"+"/"
        #rawmeg = mne.io.read_raw_bti(workdir+"c,rfhp1.0Hz",preload=True,rename_channels=False)
        raw1 = mne.io.read_raw_bti(workdir1+"c,rfhp1.0Hz",preload=True,rename_channels=False)
        raw2 = mne.io.read_raw_bti(workdir2+"c,rfhp1.0Hz",preload=True,rename_channels=False)
        raw_files=[raw1,raw2]
        raw = concatenate_raws(raw_files)
        rawmeg=raw
        rawmeg_trigs = mne.find_events(rawmeg,stim_channel="TRIGGER",initial_event=True,consecutive=True)
        for i_idx in range(len(rawmeg_trigs)):
            if rawmeg_trigs[i_idx,2]>1000:
                rawmeg_trigs[i_idx,2]=rawmeg_trigs[i_idx,2]-4095
        rawmeg.notch_filter(notches,n_jobs="cuda")
        #rawmeg,rawmeg_trigs = rawmeg.resample(200,events=rawmeg_trigs,n_jobs="cuda")
        np.save(proc_dir+sub+"_"+run+"_events.npy",rawmeg_trigs)
        rawmeg.save("{dir}{sub}_{run}-raw.fif".format(dir=proc_dir,sub=sub,
                                                         run=run),
                                                         overwrite=True)
