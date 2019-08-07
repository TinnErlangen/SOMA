import mne
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import scipy.io as sio

plt.ion()

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"proc/"
save_dir = base_dir+"for fieldtrip/" # directory where files for matlab are saved
subjs=["SOM_20"]
runs = ["2"]

for sub in subjs:
    for run in runs:
        epo = mne.read_epochs(proc_dir+sub+"_"+run+"_prepro-epo.fif") # path to preprocessed file you want to read in in fieldtrip
        # Data
        datamatrix=epo.get_data()
        scipy.io.savemat(save_dir+'dataMNE.mat', mdict={'dataMNE': datamatrix})

        #Bad segments, info for fieldtrip
        dic1={}
        badsegs=[]
        c=0
        for inx,d in enumerate(epo.drop_log):
            if d == ['USER']:
                badsegs.insert(c,str(inx+1))
                c=c+1
        dic1={'segsMNE': badsegs}
        scipy.io.savemat(save_dir+'segsMNE.mat', dic1)

        # Bad channels , info for fieldtrip
        dic2={}
        if epo.info["bads"]:
            dic2={'channsMNE': epo.info["bads"]}
        scipy.io.savemat(save_dir+'channsMNE.mat', dic2)
