#!/usr/bin/python3
# Purpose:	
# Usage:	
# Author:	Timmy93
# Date:		
# Version:	
# Disclaimer:	

from M3uParser import M3uParser
import configparser
import subprocess

#Rename all the file in this directory
def renameAll(path):
	#TODO
	#Read all file in path
	#For each file check if it has a name
	#Rename with its name
	print("Not implemented - rename all")

def startDownload(downloader, url, temp, completed):
	#TODO
	#Start the download of a certain file using an sh script
	res = subprocess.run([downloader, url, temp, completed], stdout=subprocess.PIPE)
	print("Result: "+str(res.returncode))

def debugTypes(myFile):
	old = ""
	for file in myFile.getList():
		now = file["tvg-group"]
		if old != now:
			print(now)
			old = now
	
def main():
	iniFile = "info.ini"
	iniSample = "[Settings]\nurl=http://your/url/here\nfilename=IPTV.m3u"
	#Read ini file
	try:
		config = configparser.ConfigParser()
		config.read(iniFile)
	except:
		print("Created ini file - Update it!")
		file = open(iniFile,"w") 
		file.write(iniSample) 
		file.close()
		config = configparser.ConfigParser()
		config.read(iniFile)
	#Info for m3u file
	url = config['Settings']['url']
	filename = config['Settings']['filename']
	#Info for renaming
	temp_path = config['Download']['temp_path']
	completed = config['Download']['completed']
	downloader = config['Download']['downloader']
	#Info for download
	source_to_rename = config['Rename']['source_to_rename']
	new_dir = config['Rename']['new_dir']

	#Start parser
	myFile = M3uParser()
	myFile.downloadM3u(url, filename)
	#Set filters
	myFile.filterOutFilesEndingWith(".ts")
	myFile.filterOutFilesOfGroupsContaining("Film Sala")
	myFile.filterOutFilesOfGroupsContaining("Film Ultimi Inseriti Cam")
	myFile.filterOutFilesOfGroupsContaining("3D")
	
	random = myFile.getRandomFile()
	#Debug
	# ~ debugTypes(myFile)
	
	#TODO
	# ~ renameAll(path)
	startDownload(downloader, random["link"], temp_path, completed)
	
	# ~ print(myFile.getCustomTitle("15373.mkv"))
	
main()
