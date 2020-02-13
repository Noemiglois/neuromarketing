#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Se escribe la info del objeto en el fichero Data_Info_Eeg (abrir, escribir, cerrar)
def Load_Eeg_Info(Eeg_Info):
	Info_File = open('Data_Info_Eeg','w')
	Info_File.write(str(Eeg_Info))
	Info_File.close()
	return 'Data_Info_Eeg'

# Se busca la frecuencia de muestreo en el fichero Data_Info_Eeg (abrir, leer,buscar)
def Get_Frequency(Info_File):
	Info_File = open('Data_Info_Eeg', 'r')
	Info = Info_File.read()
	Freq_Line = Info.splitlines()[16]
	Freq = Freq_Line.split('|')[1].split(' ')[1].split('.')[0]
    #¿CERRAR FICHERO?
	return Freq

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
def Get_Start(File):
    
	Info_File = open(File, 'r')
	Info = Info_File.read()

	Info_Lines = Info.splitlines()
	Total_Lines  = len(Info_Lines)
    
	i = 0
	while i<Total_Lines:
		Line_Data = Info_Lines[i]
		if Line_Data[:3] == 'Mk2':
			start = Line_Data.split(',')[2]
			i += 1
		else:
			i += 1
	return start

# Se sacan los valores de EEG en cada comienzo de anuncio
def spot_samples(start, freq, spot_secs):
	spot_samples = []
	for i in spot_secs:
		sample = int(i)*int(freq) + int(start)
		spot_samples.append(sample)
	return spot_samples