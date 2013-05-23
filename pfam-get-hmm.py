#! /usr/bin/python

##	pfam-get-hmm.py
##	Sandip Chatterjee
##
##	Usage:
##		>>python pfam-get-hmm.py
##		-OR-
##		>>python pfam-get-hmm.py list_of_pfam_search_terms.txt
##
##	Quick and dirty script for downloading Pfam HMM files that contain a given search term
##	Uses: http://pfam.janelia.org/families?output=text
##	
##	Can optionally accept an input file containing a list of search terms (1 per line)

import urllib2
import sys

print "pfam-get-hmm.py"
print "For obtaining Pfam HMM files that contain a given search term"

searchTerms = []

if len(sys.argv) == 1:

	print "Search for what?"
	searchTerms.append(raw_input())

elif len(sys.argv) == 2:

	print "Searching for Pfam families matching entries in file "+sys.argv[1]

	inputFile = open(sys.argv[1],'rb')
	searchTerms = []
	for line in inputFile:
		searchTerms.append(line.rstrip('\n'))
	inputFile.close()

	print str(len(searchTerms))+" search terms found"

else:
	print "Wrong number of arguments"
	sys.exit()

print "Accessing Pfam at http://pfam.janelia.org/"
response = urllib2.urlopen('http://pfam.janelia.org/families?output=text')

fullPageList = []
for line in response:
	if '#' not in line and 'PF' in line:
		fullPageList.append(line.rstrip().split('\t'))

response.close()

filteredFullPageList = [entry for entry in fullPageList if entry[1] in searchTerms]

print "Searched Pfam family list at http://pfam.janelia.org/families and found "+str(len(filteredFullPageList))+" entries matching your search terms"

if filteredFullPageList:
	print "Downloading HMM files"
	for entry in filteredFullPageList:
		pfamID = entry[0]
		
		hmmURL = urllib2.urlopen("http://pfam.janelia.org/family/"+pfamID+"/hmm")
		outputFile = open(pfamID+'.hmm','wb')
		outputFile.write(hmmURL.read())
		outputFile.close()
		hmmURL.close()

		sys.stdout.write("\rDownloaded file: %s   " % pfamID )
		sys.stdout.flush()
	print ''
	print "Finished downloading "+str(len(filteredFullPageList))+" files.  Concatenate all new .hmm files into one file? y/n"
	if raw_input() == 'y':
		filenames = [entry[0]+'.hmm' for entry in filteredFullPageList]
		if len(sys.argv) == 1:
			catFileName = searchTerms[0]
		else:
			catFileName = sys.argv[1]
		with open(catFileName+'_concatenated.hmm','w') as outputFile:
			for filename in filenames:
				with open(filename,'r') as inputFile:
					for line in inputFile:
						outputFile.write(line)
		print "Concatenated "+str(len(filenames))+" files and saved as file "+catFileName+'_concatenated.hmm'

else:
	print "Try different search terms"
