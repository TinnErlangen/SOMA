import mne
import numpy as np

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"proc/"

subjs = ["SOM_10","SOM_12","SOM_13","SOM_15","SOM_16","SOM_17","SOM_18","SOM_19","SOM_20","SOM_21","SOM_22","SOM_23","SOM_24","SOM_26","SOM_27","SOM_29","SOM_30","SOM_31","SOM_32","SOM_33","SOM_34","SOM_35","SOM_36"]
runs = ["2"]

for sub in subjs:
    for run_idx,run in enumerate(runs):
        raw = mne.read_epochs(proc_dir+sub+"_"+run+"_prepro-epo.fif")

        icaref = mne.preprocessing.ICA(n_components=6,max_iter=10000,method="picard",allow_ref_meg=True)
        picks = mne.pick_types(raw.info,meg=False,ref_meg=True)
        icaref.fit(raw,picks=picks)
        icaref.save(proc_dir+sub+"_"+run+"_prepro_ref-ica.fif")

        icameg = mne.preprocessing.ICA(n_components=100,max_iter=10000,method="picard")
        picks = mne.pick_types(raw.info,meg=True,ref_meg=False)
        icameg.fit(raw,picks=picks)
        icameg.save(proc_dir+sub+"_"+run+"_prepro_meg-ica.fif")

        ica = mne.preprocessing.ICA(n_components=100,max_iter=10000,method="picard",allow_ref_meg=True)
        picks = mne.pick_types(raw.info,meg=True,ref_meg=True)
        ica.fit(raw,picks=picks)
        ica.save(proc_dir+sub+"_"+run+"_prepro-ica.fif")
