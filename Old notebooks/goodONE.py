# MODULES
from mne.io import read_raw_brainvision
from TFG_utils import (returnFolders, returnFiles, take_vmrk_files, take_vhdr_files, take_eeg_files, plot_eeg_time, plot_PSD)
import matplotlib.pyplot as plt
from mne.preprocessing import ICA
import mne
# COLLECTING DATA
foldername = 'EEG_folders'
EEG_folders=returnFolders(foldername)
EEG_files=returnFiles(EEG_folders)
vmrk_files=take_vmrk_files(EEG_files)
vhdr_files=take_vhdr_files(EEG_files)
eeg_files=take_eeg_files(EEG_files)

# READING and PREPROCESSING DATA
icas=[]
raws=[]
raws_filtered=[]
spots_times_sec = [0, 60, 120, 180, 226, 287, 347] # Time (sec) at which each spot begins

#for i in range(len(EEG_folders)):
for i in range(1):
    raw = read_raw_brainvision(vhdr_files[i]).load_data()

    # FILTERING
    raw_filtered=raw.copy()
    raw_filtered.set_montage("standard_1020") # No estoy segura de que sea este montaje¿?
    sampling_freq = int(raw.info['sfreq'])
    
    #Removing slow drifts (high pass filter (1 Hz))
    raw_filtered.filter(l_freq=1., h_freq=None)

    #Band Pass filter
    raw_filtered.filter(l_freq=0.5, h_freq=40,method='fir', fir_window='hann', fir_design='firwin')

    #Notch filter
    iir_params = dict(order=4, ftype='butter', output='sos')
    iir_params = mne.filter.construct_iir_filter(iir_params, 40, None, 1000, 'low', return_copy=False)  
    raw_filtered.notch_filter(50,method='iir', fir_window='hann', fir_design='firwin', iir_params=iir_params)
    mne.viz.plot_filter(iir_params, 500)

    raws.append(raw)
    raws_filtered.append(raw_filtered) 

    #plot SPOTS
    #plot_eeg_time(raw,raw_filtered,i,vmrk_files)
    
    #plot RAW
    #raw.plot(scalings={"eeg": 75e-4},title='Raw EEG signal') #color='tab:orange'
    #raw_filtered.plot(scalings={"eeg": 75e-4},title='Filtered EEG signal') #color= 'tab:blue'
    
    #plot PSD
    plot_PSD(raw,raw_filtered, filter_applied='Notch filtered EEG signal')
# ICA
#for raw_filtered in raws_filtered:
    #ica = ICA(n_components=None, method='infomax', fit_params=dict(extended=True), random_state=1)
    #ica.fit(raw_filtered)   
    #ica.plot_sources(raw_filtered,title='Raw EEG signal')
    #ica.plot_components(inst=raw_filtered)
