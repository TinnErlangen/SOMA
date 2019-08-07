import mne
import numpy as np
import os

# Convert from BTI format to MNE-Python and do filtering and resampling

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
raw_dir = base_dir+"raw/"
proc_dir = base_dir+"proc/"

#l_freq=None
#h_freq=None
notches = [50, 100, 150, 200]

subjs = ["SOM_12","SOM_13","SOM_15","SOM_17","SOM_18","SOM_19","SOM_20","SOM_21","SOM_22","SOM_23","SOM_24","SOM_26","SOM_27","SOM_28","SOM_29","SOM_30","SOM_31","SOM_32","SOM_33","SOM_34","SOM_35","SOM_36"]
#subjs=["SOM_20"]
##14 (16 sehr müde) (28 keine Trigger) bei 25 passt was in run3 nicht, 12 in run 2 und 4 steckt Block 2&3
runs = [str(x+1) for x in range(3)]
runs = [str(x+3) for x in range(1)] #nur run 3
runs = str(2)

# create processing folder for each subject
#for sub in subjs:
#    os.chdir(proc_dir)
#    os.mkdir(sub)

for sub in subjs:
    for run_idx,run in enumerate(runs):
        workdir = raw_dir+"nc_"+sub+"/Tinn1.0/Data/"+run+"/"
        rawmeg = mne.io.read_raw_bti(workdir+"c,rfhp1.0Hz",preload=True,
                                     rename_channels=False)
        rawmeg_trigs = mne.find_events(rawmeg,stim_channel="TRIGGER",initial_event=True,consecutive=True)
        for i_idx in range(len(rawmeg_trigs)):
            if rawmeg_trigs[i_idx,2]>1000:
                rawmeg_trigs[i_idx,2]=rawmeg_trigs[i_idx,2]-4095
        rawmeg.notch_filter(notches,n_jobs="cuda")
        #rawmeg,rawmeg_trigs = rawmeg.resample(256,events=rawmeg_trigs,n_jobs="cuda")
        np.save(proc_dir+sub+"_"+run+"_events.npy",rawmeg_trigs)
        rawmeg.save("{dir}{sub}_{run}-raw.fif".format(dir=proc_dir,sub=sub,
                                                         run=run),
                                                         overwrite=True)
