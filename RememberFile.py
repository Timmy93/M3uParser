#!/usr/bin/python3
# Purpose:	
# Usage:	
# Author:	Timmy93
# Date:		
# Version:	
# Disclaimer:	

import os

class RememberFile:
	
	def __init__(self, filename):
		#Set filename
		self.filename = filename
		#Create file if not exist
		if not os.path.exists(filename):
			with open(filename, 'w'): pass
		#Load all already downloaded files
		self.files = [line.rstrip('\n') for line in open(filename)]
	
	#Check if the title already exists
	def isAlreadyDownloaded(self, title):
		return title in self.files
	
	#Write the new line in the file
	def appendTitle(self, title):
		#Append to file
		with open(self.filename, 'a') as file:
			file.write(title+"\n")
		#Append to array
		self.files.append(title)
