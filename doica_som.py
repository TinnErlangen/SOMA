import mne

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"proc/"

subjs = ["SOM_20"]
#runs = ["1","2","3"]
runs = ["2"]

for sub in subjs:
    for run in runs:
        mepo = mne.read_epochs(proc_dir+sub+"_"+run+"_m-epo.fif")
        ica = mne.preprocessing.ICA(n_components=0.95,max_iter=500,method="picard")
        ica.fit(mepo)
        ica.save(proc_dir+sub+"_"+run+"_prepro-ica.fif")
