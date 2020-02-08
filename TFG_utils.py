#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def Load_Eeg_Info(Eeg_Info):
	Info_File = open('Data_Info_Eeg','w')
	Info_File.write(str(Eeg_Info))
	Info_File.close()

	return 'Data_Info_Eeg'

def Get_Frequency(Info_File):
	Info_File = open('Data_Info_Eeg', 'r')
	Info = Info_File.read()
	Freq_Line = Info.splitlines()[16]
	Freq = Freq_Line.split('|')[1].split(' ')[1].split('.')[0]
	return Freq

def take_vmrk_file(Eeg_path):
	dirs = os.listdir(os.getcwd() + "\\" + Eeg_path)
	dir_len = len(dirs)
	i = 0
	while i < dir_len:
		x = dirs[i].split('.')
		if x[1] == 'vmrk':
			return dirs[i]
		else:
			i += 1

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

def spot_samples(start_end, freq, spot_secs):
	spot_samples = []
	print("before")
	for i in spot_secs:
		sample = int(i)*int(freq) + int(start_end[0])
		spot_samples.append(sample)
	return spot_samples
