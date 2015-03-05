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



Simple bash loop:
for d in $UCF_Frames
do
	for f in $d
	do
		for cp $f 
	done
done
 