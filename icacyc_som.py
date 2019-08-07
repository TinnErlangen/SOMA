import mne
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"proc/"

subjs = ["SOM_12","SOM_13","SOM_15","SOM_17","SOM_18","SOM_19","SOM_20","SOM_21","SOM_22","SOM_23","SOM_24","SOM_26","SOM_27","SOM_29","SOM_30","SOM_31","SOM_32","SOM_33","SOM_34","SOM_35","SOM_36"]
subjs = ["SOM_10","SOM_16"]
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

#def go(self,idx=0):
    def go(self):
        plt.close('all')
        # load the next raw/ICA files
        self.fn = self.filelist.pop()
        self.epo = mne.read_epochs(self.fn[0],preload=True)
        self.ica = mne.preprocessing.read_ica(self.fn[3])
        self.ica_ref = mne.preprocessing.read_ica(self.fn[1])

        # housekeeping on reference components, add them to raw data
        #refcomps = self.icaref.get_sources(self.epo)
        #for c in refcomps.ch_names[:self.ref_comp_num]: # they need to have REF_ prefix to be recognised by MNE algorithm
        #    refcomps.rename_channels({c:"REF_"+c})
        #self.epo.add_channels([refcomps])

        self.comps = []

        # plot everything out for overview
        self.ica.plot_components(picks=list(range(20)))
        self.ica.plot_sources(self.epo)

        #Fenster um ICA Komponenten auszuwählen kann immer mit cyc.ica.plot_sources(cyc.epo) zurückgeholt werden

    def plot_props(self,props=None):
        # in case you want to take a closer look at a component
        if not props:
            props = self.comps
        self.ica.plot_properties(self.epo,props)

    def show_file(self):
        print("Current raw file: "+self.fn[0])

    def without(self,comps=None,fmax=40):
        # see what the data would look like if we took comps out
        self.comps +=self.ica.exclude
        if not comps:
            comps = self.comps
        test = self.epo.copy()
        test.load_data()
        test = self.ica.apply(test,exclude=comps)
        test.plot_psd(fmax=fmax)
        test.plot(n_epochs=12,n_channels=30,scalings=dict(mag=2e-12))
        self.test = test

    def identify_bad(self,method,threshold=4):
        # search for components which correlate with noise
        # example: method= ["ecg","ref"]
        if isinstance(method,str):
            method = [method]
        elif not isinstance(method,list):
            raise ValueError('"method" must be string or list.')
        for meth in method:
            print(meth)
            if meth == "eog":
                func = self.ica.find_bads_eog
            elif meth == "ecg":
                func = self.ica.find_bads_ecg
            elif meth == "ref":
                func = self.ica.find_bads_ref
            else:
                raise ValueError("Unrecognised method.")
            inds, scores = func(self.epo)
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
