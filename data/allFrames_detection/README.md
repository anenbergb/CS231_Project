
The data in this directory is for the localization task.
* All the frames belonging to each video are assigned a label.

* For the detection task, there are only 20 action classes.
* All other classes are treated as background.

* The "data" is located in the ../allFrames/Train and ../allFrames/Test directory
* Every video in the Train directory contains frames. Each of the frames
* is assigned a label based on its time stamp.

*This directory only prepares the data lists with the appropriate class labels to the frames.

* At the data server there exists a subdirectory "annotation" that contains 
* .txt files with 
(original password: THUMOS14_REGISTERED)

temporal locations of instances of one class. Each row denotes 
one instance with the following format:

[video_name starting_time ending_time]

The following is the list of 20 action classes for which temporal 
annotation is available:

7 BaseballPitch
9 BasketballDunk
12 Billiards
21 CleanAndJerk
22 CliffDiving
23 CricketBowling
24 CricketShot
26 Diving
31 FrisbeeCatch
33 GolfSwing
36 HammerThrow
40 HighJump
45 JavelinThrow
51 LongJump
68 PoleVault
79 Shotput
85 SoccerPenalty
92 TennisSwing
93 ThrowDiscus
97 VolleyballSpiking

Goal of the detection task:

Output a file with rows of the following format:

[video_name] [starting_time] [ending_time] [class_label] [confidence_score]
Each row has 5 fields representing a single detection
A detector can fire multiple times in a test video (reported using multiple rows in the submission file)

##########################################################################
##########################################################################
Labeling convention:
0 Background
1 BaseballPitch
2 BasketballDunk
3 Billiards
4 CleanAndJerk
5 CliffDiving
6 CricketBowling
7 CricketShot
8 Diving
9 FrisbeeCatch
10 GolfSwing
11 HammerThrow
12 HighJump
13 JavelinThrow
14 LongJump
15 PoleVault
16 Shotput
17 SoccerPenalty
18 TennisSwing
19 ThrowDiscus
20 VolleyballSpiking


* Re-labeled the classes specifically for the detection task.
* class 0 corresponds to the background which is any "unlabled" frame and any video
  not from one of the 20 classes.


##########################################################################
##########################################################################

Description of the files in this directory

#map from video name to UCF101 index.
VALID_vidmap
TEST_vidmap



1. prepareData.sh
    Script used to execute the codes.

2. makeDetectionIndexMap.py
	python makeDetectionIndexMap.py

	Script to define the mapping between class name and class id.
	Saves the mapping in a pkl file: class_index.pkl

	map[0] = map from class name to index. map[0]['VolleyballSpiking'] = 20
	map[1] = map from class index to the class
	map[2] = map from UCF_id to class_id

detection_class_index.pkl

2. makeVid_class_index_map.py
	Script that uses the temporal annotations to construct a map:
	map[videoname][time_stamp] = class_id
	time stamp is a float in 0.1 precision.

["./VALID_TSmap.pkl","./TEST_TSmap.pkl"]




