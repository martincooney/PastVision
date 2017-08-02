#!/usr/bin/env python

#Copyright 2017 Martin Cooney
#This file is subject to the terms and conditions defined in file 'Readme.md', which is part of this source code package.

import cv2
import numpy as np
import sys

basename = '../../data/objects/objects1'
if len(sys.argv) > 1:
	basename = sys.argv[1]

thermalFileName = "%s-thermal1.avi" % basename
rgbFileName = "%s-rgb.avi" % basename
cap=cv2.VideoCapture(rgbFileName)
cap_thermal=cv2.VideoCapture(thermalFileName)
currentFrame=0

cv2.namedWindow("RGB")
cv2.moveWindow("RGB",0,200)
cv2.namedWindow("Thermal")
cv2.moveWindow("Thermal",320,200)

print ""
print "--------------------------"
print "= Find frames (MAY 2017) ="
print "--------------------------"
print ""

print("Press f to output frame number, w to write a frame to image, and q to quit")
while(cap.isOpened() and cap_thermal.isOpened()):
	ret, frame = cap.read()
	ret, frame_thermal = cap_thermal.read()
	if not (frame is None or frame_thermal is None):
		currentFrame=currentFrame+1
		cv2.imshow('RGB', frame)
		cv2.imshow('Thermal', frame_thermal)
	key = cv2.waitKey(50)
	if key == ord('q'):
		break
	elif key == ord('f'): #output the current frame number to console
		print currentFrame
	elif key == ord('w'): #output the current frame as an image
		if not (frame is None or frame_thermal is None):
			print currentFrame
                        filename = "../../data/captured_frames/cap%d_rgb.jpg" % currentFrame
			cv2.imwrite(filename, frame)
			filename = "../../data/captured_frames/cap%d_thermal.jpg" % currentFrame
			cv2.imwrite(filename, frame_thermal)

cap.release()
cap_thermal.release()
cv2.destroyAllWindows()


