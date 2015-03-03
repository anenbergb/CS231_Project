
The data in this directory is for the recognition task.
* Every input video is assigned a primary class label.
* All the frames belonging to this video are also assigned this same class label.

Goal of recognition task:
* For each ./Test video, report the score/confidence across all possible
class labels.
[test_video_name_1] [confidence_score_class_1] [confidence_score_class_2] … [confidence_score_class_m]


##########################################################################
##########################################################################

Description of the files in this directory


1. prepareData.sh
    Script used to execute the codes.

2. createDataDirs.py
    Script to populate the Train and Test directories with the symbolic links to the actual
    data directories (the video directories)

3. makeLists.py
    Constructs the data lists of image to id with the following format.
    [video_name/%08d] [class_id]
    stores them in:
    "./Train_list.txt"
    "./Test_list.txt"


##########################################################################
Temporary / Quick Test files

1. checkingCaffe_makeList.py
    Quick file used to construct the checkingCaffe_list.txt file. 