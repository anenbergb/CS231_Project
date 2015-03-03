UCF_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/videos/"
VALID_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/videos/"
BACK_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Background/videos/"
TEST_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/videos/"

UCF_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/train_set.txt"
VALID_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/validation_primaryclass.txt"
BACK_FULL=""
TEST_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/test_primaryclass.txt"


#Lets assume that we have already generated the data lists 

SRC="../../code/"

CLASS_INDEX="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/ucfTrainTestlist/classInd.txt"
CLASS_INDEX_OUT="./class_index"

python $SRC"makeUCF101_class_index_map.py" $CLASS_INDEX $CLASS_INDEX_OUT -p


UCF_FRAMES="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/Frames/"
VALID_FRAMES="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/Frames/"
TEST_FRAMES="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/Frames/"

thisTrainDir="./Train"
thisTestDir="./Test"

#rm -rf $thisTrainDir
#python createDataDirs.py $UCF_FRAMES $VALID_FRAMES $TEST_FRAMES -l $thisTrainDir $thisTrainDir $thisTestDir



thisTrainList="./Train_list.txt"
thisTestList="./Test_list.txt"

#python makeLists.py $thisTrainDir $thisTestDir -l $thisTrainList $thisTestList

