#!/usr/bin/python3
# Purpose:	
# Usage:	
# Author:	Timmy93
# Date:		
# Version:	
# Disclaimer:	

import os
import re
import urllib.request
import random

class M3uParser:
	
	def __init__(self):
		self.files = []
	
	#Download the file from the given url
	def downloadM3u(self, url, filename):
		currentDir = os.path.dirname(os.path.realpath(__file__))
		if not filename:
			filename = "test.m3u"
		try:
			filename = os.path.join(currentDir, filename)
			urllib.request.urlretrieve(url, filename)
		except:
			print("Cannot download anything from the url\nHave you modified the ini file?")
			exit()
		self.readM3u(filename)
	
	#Read the file from the given path
	def readM3u(self, filename):
		self.filename = filename
		self.readAllLines()
		self.parseFile()

	#Read all file lines
	def readAllLines(self):
		self.lines = [line.rstrip('\n') for line in open(self.filename)]
		return len(self.lines)
	
	def parseFile(self):
		numLine = len(self.lines)
		for n in range(numLine):
			line = self.lines[n]
			if line[0] == "#":
				#print("Letto carattere interessante")
				self.manageLine(n)
	
	def manageLine(self, n):
		lineInfo = self.lines[n]
		lineLink = self.lines[n+1]
		if lineInfo != "#EXTM3U":
			m = re.search("tvg-name=\"(.*?)\"", lineInfo)
			name = m.group(1)
			m = re.search("tvg-ID=\"(.*?)\"", lineInfo)
			id = m.group(1)
			m = re.search("tvg-logo=\"(.*?)\"", lineInfo)
			logo = m.group(1)
			m = re.search("group-title=\"(.*?)\"", lineInfo)
			group = m.group(1)
			m = re.search(",(.*?)$", lineInfo)
			title = m.group(1)
			# ~ print(name+"||"+id+"||"+logo+"||"+group+"||"+title)
			
			test = {
				"title": title,
				"tvg-name": name,
				"tvg-ID": id,
				"tvg-logo": logo,
				"tvg-group": group,
				"titleFile": os.path.basename(lineLink),
				"link": lineLink
			}
			self.files.append(test)
			
	def exportJson(self):
		#TODO
		print("Not implemented")
	
	#Remove files with a certain file extension
	def filterOutFilesEndingWith(self, extension):
		self.files = list(filter(lambda file: not file["titleFile"].endswith(extension), self.files))
	
	#Select only files with a certain file extension
	def filterInFilesEndingWith(self, extension):
		#Use the extension as list
		if not isinstance(extension, list):
			extension = [extension]
		if not len(extension):
			logging.info("No filter in based on extensions")
		new = []
		#Iterate over all files and extensions
		for file in self.files:	
			for ext in extension:
				if file["titleFile"].endswith(ext):
					#Allowed extension - go to next file
					new.append(file)
					break
		logging.info("Filter in based on extension: ["+",".join(extension)+"]")
		self.files = new
	
	#Remove files that contains a certain filterWord
	def filterOutFilesOfGroupsContaining(self, filterWord):
		self.files = list(filter(lambda file: filterWord not in file["tvg-group"], self.files))

	#Select only files that contais a certain filterWord
	def filterInFilesOfGroupsContaining(self, filterWord):
		#Use the filter words as list
		if not isinstance(filterWord, list):
			filterWord = [filterWord]
		if not len(filterWord):
			logging.info("No filter in based on groups")
			return
		new = []
		for file in self.files:
			for fw in filterWord:	
				if fw in file["tvg-group"]:
					#Allowed extension - go to next file
					new.append(file)
					break
		logging.info("Filter in based on groups: ["+",".join(filterWord)+"]")
		self.files = new

	#Getter for the list
	def getList(self):
		return self.files
		
	#Return the info assciated to a certain file name
	def getCustomTitle(self, originalName):
		result = list(filter(lambda file: file["titleFile"] == originalName, self.files))
		if len(result):
			return result
		else:
			print("No file corresponding to: "+originalName)

	#Return a random element
	def getRandomFile(self):
		random.shuffle(self.files)
		return self.files.pop()
