#[190,192,4286,4288];%Trigger von Tönen in Anspannungsbedingung
#{'ton_r1': 190,'ton_r2': 191, 'ton_s1': 192, 'ton_s2': 193}
#[196,198,4290,4292];%Trigger von Tönen in Entspannungsbedingung
#{'ton_r1': 195,'ton_r2': 196, 'ton_s1': 197, 'ton_s2': 198}
#jeder Ton ist 30 sec lang und wird pro Bedingung 2 mal gespielt
import mne
import numpy as np
from mne.io import concatenate_raws, read_raw_edf

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"proc/"

subjs= ["SOM_12"]
#12 in run 2 und 4 steckt Block 2&3

runs = str(2)
runs = ["2","3"]
run_special = str(2)

event_id = {'ton_r1_tension': 190,'ton_r2_tension': 191, 'ton_s1_tension': 192, 'ton_s2_tension': 193,'ton_r1_relax': 195,'ton_r2_relax': 196, 'ton_s1_relax': 197, 'ton_s2_relax': 198}

mini_epochs_num = 15
mini_epochs_len = 2
sub="SOM_12"

raw1 = mne.io.Raw(proc_dir+sub+'_'+'2'+'-raw.fif',preload=True)
raw2 = mne.io.Raw(proc_dir+sub+'_'+'3'+'-raw.fif',preload=True)
raw_files=[raw1,raw2]
raw = concatenate_raws(raw_files)
events1 = list(np.load(proc_dir+sub+'_'+'2'+'_events.npy'))
events1a = events1[0:7] # hier nur die ersten 8 nehmen, weil danach die Töne kommen
events2 = list(np.load(proc_dir+sub+'_'+'3'+'_events.npy'))
events = events1a
events.extend(events2)
new_events = []

for e in events:
    for me in range(mini_epochs_num):
        new_events.append(np.array(
        [e[0]+me*round(mini_epochs_len*raw.info["sfreq"]), 0, e[2]]))
new_events = np.array(new_events).astype(int)
#        print(len(new_events))
#        print(np.unique(new_events[:,2]))
epochs = mne.Epochs(raw,new_events,event_id=event_id,baseline=None,tmin=0,tmax=mini_epochs_len,preload=True)
epochs.save(proc_dir+sub+'_'+run_special+'-epo.fif')
