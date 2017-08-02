#!/usr/bin/env python

#Copyright 2017 Martin Cooney
#This file is subject to the terms and conditions defined in file 'Readme.md', which is part of this source code package.

import cv2
import numpy as np
import sys

basename = ''
if len(sys.argv) > 1:
	basename = sys.argv[1]
else:
	basename = "../../data/objects/objects1"

width=320
height=240
thermalFileName = "%s-thermal1.avi" % basename
rgbFileName = "%s-rgb.avi" % basename
cap_thermal=cv2.VideoCapture(thermalFileName)
cap_rgb=cv2.VideoCapture(rgbFileName)

#below is an example of parameters which can be used for the object touching data
shiftx=38
shifty=0
zoomFactor=20
alpha=0.7
shiftUp = 60

'''
#an example of parameters for drinking cold or tepid water
shiftx=30
shifty=0
zoomFactor=10#10
alpha=0.7
shiftUp = 25
'''

print ""
print "------------------------------------"
print "= Find shift parameters (MAY 2017) ="
print "------------------------------------"
print ""

cv2.namedWindow('thermal')
cv2.namedWindow('RGB')
cv2.namedWindow('overlay')
cv2.moveWindow('thermal', 500, 100)
cv2.moveWindow('RGB', 820, 100)
cv2.moveWindow('overlay', 1120, 100)

ret, my_thermal_image = cap_thermal.read()
ret, my_rgb_image = cap_rgb.read()

print("Press q to quit")
while(cap_thermal.isOpened()):

	ret, my_thermal_image = cap_thermal.read()
	ret, my_rgb_image = cap_rgb.read()

	if (my_rgb_image is None or my_thermal_image is None):
		break;
	else:

		#align rgb and thermal
		shifted_rgb= my_rgb_image[shifty+zoomFactor:240-zoomFactor, 0+zoomFactor:320-shiftx-zoomFactor]
		shifted_thermal= my_thermal_image[0+shiftUp:240-shifty, shiftx:320]
		shifted_rgb = cv2.resize(shifted_rgb, (width, height))
		shifted_thermal = cv2.resize(shifted_thermal, (width, height))

		#create an overlay
		over1=shifted_thermal.copy()
		over2=shifted_rgb.copy() 
		overlay=shifted_rgb.copy()
		cv2.addWeighted(over1, alpha, over2, 1-alpha, 0, overlay)

		#display
		cv2.imshow('RGB', shifted_rgb)
		cv2.imshow('thermal', shifted_thermal)
		cv2.imshow('overlay', overlay)
	
	key = cv2.waitKey(100)
	if key == ord('q'):
		break

cap_thermal.release()
cap_rgb.release()
cv2.destroyAllWindows()


