import os
import mne
from mne.preprocessing import (ICA, create_eog_epochs, create_ecg_epochs)
sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)
raw.crop(tmax=60.)
#%% pick some channels that clearly show heartbeats and blinks
regexp = r'(MEG [12][45][123]1|EEG 00.)'
artifact_picks = mne.pick_channels_regexp(raw.ch_names, regexp=regexp)
raw.plot(order=artifact_picks, n_channels=len(artifact_picks))
#%%
eog_evoked = create_eog_epochs(raw).average()
eog_evoked.apply_baseline(baseline=(None, -0.2))
eog_evoked.plot_joint()
#%%
ecg_evoked = create_ecg_epochs(raw).average()
ecg_evoked.apply_baseline(baseline=(None, -0.2))
ecg_evoked.plot_joint()
#%%
filt_raw = raw.copy()
filt_raw.load_data().filter(l_freq=1., h_freq=None)
#%%
ica = ICA(n_components=15, random_state=97)
ica.fit(filt_raw)
#%%
raw.load_data()
ica.plot_sources(raw)
#%%
ica.plot_components()
#%%
# blinks
ica.plot_overlay(raw, exclude=[0], picks='eeg')
# heartbeats
ica.plot_overlay(raw, exclude=[1], picks='mag')
#%%
ica.plot_properties(raw, picks=[0, 1])
#%%
import matplotlib.pyplot as plt

line, = plt.plot([1, 2, 3], label='Inline label')
plt.legend()

#%%PARÉNTESIS
raw = read_raw_brainvision(vhdr_files[0])
print(raw.info)
#raw.crop(tmax=60.)
raw.ch_names
#raw.plot()

data, times = raw[:,:]
print(data.shape)

start, stop = raw.time_as_index([10, 90])  # 100 s to 115 s data segment
data, times = raw[:, start:stop]
#print(data.shape)
#print(times.shape)
#print(times.min(), times.max())
picks = mne.pick_types(raw.info, eeg=True, exclude=[])
#print(picks)
data, times = raw[picks[:10],start:stop]
#print(data.shape)
#print(times.shape)
#print(times.min(), times.max())
raw.plot(scalings={"eeg": 75e-4})
#CERRAMOS PARÉNTESIS

#%% MORE FILTERS 
    # Baseline filter
    raw_filtered= signal.detrend(raw_filtered,axis=-1,type='linear')

    # Notch filter
    f0 = 50  # Frequency to be removed from signal (Hz)
    Q_n = 30  # Quality factor
    b, a = signal.iirnotch(f0, Q_n, sampling_freq) # Design notch filter
    raw_filtered = signal.filtfilt(b, a, raw_filtered) # Apply notch filter
    
    # Band Pass filter
    f1,f2 = (0.5,40) # Band pass frequencies
    numtaps= 70
    b = signal.firwin(numtaps, [f1,f2], pass_zero=False ,fs=sampling_freq) # Get coefficients
    raw_filtered = signal.filtfilt(b, 1, raw_filtered)
    
    #
for cutoff in (0.1, 0.2):
    raw_highpass = raw.copy().filter(l_freq=cutoff, h_freq=None)
    fig = raw_highpass.plot(duration=60, order=mag_channels, proj=False,
                            n_channels=len(mag_channels), remove_dc=False)
    fig.subplots_adjust(top=0.9)
    fig.suptitle('High-pass filtered at {} Hz'.format(cutoff), size='xx-large',
                 weight='bold')