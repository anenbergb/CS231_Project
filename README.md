# CS231N_Project

Data:

(Action Recognition)
1. Training: entire UCF action data set. It consists of 101 human action categories with 13,320 videos in total. Each category has more than 100 video clips, all of which are temporally trimmed.
2. Validation data: There are 1,000 videos in total provided for 101 action classes as validation data (each class has exactly 10 videos). In general, there is one primary action class shown in each video; however, some videos may include one or more instances from other action classes.
3. Background data: 2,500 videos, which are verified to make sure they do not include an instance of any of the 101 action classes, are provided as background. Each video is relevant to one of the action classes. For instance, the background videos related to the ac-tion class “Basketball Dunk” may show the basketball court when the game is not being played.
4. 1,574 temporally untrimmed videos are provided as the test data. Some videos may contain one or multiple instances from one or multiple action classes, and some videos may not include any actions from the 101 classes. A significant portion of the video may not include any particular action, and multiple instances may occur at differnet time stamps within the video.

(Action Detection)

1. Training: A subset of UCF101 action dataset with 20 action classes is used for training. The remaining action classes in UCF101 may also be used for training, if desired.
2. 200 videos from 20 action classes are provided as the validation set. These videos have the same properties as the validation videos in the recognition task. The validation set could be added to the training data, if desired.
3. Background: same as before.
4. Same format as validation.

Result format:
(Action Recognition)
[test_video_name_1] [confidence_score_class_1] [confidence_score_class_2] … [confidence_score_class_m]

for each of the m=101 test classes.

(Action Detection)
[video_name] [starting_time] [ending_time] [class_label] [confidence_score]

A detector can fire multiple times in a test video (there may be multiple rows with the same video name)


Project goal:
The project hopes to achieve two goals: Action Recognition and Temporal Action Detection.

Use a CNN trained on the training and validation data to output a real valued score indicating the confidence of the precense of each action class in a test video.

Project approach:

Step 1: Train a CNN on only the training data set (UCF action data set) to perform action recognition on the UCF data set. First iteration of this model will be trained using only the first frame from each video.

Step 2: Train CNN on the training and validation data sets using only the first frame from each video and test on a held out portion of the validation data set.

Step 3: Implement a more elaborate CNN architecture, similar to two-stream CNN architecture proposed by Karen Simonyan and Andrew Zisserman. Report performance using the spatial stream, and then the combined performance with the temporal stream.

Step 4: Experiment with a new CNN trained on single video frames that have been identified using tubelet preprocessing. For each video, the tubelet extraction yields K tubelets, which are sequences of bounding boxes over a set range of frames. Each tubelet proposes a candidate spatio-temporal localization of an action. The most promising tubelets inform us on where to sample the frames from the video.


