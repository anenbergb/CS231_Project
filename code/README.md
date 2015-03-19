List of each file in this directory and their purpose.

1. avconv.py
Python wrapper for the avconv utilities. Used to sample frames from videos or resize videos, etc.

2. extractFrames.py
Example usage:
python extractFrames.py $UCF_DIR $VALID_DIR $TEST_DIR -l $UCF240 $VALID240 $TEST240

Extracts the frames from the videos in the specified list.txt files (-l arguments)
and constructs ./Frame subdirectories in the data directories (parent of 
$UCF_DIR for example) $UCF_dir is path to the video files.

3. framesFromVid.py
Python version of Frames_From_UCF.ipynb
deprecated

4. makeNameIndexMap.py
Script to build a map from the video name to the associated class index.
Note, the 101 classes are 1 indexed. 0 class index is considered "background"

map = UCF_vidmap.pkl
map[0] = map from class index to list of videos with that index.
map[1] = map from individual video to list class index.

same format for the following maps.
VALID_vidmap.pkl
TEST_vidmap.pkl

usage:
python $SRC"makeNameIndexMap.py" $UCF_FULL $VALID_FULL $TEST_FULL -f \
./UCF_vidmap.pkl ./VALID_vidmap.pkl ./TEST_vidmap.pkl


5. makeUCF101_class_index_map.py
map = class_index.pkl: contains map from class name to index, and verse as well.
map[0] = map from class name to index. map[0]['applyeyemakeup'] = 1
map[1] = map from class index to the class


5. ShotDetection notebook / shotDetection.py
Using the ShotDetect software to detect the transitions scene transitions
https://github.com/johmathe/Shotdetect

This software yields a list of frames numbers which mark the boundaries between scenes.
shotError.txt: a nonsense file that is overwritten as shot detection is computed


6. OpenCV optical flow computation
./OpenCV
editing OpenCV Mat structures
http://docs.opencv.org/modules/core/doc/basic_structures.html

OpticalFlow ipython notebook: basic experiments computing optical flow using the opencv code

computeOpticalFlow.py script to compute the optical flow of UCF101 videos.




7. Tubelet investigation: findTubelets.py

Next, for each video split it into frames of .jpg and .ppm format.
- Extract frames and save then in a directory 'Frames' (here 'ppm' in .ppm format required by libsvx.v3.0).

1. For each dataSet, create a directory and populate it with sub-directoryies of the video_name
	ppm - (contains .ppm frames)
	Frames (contains .png frames)
	ppm_c200_sz500
	AC_IMEmap: initial GB segmentation
	svox (empty)
	tubelet.mat (destination of where to save the tubelet)

Tubelet extraction, for details refer to findTubelets.py

To construct the tubelets I had to specify a merging scheme:
I used options 5 and 13
5: C+T+S+F
13: M+C+T+S+F (I think)





Some calculations of size of video frame folders.
43M	./video_validation_0001001/Frames
197M	./video_validation_0001001/ppm
240M	./video_validation_0001001

Lower bound of 10 seconds would equate to 60.3Mb
So, upper bound of 240 second video would equate to 1.4 Gb of space.

For ucf_list.txt : 13,320 videos at approximately 10 seconds each. >> 784 Gb
For valid_list.txt : 779 videos >> 1090 Gb (upper bound)
For test_list.txt : 1345 >> 1883 Gb

First will experiment with 10 videos from ucf and 10 from valid_list

w-Flow
http://www.irisa.fr/texmex/people/jain/w-Flow/


 