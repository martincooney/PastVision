#!/usr/bin/env python

#Copyright 2017 Martin Cooney
#This file is subject to the terms and conditions defined in file 'Readme.md', which is part of this source code package.

# import the necessary packages
import numpy as np
import cv2
from subprocess import call
import sys
import math

#--------------------------------------------------------
# Setup
#--------------------------------------------------------

#Some default alignment parameters for the default dataset of drinking water: 
#(please replace these with your own parameters if using different data)
width=320
height=240
shiftx=30
shifty=0
zoomFactor=10
alpha=0.7
shiftUp = 22

#get arguments and filenames:
#please change these as needed to match where folders are on your system
basename = sys.argv[0] 
beforeBaseName = sys.argv[1] 
conditionName = sys.argv[2] 
thermalFileName = "%s/%s_thermal.jpg" % (basename, beforeBaseName)
rgbFileName = "%s/%s_rgb.jpg" % (basename, beforeBaseName)
image_rgb = cv2.imread(rgbFileName)
image_thermal = cv2.imread(thermalFileName)
image_rgb= cv2.resize(image_rgb, (width, height)) 
image_thermal = cv2.resize(image_thermal, (width, height)) 
outputThermalImageFilename = "../../data/mouth/output/out_%s_thermal.jpg" % beforeBaseName
outputRGBImageFilename = "../../data/mouth/output/out_%s_rgb.jpg" % beforeBaseName
shifted_RGB_filename = '../../data/mouth/my_rgb_shifted.jpg'
facial_landmarks_filename = '../../data/mouth/face_landmarks_detected.txt'
facial_landmark_detector_path = "../../../../dlib/examples/build/pastvision-face_landmark_detection_ex"
outputPredictionsFileName= '../../output/%s_predictions.dat' % conditionName
outputFeaturesFileName= '../../output/%s_resultsLogFile.dat' % conditionName

#align mask and rgb for both before and after
shifted_rgb= image_rgb[shifty+zoomFactor:240-zoomFactor, 0+zoomFactor:320-shiftx-zoomFactor]
shifted_thermal= image_thermal[0+shiftUp:240-shifty, shiftx:320]
shifted_rgb = cv2.resize(shifted_rgb, (width, height))
shifted_thermal= cv2.resize(shifted_thermal, (width, height)) 

#init vars just in case needed
myMask = np.zeros((height, width), dtype=np.uint8)
faceWindowMask = np.zeros((height, width), dtype=np.uint8)
bothMask = np.zeros((height, width), dtype=np.uint8)
faceAreaInWindow = np.zeros((height, width), dtype=np.uint8)
bothMaskColor = np.zeros((height, width, 3), dtype=np.uint8)
outputBM= np.zeros((height, width, 3), dtype=np.uint8)
colorToUse = (0, 0, 255)

#to store results
myStatistics = [ ]

print ""
print "= Detect drinking in a single frame (MAY 2017) ="
print beforeBaseName

#--------------------------------------------------------
# Detect facial landmarks
#--------------------------------------------------------

#system call to find face landmarks
cv2.imwrite(shifted_RGB_filename, shifted_rgb)
call(facial_landmark_detector_path, shell=True)

#read in the facial landmark positions from the output file
f=open(facial_landmarks_filename, 'r')
l=list(f)
f.close()

print ("")
if len(l) == 73:   			#if a face is detected
	print ("Detected a face")
	facial_landmarks=[]
	num_of_faces = l[0].rstrip()
	face_left= l[1].rstrip()
	face_top = l[2].rstrip()
	face_right = l[3].rstrip()
	face_bottom = l[4].rstrip()

	for pointIndex in range(4,72):
		facial_landmark_data = l[1+pointIndex].rstrip()
		facial_landmark_data2 = facial_landmark_data.split()
		facial_landmark_data2_x = facial_landmark_data2[0]
		facial_landmark_data2_y = facial_landmark_data2[1]
		facial_landmark_data2_x = facial_landmark_data2_x.replace('(', '').replace(')', '').replace(',', '')
		facial_landmark_data2_y = facial_landmark_data2_y.replace('(', '').replace(')', '').replace(',', '')
		facial_landmarks.append((int(facial_landmark_data2_x)/2, int(facial_landmark_data2_y)/2))

#--------------------------------------------------------
# Detect lips area
#--------------------------------------------------------

	L=[]

	#outer lips
	start=48
	end=60
	for pointIndex in range(start, end):
		L.append(facial_landmarks[pointIndex])

	#turn this list of outer lip points into an opencv contour and draw it
	cnt = np.array(L).reshape((-1,1,2)).astype(np.int32)
	imgray = cv2.cvtColor(shifted_thermal,cv2.COLOR_BGR2GRAY)
	mask = np.zeros(imgray.shape,np.uint8)
	cv2.drawContours(mask,[cnt],0,255,-1)
	areaOfOuterMouth = cv2.contourArea(cnt)
	cv2.drawContours(shifted_rgb,[cnt],0,(0,0,255),-1)

	#find a second contour for the inside of lips and draw it in black
	L=[]
	start=60
	end=65
	for pointIndex in range(start, end):
		L.append(facial_landmarks[pointIndex])
        cnt = np.array(L).reshape((-1,1,2)).astype(np.int32)
	cv2.drawContours(mask,[cnt],0,0,-1) #color black
	cv2.drawContours(shifted_rgb,[cnt],0,(0,0,0),-1)
	areaOfInnerMouth = cv2.contourArea(cnt)

#--------------------------------------------------------
# Calculate statistics
#--------------------------------------------------------

	#find the mean, std, median, min/max (intensity and location) for lips area; and, nose length, and mean intensity between mouth and chin
	(means, stds) = cv2.meanStdDev(imgray,mask = mask)
	pixelpoints = np.transpose(np.nonzero(mask))
	intensities= []
	for pointIndex in range(len(pixelpoints)):
		intensities.append(imgray[pixelpoints[pointIndex][0]][pixelpoints[pointIndex][1]])
	myMedian=np.median(intensities)
	min_val, max_val, min_loc,max_loc = cv2.minMaxLoc(imgray,mask = mask)

	noseLength= math.sqrt( (float(facial_landmarks[27][0])-float(facial_landmarks[30][0])) ** 2 + (float(facial_landmarks[27][1])-float(facial_landmarks[30][1])) ** 2 )
	
	#get the mean also for an area from the bottom of the mouth to the chin, which should not change after drinking
	L=[]
	start=7
	end=10
	for pointIndex in range(start, end):
		L.append(facial_landmarks[pointIndex])
	start=55
	end=60
	for pointIndex in range(start, end):
		L.append(facial_landmarks[pointIndex])
	cnt = np.array(L).reshape((-1,1,2)).astype(np.int32)
	mask = np.zeros(imgray.shape,np.uint8)
	cv2.drawContours(mask,[cnt],0,255,-1)
	areafromMouthToChin = cv2.contourArea(cnt)
	(meansMyArea, stdsMyArea) = cv2.meanStdDev(imgray,mask = mask)
	meanForMyArea=meansMyArea[0][0]

	myStatistics.append(means[0][0])
	myStatistics.append(stds[0][0])
	myStatistics.append(myMedian)
	myStatistics.append(min_val)
	myStatistics.append(max_val)
	myStatistics.append(min_loc)
	myStatistics.append(max_loc)
	myStatistics.append(noseLength)
	myStatistics.append(meanForMyArea)

#--------------------------------------------------------
# Draw detection results
#--------------------------------------------------------

	#draw face outline
	start=0
	end=16
	for pointIndex in range(start, end):
		cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (0, 255, 0))

	#draw eyebrows
	start=17
	end=21
	for pointIndex in range(start, end):
			cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (0, 255, 0))
	start=22
	end=26
	for pointIndex in range(start, end):
		cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (0, 255, 0))

	#draw nose
	start=27 #vertical line of nose
	end=30
	for pointIndex in range(start, end):
		cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (0, 255, 0))
	start=31 #bottom part of nose
	end=35
	for pointIndex in range(start, end):
		cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (0, 255, 0))

	#draw eyes
	start=36
	end=41
	for pointIndex in range(start, end):
		cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (0, 255, 0))
	cv2.line(shifted_thermal, facial_landmarks[end], facial_landmarks[start], (0, 255, 0))
	start=42
	end=47
	for pointIndex in range(start, end):
		cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (0, 255, 0))
	cv2.line(shifted_thermal, facial_landmarks[end], facial_landmarks[start], (0, 255, 0))
	
	#draw outer lips
	start=48
	end=60
	for pointIndex in range(start, end):
		cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (255, 0, 0))
	cv2.line(shifted_thermal, facial_landmarks[end], facial_landmarks[start], (255, 0, 0))

	#draw inner lips
	start=60
	end=67
	for pointIndex in range(start, end):
		cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (255, 0, 0))
		
	#draw area below the lips used for comparison
	start=7
	end=10
	for pointIndex in range(start, end):
		cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (255, 255, 0))
	start=55
	end=59
	for pointIndex in range(start, end):
		cv2.line(shifted_thermal, facial_landmarks[pointIndex], facial_landmarks[pointIndex+1], (255, 255, 0))
	cv2.line(shifted_thermal, facial_landmarks[7], facial_landmarks[58], (255, 255, 0))
	cv2.line(shifted_thermal, facial_landmarks[9], facial_landmarks[55], (255, 255, 0))
		
	#draw face rectangles
	cv2.rectangle(shifted_rgb, (int(face_left)/2, int(face_top)/2), (int(face_right)/2, int(face_bottom)/2), colorToUse, thickness=2)
	cv2.rectangle(shifted_thermal, (int(face_left)/2, int(face_top)/2), (int(face_right)/2, int(face_bottom)/2), colorToUse, thickness=2)

	#draw a circle where the intensity is lowest (coldest temperature) 
	cv2.circle(shifted_rgb, min_loc, 2, (0,255,0), -1)


else: 	#if no face found add some dummy values
	for ind in range(9):
		myStatistics.append(-1)

#--------------------------------------------------------
# Predict drinking
#--------------------------------------------------------

#using SD
classifierPrediction = -1
if len(l) == 73:
	if noseLength < 11:
		if myStatistics[1] > 6:
			classifierPrediction = 1
		else:
			classifierPrediction = 0		

#--------------------------------------------------------
# Output results
#--------------------------------------------------------


resultsLogFile=open(outputPredictionsFileName, 'a')
lineToWrite= "%s %d\n" % (beforeBaseName, classifierPrediction)
resultsLogFile.write(lineToWrite)
resultsLogFile.close()

resultsLogFile=open(outputFeaturesFileName, 'a')
lineToWrite= "RESULT! %s \n" % (beforeBaseName)
resultsLogFile.write(lineToWrite)
lineToWrite= "mean: %d\n" % (myStatistics[0])
resultsLogFile.write(lineToWrite)
lineToWrite= "sd: %d\n" % (myStatistics[1])
resultsLogFile.write(lineToWrite)
lineToWrite= "median: %d\n" % (myStatistics[2])
resultsLogFile.write(lineToWrite)
lineToWrite= "noseLength: %d\n" % (myStatistics[7])
resultsLogFile.write(lineToWrite)
lineToWrite= "meanForMyArea: %d\n" % (myStatistics[8])
resultsLogFile.write(lineToWrite)
resultsLogFile.close()

print("Statistics:")
print "  mean: ", myStatistics[0]
print "  sd: ", myStatistics[1]
print "  median: ", myStatistics[2]
print "  noseLength: ", myStatistics[7]
print "  mean for area below lips: ", myStatistics[8]
print ""

 
cv2.imwrite(outputThermalImageFilename, shifted_thermal)
cv2.imwrite(outputRGBImageFilename, shifted_rgb)





