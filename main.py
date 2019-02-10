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
import logging
import yaml

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

#Check if the given path is an absolute path
def createAbsolutePath(path):
	if not os.path.isabs(path):
		currentDir = os.path.dirname(os.path.realpath(__file__))
		path = os.path.join(currentDir, path)
		
	return path
		
def main():
	configFile = "config.yml"
	logFile = "M3uParser.log"
	#Set logging file
	logging.basicConfig(filename=createAbsolutePath(logFile),level=logging.ERROR,format='%(asctime)s %(levelname)-8s %(message)s')
	#Load config
	with open(createAbsolutePath(configFile), 'r') as stream:
		try:
			config = yaml.load(stream)
			#Info for m3u file
			url = config['Settings']['url']
			filename = config['Settings']['filename']
			logLevel = config['Settings']['logLevel']
			#Info for download
			temp_path = createAbsolutePath(config['Download']['temp_path'])
			completed = createAbsolutePath(config['Download']['completed'])
			downloader = createAbsolutePath(config['Download']['downloader'])
			db_path = createAbsolutePath(config['Download']['db'])
			#Info for renaming
			source_to_rename = createAbsolutePath(config['Rename']['source_to_rename'])
			new_dir = createAbsolutePath(config['Rename']['new_dir'])
			#Info for time range activity
			start_time = config['Time']['start_time']
			end_time = config['Time']['end_time']
			logging.getLogger().setLevel(logLevel)
			logging.info('Loaded settings started')
		except yaml.YAMLError as exc:
			print("Cannot load file: ["+configFile+"] - Error: "+exc)
			logging.error("Cannot load file: ["+configFile+"] - Error: "+exc)
			exit()
	
	#Start parser
	myFile = M3uParser(logging)
	myFile.downloadM3u(url, filename)
	logging.info('Downloaded m3u file')
	#Set filters
	#Remove extensions
	for val in config['ExtensionFilterOut']['value']:
		myFile.filterOutFilesEndingWith(val)
	#Remove groups
	for val in config['GroupFilterOut']['value']:
		myFile.filterOutFilesOfGroupsContaining(val)
	#Select extensions
	myFile.filterInFilesEndingWith(config['ExtensionFilterIn']['value'])
	#Select groups
	myFile.filterInFilesOfGroupsContaining(config['GroupFilterIn']['value'])
	
	#Create DB
	db = RememberFile(db_path)
	logging.info('DB file found')
	
	logging.info("File left after filtering: "+str(len(myFile.getList())))
	while len(myFile.getList()) and time_in_range(start_time, end_time):
		#Extract file
		file = myFile.getFile(config['Download']['shuffle'])

		#Check if it is a new file
		if db.isAlreadyDownloaded(file["title"]):
			logging.debug("Skip file already downloaded: "+file["title"])
			continue
		#Download file
		if startDownload(downloader, file["link"], temp_path, completed):
			try:
				#Move renamed file
				rename(source_to_rename, new_dir, file["titleFile"], file["title"])
				#Save that the file has been renamed
				db.appendTitle(file["title"])
				logging.info("Downloaded: "+file["title"])
			except FileNotFoundError:
				logging.error("Error: No file found, "+file["titleFile"]+" ("+file["titleFile"]+") not found")
		else:
			logging.warning("Problem downloading: "+file["title"]+" - No time to download or no space in the disk")
	
	if not len(myFile.getList()):
		print("Downloaded every file")
		logging.info("STOP: No more file to download")
	elif not time_in_range(start_time, end_time):
		print("It is not time to download")
		logging.info("STOP: Out of download time range")
	else:
		logging.warning("STOP: Unexpected stop")	

main()
