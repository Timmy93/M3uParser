#!/usr/bin/python3
# Purpose:	
# Usage:	
# Author:	Timmy93
# Date:		
# Version:	
# Disclaimer:	

from M3uParser import M3uParser
from RememberFile import RememberFile
import configparser
import subprocess
import os
import datetime

#Rename all the file in this directory
def rename(src, dst, oldName, newName):
	filename, file_extension = os.path.splitext(oldName)
	os.rename(src+oldName, dst+newName+file_extension)

#Downlad the file in a certain directory - Return True if correctly downloaded
def startDownload(downloader, url, temp, completed):
	#Start the download of a certain file using an sh script
	res = subprocess.run([downloader, url, temp, completed], stdout=subprocess.PIPE)
	return res.returncode == 1

#Get time elapsed between two time
def time_in_range(start, end):
    """Return true if x is in the range [start, end]"""
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    x = datetime.time(int(h), int(m), 0)
    #Set time as datetime
    h,m = start.split(":")
    start = datetime.time(int(h), int(m), 0)
    h,m = end.split(":")
    end = datetime.time(int(h), int(m), 0)
    #Start comparison
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

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
	#Info for download
	temp_path = config['Download']['temp_path']
	completed = config['Download']['completed']
	downloader = config['Download']['downloader']
	db_path = config['Download']['db']
	#Info for renaming
	source_to_rename = config['Rename']['source_to_rename']
	new_dir = config['Rename']['new_dir']
	#Info for time range activity
	start_time = config['Time']['start_time']
	end_time = config['Time']['end_time']

	#Start parser
	myFile = M3uParser()
	myFile.downloadM3u(url, filename)
	#Set filters
	myFile.filterOutFilesEndingWith(".ts")
	myFile.filterOutFilesOfGroupsContaining("Film Sala")
	myFile.filterOutFilesOfGroupsContaining("Film Ultimi Inseriti Cam")
	myFile.filterOutFilesOfGroupsContaining("3D")
	
	
	#Debug
	# ~ debugTypes(myFile)
	
	#TODO
	# ~ renameAll(path)
	# ~ 
	
	db = RememberFile(db_path)
	fileLeft = len(myFile.getList())
	correctTimeRange = time_in_range(start_time, end_time)
	while fileLeft and correctTimeRange:
		#Extract file
		random = myFile.getRandomFile()
		#Check if it is a new file
		if db.isAlreadyDownloaded(random["title"]):
			break
		#Download file
		if startDownload(downloader, random["link"], temp_path, completed):
			#Move renamed file
			rename(source_to_rename, new_dir, random["titleFile"], random["title"])
			#Save that the file has been renamed
			db.appendTitle(random["title"])
	
	if not fileLeft:
		print("Downloaded every file")
	if not correctTimeRange:
		print("It is not time to download")
	# ~ print(myFile.getCustomTitle("15373.mkv"))
	
main()
