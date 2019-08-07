#Tontrigger: 250   254  4346  4348
import mne
import numpy as np

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"proc/"

subjs = ["SOM_12","SOM_13","SOM_15","SOM_17"]
subjs = ["SOM_18","SOM_19","SOM_20","SOM_21","SOM_22","SOM_23","SOM_24","SOM_25","SOM_26","SOM_27","SOM_28"]
subjs = ["SOM_29","SOM_30","SOM_31","SOM_32","SOM_33","SOM_34","SOM_35","SOM_36"]
subjs = ["SOM_14"]
##(16 sehr müde) (28 keine Trigger) bei 25 passt was in run3 nicht
runs = str(3)

event_id = {'ton_r1': 250,'ton_r2': 251, 'ton_s1': 253, 'ton_s2': 254}


for sub in subjs:
    for run in runs:
        raw = mne.io.Raw(proc_dir+sub+'_'+run+'-raw.fif')
        events = np.load(proc_dir+sub+'_'+run+'_events.npy')
        #check if events alright
        print(events[:25,:])
        print(len(events))
        print(np.unique(events[:,2]))

        epochs = mne.Epochs(raw,events,event_id=event_id,baseline=None,preload=True)
        #check epochs and labels
        print(epochs.event_id)
        print(epochs.events[:12])
        print(epochs[1:3])
        print(epochs['ton_s1'])
        epochs.save(proc_dir+sub+'_'+run+'-epo.fif')

        #look at them
        #epochs.plot(n_epochs=8,n_channels=10)
        #epochs.plot_psd(fmax=50)
        #epochs.plot_psd_topomap()
