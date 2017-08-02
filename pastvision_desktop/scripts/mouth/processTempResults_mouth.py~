#!/usr/bin/env python

#Copyright 2017 Martin Cooney
#This file is subject to the terms and conditions defined in file 'Readme.md', which is part of this source code package.
 
import re

#--------------------------------------------------------
# Setup (please change parameters as needed for your case)
#--------------------------------------------------------

conditionName='cold'
#conditionName='tepid'
inputFileName= '../../output/%s_predictions.dat' % conditionName
linesOfResultsPerFrame=1
correctAnswer=-1
predictedAnswer=-1
numberOfCorrectAnswers = 0
numberOfIncorrectAnswers = 0
numberOfBadFrames = 0

print ""
print "---------------------------------------------------------------------"
print "= Results of detecting cooled lips due to drinking water (MAY 2017) ="
print "---------------------------------------------------------------------"
print ""

#--------------------------------------------------------
# Read in predictions and analyze
#--------------------------------------------------------

resultsLogFile=open(inputFileName, 'r')
l=list(resultsLogFile)
resultsLogFile.close()

for frameResult in range(len(l)):
	myList= re.split(' |\n', l[(frameResult*linesOfResultsPerFrame)])
	myList2= re.split('_|\n', myList[0])

	predictedAnswer = int(myList[1])
	frameNo= int(myList2[1])

	if(frameNo < 3): 
		correctAnswer = 0
	else:
		correctAnswer = 1

	if(predictedAnswer==-1):
		numberOfBadFrames = numberOfBadFrames + 1
	elif(predictedAnswer==correctAnswer):
		numberOfCorrectAnswers= numberOfCorrectAnswers + 1
	else:
		numberOfIncorrectAnswers = numberOfIncorrectAnswers + 1

#--------------------------------------------------------
# Output results
#--------------------------------------------------------

print "Condition:", conditionName
print "Total number of samples:", numberOfCorrectAnswers+numberOfIncorrectAnswers+numberOfBadFrames
print "Number of correct answers:", numberOfCorrectAnswers 
print "Number of incorrect answers:", numberOfIncorrectAnswers
print "Number of bad frames with no face detected:", numberOfBadFrames
print "Accuracy ignoring bad frames:", (100.0 * (float(numberOfCorrectAnswers)/float(numberOfCorrectAnswers+numberOfIncorrectAnswers)))
print "Accuracy including bad frames:", (100.0* (float(numberOfCorrectAnswers)/float(numberOfCorrectAnswers+numberOfIncorrectAnswers+numberOfBadFrames)))
print ""



