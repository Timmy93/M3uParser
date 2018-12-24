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

class M3uParser:
	
	def __init__(self):
		self.files = []
	
	#Download the file from the given url
	def downloadM3u(self, url, filename):
		if not filename:
			filename = "test.m3u"
		try:
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
	
	def getNoStreaming(self):
		return list(filter(lambda file: not file["titleFile"].endswith(".ts"), self.files))
	
	def getNoCamNoStreaming(self):
		return list(filter(lambda file: "Cam" not in file["tvg-group"], self.getNoStreaming()))

