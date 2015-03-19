Structure of the Data Set:

Here we will elaborate on how the data set is stored.

1. Data is stored at /afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/
Subdirectories:
	a. Training
	b. Validation
	c. Testing
	d. Background

	In each subdirectory, there exists the following subdirectories.

	1. videos
		.avi or .mp4 videos downloaded from the THUMOS2014 challenge website

	2. Frames
		For each of the videos in the ../videos directory, there is a corresponding directory
		here. These directories are populated with the individual video frames.
		These frames were extracted using the python script "extractFrames.py" in the src/code directory.
		Frame naming convention:


2. CS231N/data directory
	1. allFrames
		Each project contains a /train and a /test directory.
		Each directory contains symbolic links to the data stored at on the server.
		e.g.
		Train/v_ApplyEyeMakeup_g08_c01 is a symbolic link to 
			/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/Frames/v_ApplyEyeMakeup_g08_c01
	2. lists.
		List of image to id with the following format.
		[video_name/%08d] [class_id]
		






Caffe:
	* Caffe loads the data into a lmdb data base.
	Requires:
		1. data_list.txt: a list of image to photos.
			[image_name] [class_id]
		2. Path to data directory. In this data directory, Caffe expects to see the images from the above list.

	Images are saved in lmdb in the following format:
	 	key: 00000015_v_ApplyEyeMakeup_g08_c01/00001.jpg
	 	Where they "%08d" is the line in the data_list.txt file of this entry named v_ApplyEyeMakeup_g08_c01/00001.jpg
