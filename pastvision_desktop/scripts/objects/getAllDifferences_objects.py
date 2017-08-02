#!/usr/bin/env python

#Copyright 2017 Martin Cooney
#This file is subject to the terms and conditions defined in file 'Readme.md', which is part of this source code package.

import sys

conditionName = 'objects'

#use these parameters to run a quick test
numberOfSamples = 1
numberOfObjects = 1
startFrame = 15
stopFrame = 20


#use these parameters instead to process the entire dataset
'''
numberOfSamples = 4 
numberOfObjects = 5
startFrame = 0
stopFrame = 24
'''

print ""
print "--------------------------------------------"
print "= Test detecting object touches (MAY 2017) ="
print "--------------------------------------------"
print ""

#clear file
outputFileName= '../../output/%s_resultsLogFile.dat' % conditionName
resultsLogFile=open(outputFileName, 'w')
resultsLogFile.close()

#execute test
for sampleIndex in range(numberOfSamples):
	for objectIndex in range(numberOfObjects):
		for frameIndex in range(startFrame, stopFrame):
			arg2= '%s%d_%d_%d' % (conditionName, sampleIndex+1, objectIndex+1, frameIndex)
			sys.argv=['../../data/objects/cropped', arg2, conditionName, str(objectIndex+1)]
			execfile("calculateStatistics_objects.py")

