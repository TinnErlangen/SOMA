import mne
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import scipy.io as sio

plt.ion()

subjs = ["SOM_10","SOM_12","SOM_13","SOM_15","SOM_16","SOM_17","SOM_19","SOM_22","SOM_23","SOM_24","SOM_26","SOM_27","SOM_29","SOM_30","SOM_31","SOM_32","SOM_33","SOM_34","SOM_35","SOM_36"]
runs = ["2"]

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"ana/"

for sub in subjs:
    for run in runs:
        save_dir = base_dir+"data mne/"+"nc_"+sub+"/"
        epo = mne.read_epochs(proc_dir+sub+"_"+run+"_prepro_ica_final-epo.fif")
        # Data
        datamatrix=epo.get_data()
        scipy.io.savemat(save_dir+'dataMNE.mat', mdict={'dataMNE': datamatrix})

        #Bad segments
        dic1={}
        badsegs=[]
        c=0
        for inx,d in enumerate(epo.drop_log):
            if d == ['USER']:
                badsegs.insert(c,str(inx+1))
                c=c+1
        dic1={'segsMNE': badsegs}
        scipy.io.savemat(save_dir+'segsMNE.mat', dic1)

        # Bad channels
        dic2={}
        if epo.info["bads"]:
            dic2={'channsMNE': epo.info["bads"]}
        scipy.io.savemat(save_dir+'channsMNE.mat', dic2)
