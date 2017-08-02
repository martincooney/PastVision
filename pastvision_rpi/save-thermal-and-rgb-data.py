#!/usr/bin/env python

#Copyright 2017 Martin Cooney
#This file is subject to the terms and conditions defined in file 'Readme.md', which is part of this source code package.

#This code incorporates code from the pylepton library to access a FLIR thermal camera
#and Adrian Rosebrock's imutils to access the picamera
#Please make sure to install these libraries.

from __future__ import print_function
import time
import numpy as np
from imutils.video.pivideostream import PiVideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import traceback
from pylepton import Lepton
from PIL import Image
import sys
import datetime


now=datetime.datetime.now()

cv2.namedWindow("RGB")
cv2.moveWindow("RGB",0,200)
cv2.namedWindow("ThermalDynamic")
cv2.moveWindow("ThermalDynamic",320,200)
cv2.namedWindow("ThermalStatic")
cv2.moveWindow("ThermalStatic",640,200)
cv2.namedWindow("Clock")
cv2.moveWindow("Clock",0,470)

device = "/dev/spidev0.0"
lepton_buf = np.zeros((60, 80, 1), dtype=np.uint16)
clock_image = np.zeros((240, 960, 3), dtype=np.uint8)

vs = PiVideoStream().start()
time.sleep(2.0)

basename = ''
if len(sys.argv) > 1:
	basename = sys.argv[1]
else:
	basename = "%d-%d-%d_%d-%d-%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

thermalFileName = "raw-data/%s-thermal.dat" % basename
rgbFileName = "raw-data/%s-rgb.avi" % basename
timesFileName = "raw-data/%s-times.dat" % basename

fourcc = cv2.cv.CV_FOURCC(*'XVID')
out_rgb = cv2.VideoWriter(rgbFileName, fourcc, 20.0, (320, 240))

f = open(thermalFileName, 'a')
f2 = open(timesFileName, 'a')

num_frames = 0

print ""
print "---------------------------------------"
print "= Record thermovisual data (MAY 2017) ="
print "---------------------------------------"
print ""

try:

	time.sleep(0.2) # give the overlay buffers a chance to initialize
	start=time.time()
	with Lepton(device) as l:
		last_nr = 0
		while True:
			_,nr = l.capture(lepton_buf)
			if nr == last_nr:
				# no need to redo this frame
				continue

                        num_frames=num_frames+1
                        last_nr = nr
                        
			#save thermal and timestamp data
                        lep_copy= lepton_buf.copy()                        
                        np.save(f, lepton_buf)
                        now=datetime.datetime.now()
                        timeStamp = "%d %d_%d-%d-%d\n" % (num_frames, now.hour, now.minute, now.second, now.microsecond)
                        f2.write(timeStamp)
                        
			#prepare the RGB image
			frame = vs.read()
			frame = cv2.flip(frame, 0)
			frame = cv2.resize(frame, (320, 240))
                        out_rgb.write(frame)

			#prepare an adaptive thermal image (just for displaying)
                        cv2.normalize(lepton_buf, lepton_buf, 0, 65535, cv2.NORM_MINMAX)
                        np.right_shift(lepton_buf, 8, lepton_buf)
                        img = np.uint8(lepton_buf)
                        largerThermal2 = cv2.flip(img, 0)
                        largerThermal = cv2.resize(largerThermal2, (320, 240))

			#prepare a thresholded thermal image (just for displaying)
                        myMin=8150
                        myMax=myMin+255
                        x= np.clip(lep_copy, myMin, myMax)
                        y = (x-myMin)
                        z= y.astype(int)
                        img2 = np.uint8(z)
                        print(img2[0][0][0])                        
                        humanThermal = cv2.flip(img2, 0)
                        humanThermal = cv2.resize(humanThermal, (320, 240))                                  

			#prepare a clock image (just for displaying)
			now=datetime.datetime.now()
			dateStr = "%d-%d-%d" % (now.hour, now.minute, now.second)
                        cv2.rectangle(clock_image, (0,0), (960,240), (0,0,0), -1)
                        cv2.putText(clock_image, dateStr, (200,150), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255))

			cv2.imshow("ThermalDynamic", largerThermal)
			cv2.imshow("ThermalStatic", humanThermal) 			
			cv2.imshow("RGB", frame)
			cv2.imshow("Clock", clock_image)

			key = cv2.waitKey(10) 

			if key == 27:
				break

except Exception:
	traceback.print_exc()

#display some time information
end=time.time()
seconds=end-start
fps=num_frames/seconds;
str=  "estimated fps: %f" % fps 
print (str)

#add an eof marker
myEOFArray = np.zeros((60, 80, 1), dtype=np.uint16)
np.save(f, myEOFArray)

#clean up
f.close()
f2.close()
cv2.destroyAllWindows()
vs.stop()
out_rgb.release()
cv2.waitKey(100)


