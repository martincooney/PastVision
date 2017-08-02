#!/usr/bin/env python

#Copyright 2017 Martin Cooney
#This file is subject to the terms and conditions defined in file 'Readme.md', which is part of this source code package.

import sys

#use these parameters to run a quick test
numberOfConditions = 1
numberOfSamples = 1
startFrame = 10
stopFrame = 15

#use these parameters instead to process the entire dataset
'''
numberOfConditions = 2
numberOfSamples = 5 
startFrame = 0
stopFrame = 24
'''

print ""
print "---------------------------------------------------------------"
print "= Test detecting cooled lips due to drinking water (MAY 2017) ="
print "---------------------------------------------------------------"
print ""

for conditionIndex in range(2): #2 conditions, cold and tepid
	
	if conditionIndex == 0:
		conditionName = 'cold'
	else:
		if numberOfConditions == 1:
			continue
		else: 			
			conditionName = 'tepid'

	#clear files
	outputFileName= '../../output/%s_resultsLogFile.dat' % conditionName
	resultsLogFile=open(outputFileName, 'w')
	resultsLogFile.close()
	outputFileName= '../../output/%s_predictions.dat' % conditionName
	resultsLogFile=open(outputFileName, 'w')
	resultsLogFile.close()

	#execute test
	for sampleIndex in range(numberOfSamples): 
		for frameIndex in range(startFrame, stopFrame): 
			arg2= '%s%d_%d' % (conditionName, sampleIndex+1, frameIndex)
			sys.argv=['../../data/mouth/cropped', arg2, conditionName]
			execfile("calculateStatistics_mouth.py")



