
The data in this directory is for the localization task.
* All the frames belonging to each video are assigned a label.

* For the detection task, there are only 20 action classes.
* All other classes are treated as background.

* Every video in the Train directory contains frames. Each of the frames
* is assigned a label based on its time stamp.

* At the data server there exists a subdirectory "annotation" that contains 
* .txt files with 

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

Description of the files in this directory


1. prepareData.sh
    Script used to execute the codes.

2. makeVid_class_index_map.py
	Script that uses the temporal annotations to construct a map:
	map[videoname][time_stamp] = class_id





