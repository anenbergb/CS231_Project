UCF_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/videos/"
VALID_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/videos/"
BACK_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Background/videos/"
TEST_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/videos/"

UCF_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/train_set.txt"
VALID_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/validation_primaryclass.txt"
BACK_FULL=""
TEST_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/test_primaryclass.txt"


#Lets assume that we have already generated the data lists 
#ucf_list.txt
#valid_list.txt
#test_list.txt
SRC="../../code/"

UCF240="./ucf_list.txt"
VALID240="./valid_list.txt"
TEST240="./test_list.txt"

#python $SRC"extractFrames.py" $UCF_DIR $VALID_DIR $TEST_DIR -l $UCF240 $VALID240 $TEST240

TrainFrames="/afs/cs.stanford.edu/u/anenberg/scr/CS231N/data/allFrames/Train"
UCF_Frames="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/Frames/"

for d in $UCF_Frames
do
	for f in $d
	do
		for cp $f 
	done
done
 
