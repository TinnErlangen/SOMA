#[190,192,4286,4288];%Trigger von Tönen in Anspannungsbedingung
#{'ton_r1': 190,'ton_r2': 191, 'ton_s1': 192, 'ton_s2': 193}
#[196,198,4290,4292];%Trigger von Tönen in Entspannungsbedingung
#{'ton_r1': 195,'ton_r2': 196, 'ton_s1': 197, 'ton_s2': 198}
#jeder Ton ist 30 sec lang und wird pro Bedingung 2 mal gespielt
import mne
import numpy as np

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"proc/"

#subjs=["SOM_13","SOM_15","SOM_17"]
subjs = ["SOM_12","SOM_13","SOM_15","SOM_17","SOM_18","SOM_19","SOM_20","SOM_21","SOM_22","SOM_23","SOM_24","SOM_26","SOM_27","SOM_28","SOM_29","SOM_30","SOM_31","SOM_32","SOM_33","SOM_34","SOM_35","SOM_36"]
#subjs = ["SOM_18","SOM_19","SOM_20","SOM_21","SOM_22","SOM_23","SOM_24","SOM_25","SOM_26","SOM_27"]
subjs = ["SOM_10","SOM_16"]

runs = str(2)

event_id = {'ton_r1_tension': 190,'ton_r2_tension': 191, 'ton_s1_tension': 192, 'ton_s2_tension': 193,'ton_r1_relax': 195,'ton_r2_relax': 196, 'ton_s1_relax': 197, 'ton_s2_relax': 198}

mini_epochs_num = 15
mini_epochs_len = 2

for sub in subjs:
    for run in runs:
        raw = mne.io.Raw(proc_dir+sub+'_'+run+'-raw.fif')
        events = list(np.load(proc_dir+sub+'_'+run+'_events.npy'))
        new_events = []
        for e in events:
            for me in range(mini_epochs_num):
                new_events.append(np.array(
                [e[0]+me*round(mini_epochs_len*raw.info["sfreq"]), 0, e[2]]))
        new_events = np.array(new_events).astype(int)
        epochs = mne.Epochs(raw,new_events,event_id=event_id,baseline=None,tmin=0,tmax=2,preload=True)
        epochs.save(proc_dir+sub+'_'+run+'-epo.fif')
