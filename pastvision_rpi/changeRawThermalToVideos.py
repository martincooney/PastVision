#!/usr/bin/env python

#Copyright 2017 Martin Cooney
#This file is subject to the terms and conditions defined in file 'Readme.md', which is part of this source code package.

#This makes three different thermal video files thresholded at different temperature ranges from a single raw thermal data file
#the idea is we want to avoid lossy normalization (keep the resolution) and arbitrary adaptation (intensity values should still be informative about temperatures)
#while making the thermal data easy to process and display with OpenCV
#the first video is intended for working with hot objects like humans, the second for room temperature objects, and the third for cold objects. 

import cv2
import numpy as np
import datetime
import sys

now=datetime.datetime.now()

basename = '../pastvision_desktop/data/objects/objects1'
if len(sys.argv) > 1:
	basename = sys.argv[1]

motherFile = "%s-thermal.dat" % basename
thermalFileName1 = "%s-thermal1.avi" % basename
thermalFileName2 = "%s-thermal2.avi" % basename
thermalFileName3 = "%s-thermal3.avi" % basename

fourcc = cv2.cv.CV_FOURCC(*'XVID') #this works with older versions of opencv
#fourcc = cv2.VideoWriter_fourcc(*'XVID') #for newer versions of opencv please comment above and uncomment this line

out_thermal1= cv2.VideoWriter(thermalFileName1, fourcc, 20.0, (320, 240), 0)
out_thermal2= cv2.VideoWriter(thermalFileName2, fourcc, 20.0, (320, 240), 0)
out_thermal3= cv2.VideoWriter(thermalFileName3, fourcc, 20.0, (320, 240), 0)
num_frames=0

cv2.namedWindow("Thermal1")
cv2.moveWindow("Thermal1",500,500)
cv2.namedWindow("Thermal2")
cv2.moveWindow("Thermal2",800,500)
cv2.namedWindow("Thermal3")
cv2.moveWindow("Thermal3",1100,500)

print ""
print "----------------------------------------------------"
print "= Generate videos from raw thermal data (MAY 2017) ="
print "----------------------------------------------------"
print ""


with open(motherFile, 'r') as f:
    while True:
        frame= np.load(f)
        if frame[0][0][0]==0:
            print "reached EOF"
            break

        myMin=8150
        myMax=myMin+255
        x= np.clip(frame, myMin, myMax)
        y = (x-myMin)
        z= y.astype(int)
        img2 = np.uint8(z)                       
        img = cv2.flip(img2, 0)
        img = cv2.resize(img, (320, 240))        
        out_thermal1.write(img)       
        cv2.imshow("Thermal1", img)

        myMin=myMin-122
        myMax=myMin+255
        x= np.clip(frame, myMin, myMax)
        y = (x-myMin)
        z= y.astype(int)
        img2 = np.uint8(z)                       
        img = cv2.flip(img2, 0)
        img = cv2.resize(img, (320, 240))        
        out_thermal2.write(img)       
        cv2.imshow("Thermal2", img)

        myMin=myMin-255
        myMax=myMin+255
        x= np.clip(frame, myMin, myMax)
        y = (x-myMin)
        z= y.astype(int)
        img2 = np.uint8(z)                       
        img = cv2.flip(img2, 0)
        img = cv2.resize(img, (320, 240))        
        out_thermal3.write(img)       
        cv2.imshow("Thermal3", img)
      
        key = cv2.waitKey(5) 
        if key == 27:
            break

f.close()
cv2.destroyAllWindows()
out_thermal1.release()
out_thermal2.release()
out_thermal3.release()

