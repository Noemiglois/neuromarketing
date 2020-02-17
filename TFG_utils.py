#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from scipy import signal


# Se saca el nombre del fichero vmrk
def take_vmrk_filename(Eeg_path):
    for file in os.listdir(Eeg_path):
        if file.split(".")[1]== "vmrk":
            vmrk_filename = os.path.join(Eeg_path, file)
    return vmrk_filename

# Se saca el nombre del fichero vhdr
def take_vhdr_filename(Eeg_path):
    for file in os.listdir(Eeg_path):
        if file.split(".")[1]== "vhdr":
            vhdr_filename = os.path.join(Eeg_path, file)
    return vhdr_filename

# Se busca el inicio de los anuncios en el registro de EEG
def Get_Start_End(File):

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
def spot_samples(start_end, freq, spot_secs):
	spot_samples = []
	for i in spot_secs:
		sample = int(i)*int(freq) + int(start_end[0])
		spot_samples.append(sample)
	return spot_samples

#POTENCIA BANDAS
def get_potencias(num_ventanas,f_eeg,m,L,fs):
    pot_bandas_alpha = []
    pot_bandas_beta = []
    pot_bandas_gamma = []
    pot_ventanas = []
    for i in range(num_ventanas+1):
        f,Px=signal.periodogram(f_eeg[m*i:L+m*i], fs)
        pot_ventanas.append(sum(Px))

        #BANDA ALPHA
        idx_alpha = []
        for i in f:
            if i>=8 and i<14:
                idx_alpha.append(True)
            else:
                idx_alpha.append(False)
        alpha = sum(Px[idx_alpha])
        pot_bandas_alpha.append(alpha)

        #BANDA BETA
        idx_beta = []
        for i in f:
            if i>=14 and i<30:
                idx_beta.append(True)
            else:
                idx_beta.append(False)
        beta = sum(Px[idx_beta])
        pot_bandas_beta.append(beta)
        
        #BANDA BETA
        idx_gamma = []
        for i in f:
            if i>=30:
                idx_gamma.append(True)
            else:
                idx_gamma.append(False)
        gamma = sum(Px[idx_gamma])
        pot_bandas_gamma.append(gamma)
        
    return pot_bandas_alpha,pot_bandas_beta, pot_bandas_gamma, pot_ventanas

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
