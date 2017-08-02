
PastVision+

1) Basic Concept

Thermal and RGB cameras can be used together to autonomously infer what some people have done recently in the presence of temporary occlusions, by combining detection of heat traces with detection of people and objects.
For example, such an approach can be applied toward monitoring medicine intake by dementia patients, an important problem for which mistakes can have disastrous effects.
Specifically, if a dementia patient drinks from a cup, the touched portion of the cup will become warm and the person's lips cool, which can be detected.
More details are provided in some academic papers [1,2].
To help others to get started in this area, the author is making available this code/dataset.

-----------------------------------

2) Content (languages, libraries, and files used) 

As noted above, the code in this folder provides tools for thermovisual action inference for recent unobserved haptic human-object interactions (PastVision+).
This version is initial, comprising the simplest base code; future versions will include richer features.

Programming languages used are Python, C++, and Prolog (for inference).  
Various preexisting libraries and tools used include:  
pylepton		for thermal data acquisition  
OpenCV 3.2.0		for general image processing 		(e.g., whose mouth is cool from drinking?)  
darknet/YOLO9000 v2[3] 	for object detection 			(e.g., has a person touched medicine recently?)  
dlib[4] 		for facial landmark detection 		(e.g., is a person's mouth cool from drinking?)  
imutils			helper functions 

Some useful files are:  
save-thermal-and-rgb-data.py		in /pastvision_rpi/				for recording raw data using the FLIR thermal camera/Raspberry Pi  
changeRawThermalToVideos.py		in /pastvision_rpi/				for making videos from raw data  
findShiftParametersForThermalRGB.py 	in /pastvision_desktop/scripts/basic/		for finding the alignment between RGB and thermal data  
findFrameNumbers.py 			in /pastvision_desktop/scripts/basic/		for find frame numbers when events such as touches occur  
getAllFrames_objects.py			in /pastvision_desktop/scripts/objects/		for extracting frames at set time periods from the video  
getAllDifferences_objects.py 		in /pastvision_desktop/scripts/objects/		for detecting heat traces on objects  
processTempResults_objects.py		in /pastvision_desktop/scripts/objects/		for analysis of heat trace detection results  
getAllFrames_mouth.py			in /pastvision_desktop/scripts/mouth/		for extracting frames at set time periods from the video  
getAllDifferences_mouth.py 		in /pastvision_desktop/scripts/mouth/		for detecting heat traces on people's lips  
processTempResults_mouth.py		in /pastvision_desktop/scripts/mouth/		for analysis of heat trace detection results  

Dataset description:  
The dataset consists of RGB, thermal, and time stamp data, for touching objects (medicine packages) and drinking water.  
In the first case, the experimenter (the author of the code) touched five objects--a PET pill bottle (with paper wrapper), an HDPE lotion bottle, a paper box, a glass cup, and a ceramic cup--for approximately five seconds, four times each.
In the second case, the experimenter drank five times each cold (refrigerated) and room temperature water. 

------------------------

3) Setup

Required Parts  
    1x FLIR thermal camera kit ("FLiR Dev Kit" KIT-13233 for $259.95, available from sparkfun.com)  
    1x Raspberry Pi (with camera, sd card, cables)  
    1x Desktop for processing (the author used a Ubuntu 14.04 desktop with i5 2400 CPU @ 3.1 GHz)  

(a) Setting up the FLIR thermal camera/Raspberry Pi.  
*Follow the directions in the tutorials below to be able to view thermal data
https://learn.sparkfun.com/tutorials/flir-lepton-hookup-guide
https://groupgets.com/blog/posts/8-installation-guide-for-pure-breakout-board-on-raspberry-pi-2
(The author of this code can't help with troubleshooting, but some general advice is that if sudo ./raspberrypi_video yields an error (the red square), the reader can try pushing on the edges of the little black thermal camera module (the contacts are bad) while raspberrypi_video is running, and/or switching CE0 and CE1.)

*Follow the directions in Adrian Rosebrock's tutorials to install helper libraries for the picamera such as imutils (e.g., pip install imutils, pip install "picamera[array]")  
http://www.pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/

*Copy the pastvision_rpi folder onto the Raspberry Pi.  

(b) Setting up the Desktop

*Install darknet/YOLO following the tutorial:  
https://pjreddie.com/darknet/yolo/

*Install dlib following the tutorial:  
http://dlib.net/compile.html

(Install anything else which might be needed, such as OpenCV, and/or python; the author has used OpenCV 3.2.0 and Python 2.7.6)

*Modify darknet and dlib to output results to a file, and recompile
An example of code which can be used to do this (for the author's setup) is provided below:

-For darknet, the following lines were added to function "draw_detections" in "darknet/src/image.c":
#include <stdio.h>  
FILE *fp;  
fp=fopen("../../output/object_detection_results.txt", "w");  
fprintf(fp, "%s\n%.0f%%\n", names[class], prob*100);  
fprintf(fp, "%g\n%g\n%g\n%g\n", b.x, b.y, b.w, b.h);  
fclose(fp);  

-For dlib, a copy of "face_landmark_detection_ex.cpp" in "dlib/examples" was created with name "pastvision_landmark_detection_ex", 
the following line was added to "CMakeLists.txt" in "dlib/examples":  
"add_gui_example(pastvision_landmark_detection_ex)"  
And, the following lines were added to  "pastvision_landmark_detection_ex":  
	sprintf(logger_fname, "../../data/mouth/face_landmarks_detected.txt");  
	sprintf(shape_fname, "../../../../dlib/examples/build/martin_data/shape_predictor_68_face_landmarks.dat");  
	sprintf(image_fname, "../../data/mouth/my_rgb_shifted.jpg");  
	fout_logger.open(logger_fname);  
	if(!fout_logger){  
  		std::cout << "problem opening log file\n";  
  		return -1;  
	}  
. . .  
	fout_logger << dets.size() << "\n";  
. . .  
	if(shape.num_parts()==68){  
		fout_logger << dets[j].left() << "\n";  
		fout_logger << dets[j].top() << "\n";  
		fout_logger << dets[j].right() << "\n";  
		fout_logger << dets[j].bottom() << "\n";  

        	for (unsigned int k = 0; k < shape.num_parts(); ++k){  
			fout_logger << shape.part(k) << "\n";  
		}  
	}  
	fout_logger.close();
	fout_logger.clear();

-Recompile.  
For darknet, "cd darknet", "make"  
For dlib, "cd build", "cmake ..", "cmake --build . --config Release"  

-Make sure darknet can find its data files.  
(This can probably be done by editing various configuration files but the simplest solution can be to just copy the "darknet/cfg" and "darknet/data" folders into Pastvision's "scripts/objects" folder.)  

*Copy the pastvision_desktop folder onto the desktop (if the reader has not already done so)  
Preferably the pastvision_github, dlib, and darknet folders should all be within the same folder (e.g. the reader's home folder).
Otherwise the reader should adjust paths as needed.  

-----------------------------

4) Getting started  

(a) On the Raspberry Pi  
*Try recording some data (for example this could be of drinking some water):  
python save-thermal-and-rgb-data.py myTest  
from the pastvision_rpi folder where myTest is the base filename you would like to give (if a name like myTest is not provided as an argument, the program will create a name with the current timestamp).  
While running, the RGB and thermal feed and a clock should be visible (if not the reader should check that sudo ./raspberrypi_video works.)  
Stop recording by pressing Ctrl-C.  
The program will automatically save the RGB, thermal, and timestamp data in three files.  

NOTE: The step above is optional.  
If the reader wishes, they can also just use the default setup/data in the data folder on the desktop to conduct initial tests with the code without recording their own data.  

*Change the raw thermal data to some video files, for easy viewing/processing:   
python thermal-cam/changeRawThermalToVideos.py myTest

*Try watching the RGB/thermal videos (with VLC or such) to check that there are no problems. 
Then copy the video/time files into some convenient folder on the desktop.


(b) On the desktop
*Find the alignment (shift parameters) between the thermal and RGB data:  
python basic/findShiftParametersForThermalRGB.py  ../data/myTest  
This assumes the reader is calling the program from the src folder on the example data in the data folder.
The RGB and thermal streams as well as an overlayed image stream will be displayed which will help to manually vary the parameters in the python file.
For example if data of drinking water have been recorded, the reader can check that the thermal image of the cup and RGB image of the cup overlap nicely.
Add the parameters to "getAllDifferences_objects.py".

*Try assessing how long touches to objects can be perceived  
-The reader can find "ground truth" of when their touch started and ended (the frame number in the videos) by running the program below and pressing "f":  
python basic/findFrameNumbers.py   
-The reader can then feed these frame numbers to the program below to extract some frames at different time periods after the touch (5s, 10s, 15s, 30s, 60s, 90s):  
First edit getAllFrames_objects.py, and replace the folder and file names, and '45' below with a frame before touching and '135' below with a frame after touching.  
sys.argv=['../../data/objects/objects1', 'objects1_1', '45', '135', 'objects']  
Then run the program to extract:  
python objects/getAllFrames_objects.py  
-Process the extracted frames to find heat traces:  
python getAllDifferences_objects.py  
-Calculate statistics on the results  
python processTempResults_objects.py  

*Try assessing how long touches on a person's lips can be perceived   
The reader can follow the same process as above, just swapping out "objects" for "mouth" in folder and file names.  

Next the reader is encouraged to adapt the code for their own applications (and if they want, to show the author what they have built!). 
(Note: This code was written using the author's setup described above for research purposes; the author cannot help with getting it to work on the reader's system.)

----------------------------

5) Licenses

The reader is asked to please respect the separate licenses for each of the libraries which they use: dlib, darknet, OpenCV, etc.

For this author's code and dataset, the MIT license applies:

Copyright 2017 Martin Cooney 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated dataset and documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---------------------------------

6) Some References

[1] Martin Cooney, Josef Bigun. PastVision+: Thermo-visual Inference of Unobserved Recent Events. (Journal Article Submitted to Frontiers in Psychology).  
[2] Martin Cooney, Josef Bigun. PastVision: Exploring "Seeing" into the NEar as with Thermal Touch Sensing and Object Detection--For Robot Monitoring of Medicine Intake by Dementia Patients. SAIS. 2017.  
[3] Redmon, J., Divvala, S., Girshick, R., and Farhadi, A. (2016). You only look once: Unified, real-time object detection. In CVPR  
[4] King, D. E. (2009). Dlib-ml: A machine learning toolkit. Journal of Machine Learning Research 10, 1755–1758  

If the reader uses this code for their own research and would like to cite it, they can use reference [1] above.

--------------------------------

