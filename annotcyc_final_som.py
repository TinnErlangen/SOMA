import mne
import matplotlib.pyplot as plt

plt.ion()

base_dir ="C:/Users/muellena/Desktop/Desktop/Experiment Somatosensorik/SOMA Daten/"
proc_dir = base_dir+"proc/"
proc_dir2 = base_dir+"ana/"

#subjs = ["SOM_12","SOM_13","SOM_14","SOM_15","SOM_17"]
#subjs = ["SOM","SOM_29","SOM_30","SOM_31","SOM_32","SOM_33","SOM_34","SOM_35","SOM_36"]
#16 sehr müde, 28 keine Trigger, bei 25 passt was in run3 nicht
runs = ["1","2","3"]
subjs = ["SOM_10","SOM_12","SOM_13","SOM_15","SOM_16","SOM_17","SOM_19","SOM_22","SOM_23","SOM_24","SOM_26","SOM_27","SOM_29","SOM_30","SOM_31","SOM_32","SOM_33","SOM_34","SOM_35","SOM_36"]
#subjs=["SOM_10","SOM_16"]
runs = ["2"]

filelist = []
for sub in subjs:
    for run in runs:
        filelist.append('{dir}{sub}_{run}_prepro_ica-epo.fif'.format(dir=proc_dir,sub=sub,run=run))

class Cycler():

    def __init__(self,filelist):
        self.filelist = filelist

    def go(self):
        self.fn = self.filelist.pop()
        self.epo = mne.read_epochs(self.fn)
        self.epo.plot(n_epochs=12,n_channels=75,scalings=dict(mag=2e-12))
        self.epo.plot_psd(average=False)

    def plot(self,n_epochs=12,n_channels=30):
        self.epo.plot(n_epochs=n_epochs,n_channels=n_channels,scalings=dict(mag=2e-12))

    def show_file(self):
        print("Current Epoch File: " + self.fn)

    def save(self):
        self.epo.save(proc_dir2+self.fn[76:-19]+'_final-epo.fif')
        if self.epo.info["bads"]:
            with open(proc_dir2+self.fn[76:-19]+'_badchans.txt', "w") as file:
                for b in self.epo.info["bads"]:
                    file.write(b+"\n")

        #with open(self.fn[:-8]+'_epodrops.txt', "w") as file:
            #for inx,d in enumerate(self.epo.drop_log):
                #if d == ['USER']:
                    #file.write("Epoch No. {inx} Condition {trig}\n".format(inx=inx+1,trig=self.epo.events[inx, 2]))

cyc = Cycler(filelist)
