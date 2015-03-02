In this project we will train a CNN trained on the individual video frames.




1. .pkl files
Note, the 101 classes are 0 index. So -1 from the original UCF 101 classes.
map = class_index.pkl: contains map from class name to index, and verse as well.
map[0] = map from class name to index. map[0]['applyeyemakeup'] = 0
map[1] = map from class index to the class

map = UCF_vidmap.pkl
map[0] = map from class index to list of videos with that index.
map[1] = map from individual video to list class index.

same format for the following maps.
VALID_vidmap.pkl
TEST_vidmap.pkl


2. list files


Decide to discard all
videos of length longer than 4 minutes. (240 seconds)

The video lists are in the current directory:

ucf_list.txt
valid_list.txt
test_list.txt



python $SRC"extractFrames.py" $UCF_DIR $VALID_DIR $TEST_DIR -l $UCF240 $VALID240 $TEST240




Notes:

make tools
1. Modifying Caffe in order to read in files to lmdb listed in a directory. Using Boost

2. Had to modify the makefile at line 319
-lboost_filesystem -lboost_system

3. Moified the io.hpp file to add the ReadImagesToDatum function from the io.cpp


NEED to modifiy ReadImagesToDatum in io.cpp in order to concatenate the full file name.
