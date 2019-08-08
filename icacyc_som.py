import mne
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"proc/"

subjs = ["SOM_10","SOM_12","SOM_13","SOM_15","SOM_16","SOM_17","SOM_18","SOM_19","SOM_20","SOM_21","SOM_22","SOM_23","SOM_24","SOM_26","SOM_27","SOM_29","SOM_30","SOM_31","SOM_32","SOM_33","SOM_34","SOM_35","SOM_36"]
runs = ["2"]

filelist = []
for sub in subjs:
    for run in runs:
        filelist.append(["{dir}{sub}_{run}_prepro-epo.fif".format(dir=proc_dir,sub=sub,run=run),
        "{dir}{sub}_{run}_prepro_ref-ica.fif".format(dir=proc_dir,sub=sub,run=run),
        "{dir}{sub}_{run}_prepro_meg-ica.fif".format(dir=proc_dir,sub=sub,run=run),
        "{dir}{sub}_{run}_prepro-ica.fif".format(dir=proc_dir,sub=sub,run=run)])

ref_comp_num=6

class Cycler():

    def __init__(self,filelist,ref_comp_num):
        self.filelist = filelist
        self.ref_comp_num = ref_comp_num

    def go(self,idx=0):
        plt.close('all')
        # load the next raw/ICA files
        self.fn = self.filelist.pop(idx)
        self.epo = mne.read_epochs(self.fn[0],preload=True)
        self.ica = mne.preprocessing.read_ica(self.fn[3])
        self.icaref = mne.preprocessing.read_ica(self.fn[1])
        self.icameg = mne.preprocessing.read_ica(self.fn[2])

        # housekeeping on reference components, add them to raw data
        refcomps = self.icaref.get_sources(self.epo)
        for c in refcomps.ch_names[:self.ref_comp_num]: # they need to have REF_ prefix to be recognised by MNE algorithm
            refcomps.rename_channels({c:"REF_"+c})
        self.epo.add_channels([refcomps])

        self.comps = []

        # plot everything out for overview
        self.ica.plot_components(picks=list(range(40)))
        self.ica.plot_sources(self.epo, stop=8)
        self.epo.plot(n_channels=64,n_epochs=8,scalings=dict(mag=2e-12,ref_meg=3e-12,misc=10))
        self.epo.plot_psd(fmax=60,average=False,bandwidth=0.8)

        #Fenster um ICA Komponenten auszuwählen kann immer mit cyc.ica.plot_sources(cyc.epo) zurückgeholt werden

    def plot_props(self,props=None):
        # in case you want to take a closer look at a component
        if not props:
            props = self.comps
        self.ica.plot_properties(self.epo,props)

    def show_file(self):
        print("Current raw file: "+self.fn[0])

    def without(self,comps=None,fmax=60):
        # see what the data would look like if we took comps out
        self.comps +=self.ica.exclude
        if not comps:
            comps = self.comps
        test = self.epo.copy()
        test.load_data()
        test = self.ica.apply(test,exclude=comps)
        test.plot_psd(fmax=fmax,average=False,bandwidth=0.8)
        test.plot(n_epochs=8,n_channels=64,scalings=dict(mag=2e-12,ref_meg=3e-12,misc=10))
        self.test = test

    def identify_bad(self,method,threshold=0.5):
        # search for components which correlate with noise
        # example: method= ["ecg","ref"]
        if isinstance(method,str):
            method = [method]
        elif not isinstance(method,list):
            raise ValueError('"method" must be string or list.')
        for meth in method:
            print(meth)
            if meth == "eog":
                inds, scores = self.ica.find_bads_eog(self.epo)
            elif meth == "ecg":
                inds, scores = self.ica.find_bads_ecg(self.epo)
            elif meth == "ref":
                inds, scores = self.ica.find_bads_ref(self.epo, method="separate",
                                                      threshold=threshold,
                                                      bad_measure="cor")
            else:
                raise ValueError("Unrecognised method.")
            print(inds)
            if inds:
                self.ica.plot_scores(scores, exclude=inds)
                self.comps += inds

    def save(self,comps=None):
        # save the new file
        self.comps +=self.ica.exclude
        if not comps:
            self.ica.apply(self.epo,exclude=self.comps).save(self.fn[0][:-8]+"_ica-epo.fif")
        elif isinstance(comps,list):
            self.ica.apply(self.epo,exclude=self.comps+comps).save(self.fn[0][:-8]+"_ica-epo.fif")
        else:
            print("No components applied, saving anyway for consistency.")
            self.epo.save(self.fn[0][:-8]+"_ica-epo.fif")


cyc = Cycler(filelist,ref_comp_num)
