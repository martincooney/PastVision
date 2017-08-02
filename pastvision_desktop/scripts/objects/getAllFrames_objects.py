#!/usr/bin/env python

#Copyright 2017 Martin Cooney
#This file is subject to the terms and conditions defined in file 'Readme.md', which is part of this source code package.

import sys

print ""
print "----------------------------------------------------------------------------"
print "= Extract frames at various times for a person touching objects (MAY 2017) ="
print "----------------------------------------------------------------------------"
print ""

sys.argv=['../../data/objects/objects1', 'objects1_1', '45', '135', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")

#uncomment the lines below to process the whole dataset
'''
sys.argv=['../../data/objects/objects1', 'objects1_2', '45', '1258', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects1', 'objects1_3', '45', '2276', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects1', 'objects1_4', '45', '3322', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects1', 'objects1_5', '45', '4347', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")

sys.argv=['../../data/objects/objects2', 'objects2_1', '36', '106', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects2', 'objects2_2', '36', '1138', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects2', 'objects2_3', '36', '2179', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects2', 'objects2_4', '36', '3212', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects2', 'objects2_5', '36', '4241', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")

sys.argv=['../../data/objects/objects3', 'objects3_1', '19', '115', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects3', 'objects3_2', '19', '1146', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects3', 'objects3_3', '19', '2169', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects3', 'objects3_4', '19', '3183', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects3', 'objects3_5', '19', '4205', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")

sys.argv=['../../data/objects/objects4', 'objects4_1', '110', '211', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects4', 'objects4_2', '110', '1247', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects4', 'objects4_3', '110', '2271', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects4', 'objects4_4', '110', '3301', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
sys.argv=['../../data/objects/objects4', 'objects4_5', '110', '4322', 'objects']
execfile("../basic/getFramesFromVideoAtTimeIntervals.py")
'''

