#!/usr/bin/env python

#Copyright 2017 Martin Cooney
#This file is subject to the terms and conditions defined in file 'Readme.md', which is part of this source code package.
 
import re

#--------------------------------------------------------
# Setup (please change parameters as needed for your case)
#--------------------------------------------------------

conditionName = 'objects'
inputFileName =  '../../output/%s_resultsLogFile.dat' % conditionName
outputFileName = '../../output/excel/acc.csv' 
numberOfObjects = 5

resultsLogFile = open(inputFileName, 'r')
l = list(resultsLogFile)
resultsLogFile.close()

linesOfResultsPerFrame = 1
numberOfResults = len(l)
numberOfCorrectAnswers = 0
numberOfIncorrectAnswers = 0

print ""
print "---------------------------------------------------"
print "= Results of detecting touched objects (MAY 2017) ="
print "---------------------------------------------------"
print ""

#--------------------------------------------------------
# Read in predictions and analyze
#--------------------------------------------------------

for frameResult in range(numberOfResults):
	myList = re.split(' |\n', l[(frameResult*linesOfResultsPerFrame)])
	myList2 = re.split('_|\n', myList[0])

	if(int(myList[1]) == int(myList[2])):
		numberOfCorrectAnswers = numberOfCorrectAnswers + 1
	else:
		numberOfIncorrectAnswers = numberOfIncorrectAnswers + 1

#--------------------------------------------------------
# Output results
#--------------------------------------------------------
		
if (numberOfCorrectAnswers + numberOfIncorrectAnswers) > 0:
	print "Number of total answers:", (numberOfCorrectAnswers + numberOfIncorrectAnswers)
	print "Number of correct answers:", numberOfCorrectAnswers
	print "Number of incorrect answers:", numberOfIncorrectAnswers
	print "Accuracy:", float(numberOfCorrectAnswers) / float(numberOfCorrectAnswers + numberOfIncorrectAnswers) * 100
print " "




