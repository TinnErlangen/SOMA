import mne
import numpy as np

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"proc/"

subjs = ["SOM_12","SOM_13","SOM_15","SOM_17"]
subjs = ["SOM_18","SOM_19","SOM_20","SOM_21","SOM_22","SOM_23","SOM_24","SOM_25","SOM_26","SOM_27","SOM_28"]
subjs = ["SOM_29","SOM_30","SOM_31","SOM_32","SOM_33","SOM_34","SOM_35","SOM_36"]
subjs = ["SOM_14"]
##(16 sehr müde) (28 keine Trigger)
runs = str(1)

event_id = {'rest': 220}

mini_epochs_num = 90
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
        #check if events alright
        print(new_events[:25,:])
        print(len(new_events))
        print(np.unique(new_events[:,2]))

        epochs = mne.Epochs(raw,new_events,event_id=event_id,baseline=None,tmin=0,tmax=mini_epochs_len,preload=True)
        #check epochs and labels
        print(epochs.event_id)
        print(epochs.events[:12])
        print(epochs[1:3])
        print(epochs['rest'])
        epochs.save(proc_dir+sub+'_'+run+'-epo.fif')

        #look at them
        #epochs.plot(n_epochs=8,n_channels=10)
        #epochs.plot_psd(fmax=50)
        #epochs.plot_psd_topomap()
