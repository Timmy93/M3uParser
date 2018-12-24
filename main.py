#!/usr/bin/python3
# Purpose:	
# Usage:	
# Author:	Timmy93
# Date:		
# Version:	
# Disclaimer:	

from M3uParser import M3uParser
import configparser

def renameAll(path):
	#TODO
	#Read all file in path
	#For each file check if it has a name
	#Rename with its name
	print("Not implemented")
	
def debugNoStreamingNoCam(mioFile):
	old = ""
	for file in mioFile.getNoCamNoStreaming():
		now = file["tvg-group"]
		if old != now:
			print(now)
			old = now
	
def main():
	iniFile = "info.ini"
	
	#Read ini file
	config = configparser.ConfigParser()
	config.read(iniFile)
	url = config['Settings']['url']
	filename = config['Settings']['filename']
	
	#Start parser
	mioFile = M3uParser()
	mioFile.downloadM3u(url, filename)
	
	#Debug
	debugNoStreamingNoCam(mioFile)
	
	# ~ print(mioFile.files)

main()
