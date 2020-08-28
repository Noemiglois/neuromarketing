import os
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from mne.preprocessing import ICA
import time
import mne

def returnFiles(folder_name):
    EEG_folders = []
    for folder in os.listdir(folder_name):
        EEG_folders.append(os.path.join(folder_name,folder))
    EEG_files = []
    for folder in EEG_folders:
        folder_files = []
        for file in os.listdir(folder):
            folder_files.append(os.path.join(folder,file))  
        EEG_files.append(folder_files)
    return EEG_files

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def take_vmrk_files(files):
    vmrk_files=[]
    for i in range(len(files)):
        for file in files[i]:
            if file.split(".")[1]== "vmrk":
                vmrk_files.append(file)
    return vmrk_files

def take_vhdr_files(files):
    vhdr_files=[]
    for i in range(len(files)):
        for file in files[i]:
            if file.split(".")[1]== "vhdr":
                vhdr_files.append(file)
    return vhdr_files

def take_eeg_files(files):
    eeg_files=[]
    for i in range(len(files)):
        for file in files[i]:
            if file.split(".")[1]== "eeg":
                eeg_files.append(file)
    return eeg_files

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Se busca el inicio de los anuncios en el registro de EEG
def Get_Start_End_mrk(File):
	Info_File = open(File, 'r')
	Info = Info_File.read()

	Info_Lines = Info.splitlines()
	Total_Lines  = len(Info_Lines)

	Data_Start_End = []

	i = 0
	while i<Total_Lines:
		Line_Data = Info_Lines[i]
		if Line_Data[:3] == 'Mk2' or Line_Data[:3] == 'Mk3':
			Data = Line_Data.split(',')
			start_end = Data[2]
			Data_Start_End.append(start_end)
			i += 1
		else:
			i += 1
	return Data_Start_End

# Se sacan los valores de EEG en cada comienzo de anuncio
def Get_spot_start_samples(start_end, freq, spot_secs):
	spot_samples = []
	for i in spot_secs:
		sample = int(i)*int(freq) + int(start_end[0])
		spot_samples.append(sample)
	return spot_samples

#%%%%%%%%%%%%%%%%%%%%%%%%%%% PLOT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def plot_spots(vmrk_filename,sig,ch):
    fs= sig.info['sfreq']
    y,x= sig[:]
    
    spots_times_sec = [0, 60, 120, 180, 226, 287, 347] # Time at which each spot begins (in sec)
    start_end = Get_Start_End_mrk(vmrk_filename) # Start and end of spots markers
    spot_samples = Get_spot_start_samples(start_end,fs, spots_times_sec) # Start from each spot in the recording
    
    labels=['Basal activity','Spot 1','Spot 2','Spot 3','Spot 4', 'Spot 5','Spot 6']
    ini= int(60)*int(fs) # samples of 1st min of basal activity

    plt.figure(figsize=(12,7))
    it=0
    axx=x[spot_samples[it]-ini:spot_samples[it]]
    axy=y[ch][spot_samples[it]-ini:spot_samples[it]]
    plt.plot(axx, axy, linewidth=1, label=labels[it])

    while it<(len(spot_samples)-1):
        axx=x[spot_samples[it]:spot_samples[it+1]]
        axy=y[ch][spot_samples[it]:spot_samples[it+1]]
        plt.plot(axx, axy, linewidth=1, label=labels[it+1])
        it+=1

    plt.xlabel('Time [sec]')
    plt.ylabel('EEG [µV]')
    plt.legend(loc='best')
    plt.show()

def plot_freq_response(b,a,fs,xlim=150):
    freq, h = signal.freqz(b=b, a=a, fs=fs)
    fig, ax = plt.subplots(2, 1, figsize=(12, 7))
    fig.suptitle('Frequency Response (FOI)', fontsize=16)
    
    ax[0].set_title("Bode magnitude plot")
    ax[0].plot(freq, 20*np.log10(abs(h)), color='blue')
    ax[0].set_ylabel("Amplitude (dB)", color='blue')
    ax[0].set_xlim([0, xlim])
    ax[0].grid()
    
    ax[1].set_title("Bode phase plot")
    ax[1].plot(freq, np.unwrap(np.angle(h))*180/np.pi, color='green')
    ax[1].set_ylabel("Phase (degrees)", color='green')
    ax[1].set_xlabel("Frequency (Hz)")
    ax[1].set_xlim([0, xlim])
    ax[1].grid()
    
    plt.show()

def plot_PSD(raw,raw_filtered,filter_applied):
    plt.figure(figsize=(12,5))
    ax = plt.axes()
    raw.plot_psd(fmax=150,ax=ax, color='tab:blue',area_mode='std', dB=True, show=False, average=True, 
                 estimate='power', line_alpha=None)
    raw_filtered.plot_psd(fmax=150,ax=ax, color= 'tab:orange', area_mode='std', dB=True, show=False, average=True, 
                          estimate='power', line_alpha=None)    
    ax.set_xlim([0, 2])
    ax.set_title('Power Spectral Density (PSD)', fontsize=16)
    leg_lines = [line for line in ax.lines if line.get_linestyle() == '-']
    plt.legend(leg_lines, ['Raw signal',filter_applied])    

def plot_residual_PSD(sig1,sig2):
    plt.figure(figsize=(12,5))
    ax = plt.axes()
    d1,t1=sig1[:]
    d2,t2=sig2[:]
    info=sig1.info
    signal=mne.io.RawArray(d1-d2,info,verbose=False)
    signal.plot_psd(fmax=150, area_mode='std', ax=ax, dB=True, show=False, average=True, estimate='power', line_alpha=None)
    ax.set_xlim([0, 2])
    #ax.set_ylim([-50, 100])
    ax.set_title('Residual PSD', fontsize=16)
    plt.show()
    
def plot_eeg_channel_corrected(ch,sig1,sig2, filter_applied):
    y1,x1=sig1[:]
    y2,x2=sig2[:]

    mysignals = [{'name': 'Raw signal', 'x': x1,
                 'y': y1[ch], 'color':'tab:blue', 'alpha':0.7, 'linewidth':0.3},
                {'name': filter_applied, 'x': x2,
                 'y': y2[ch], 'color':'tab:orange','alpha':0.7, 'linewidth':1}]

    fig, ax = plt.subplots(figsize=(12,5))
    for signal in mysignals:
        ax.plot(signal['x'], signal['y'], 
                color=signal['color'], alpha=signal['alpha'],
                linewidth=signal['linewidth'],
                label=signal['name'])

    # Enable legend
    ax.legend()
    ax.set_ylabel('EEG [µV]')
    ax.set_xlabel('Time [sec]')
    ax.set_title("EEG time signal (Channel %s"%sig1.info['ch_names'][ch]+str(')'),fontsize=16)
    plt.show()
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#POTENCIA BANDAS
def get_potencias(ch,f_eeg,fs):   
    f, Px = signal.periodogram(f_eeg.get_data()[ch], fs) 
    pot_total=sum(Px)
    pot_banda_alpha = []
    idx_alpha = []
    for i in f:
        if i>=8 and i<14:
            idx_alpha.append(True)
        else:
            idx_alpha.append(False)
    pot_banda_alpha.append(sum(Px[idx_alpha]))
    ratio=pot_banda_alpha/pot_total
    return [pot_banda_alpha[0], pot_total, float(ratio)]

def check_index_between(f,f1,f2):
    idx = []
    for i in f:
        if i>f1 and i<=f2:
            idx.append(True)
        else:
            idx.append(False)
    return idx

#RATIOS POR BANDAS DE FRECUENCIAS
def ratios(Pot):
    pot_ventanas = Pot['Pot ventana']
    pot_alpha = Pot['Pot alpha']
    pot_beta = Pot['Pot beta']
    pot_gamma = Pot['Pot gamma']

    ratio_alpha=pot_alpha/(pot_ventanas)
    ratio_beta=pot_beta/(pot_ventanas)
    ratio_gamma=pot_gamma/(pot_ventanas)
    
    return ratio_alpha, ratio_beta, ratio_gamma    
    
def plot_eeg_time(sig1,sig2,i,vmrk_files):
    signals=[sig1,sig2]
    spots_times_sec = [0, 60, 120, 180, 226, 287, 347] # Time (sec) at which each spot begins
    colors=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 
            'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    labels=['Basal activity','spot 1','spot 2','spot 3','spot 4', 'spot 5','spot 6']

    channel_names=sig1.ch_names
    #channel_names=[1]
        
    fig, axs = plt.subplots(2,sharex=True,figsize=(15,7))
    for j in range(2):
        info=signals[j].info
        sampling_freq = int(info['sfreq'])
        start_end = Get_Start_End_mrk(vmrk_files[i])
        spot_start_samples = Get_spot_start_samples(start_end, sampling_freq, spots_times_sec)
        ini= int(60)*int(sampling_freq) # samples of 1st min of basal activity
    
        for ch in range(len(channel_names)):
            it = 0
            axx= np.arange(spot_start_samples[it]-ini,spot_start_samples[it])
            axy,t=signals[j][ch,spot_start_samples[it]-ini:spot_start_samples[it]]
            axs[j].plot(axx/sampling_freq, axy.flatten(), color=colors[it],label=labels[it])
    
            while it<(len(spot_start_samples)-1):
                axx= np.arange(spot_start_samples[it],spot_start_samples[it+1])
                axy,t=signals[j][ch,spot_start_samples[it]:spot_start_samples[it+1]]
                axs[j].plot(axx/sampling_freq, axy.flatten(), color=colors[it+1],label=labels[it+1])
                it+=1
    axs[0].set_title("EEG raw signal",fontweight='bold')
    axs[1].set_title("EEG filtered signal",fontweight='bold')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys(),loc="upper right")
    fig.add_subplot(111, frame_on=False)
    plt.tick_params(labelcolor="none", bottom=False, left=False)
    plt.xlabel("Time [sec]")
    plt.ylabel("EEG [µV]")
    plt.show()
    
##################### Filtering

def filtering_track(track):
    f1,f2=(2,40)
    track_filtered= track.copy().set_montage("standard_1020",verbose= False)
    track_filtered.filter(l_freq=f1, h_freq=f2, filter_length='auto', method='fir',fir_window='hamming', 
                          fir_design='firwin', verbose= False)
    track_filtered.notch_filter([50,100,150], filter_length='auto', method='fir', fir_window='hamming', fir_design='firwin', verbose=None)
    return track_filtered