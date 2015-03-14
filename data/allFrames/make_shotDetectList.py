import os
import numpy as np
import subprocess, os, pickle, csv, random

##data directories
train_dir = '/afs/cs.stanford.edu/u/anenberg/scr/CS231N/data/allFrames/train'
test_dir = '/afs/cs.stanford.edu/u/anenberg/scr/CS231N/data/allFrames/test'

#location to save the output list.
experiment_dir = '/afs/cs.stanford.edu/u/anenberg/scr/CS231N/data/allFrames/lists'
#folder with .pkl lists of frames number. Each frame number is the beginning of a scene.
sceneTransitions = "/afs/cs.stanford.edu/u/anenberg/scr/CS231N/data/allFrames/sceneTransitions/"

num_samples = 100
num_consecutive_frames = 10

##HARD coded in the dictionaries from the video name to the class index.
UCF_vidmap_PATH = "./UCF_vidmap.pkl"
VALID_vidmap_PATH = "./VALID_vidmap.pkl"
TEST_vidmap_PATH = "./TEST_vidmap.pkl"
UCF_vidmap = pickle.load( open(UCF_vidmap_PATH, "rb" ) )
VALID_vidmap = pickle.load( open(VALID_vidmap_PATH, "rb" ) )
TEST_vidmap = pickle.load( open(TEST_vidmap_PATH, "rb" ) )


# Train_map: map from individual video name to class label for
# UCF and Validation videos.
# Test_map: same thing, but for Test videos.
Train_map = UCF_vidmap[1]
Train_map.update(VALID_vidmap[1])
Test_map = TEST_vidmap[1]

VID_MAPS = [Train_map,Test_map]

def sampleRange(scene_list, maxFrame, threshold=150):
    """
    scene_list: list containing the frame numbers that denote the beginning of the scene.
    threshold: minimum number of frames in a scene to consider it relevant. Assume that longer
    scenes are more likely to contain frames that contain the activity of interest.
    maxFrame: the maximum index frame in video.
    
    returns: 
        1. list of integers which are the valid frames.
        2. list of ranges [(min, max), (min, max)..]
    
    """
    
    #first sort the scene_list by duration.
    
    valid_frames = []
    ranges = []
    end = maxFrame
    for i in reversed(scene_list):
        scene_duration = abs(end-i)
        if scene_duration > threshold:
            valid_frames.extend(range(i,end+1))
            ranges.append((i,end))
        end = i - 1
    random.shuffle(valid_frames)
    return (valid_frames,ranges)

def maxSceneDuration(scene_list,maxFrame):
    end = maxFrame
    longest = 0
    for i in reversed(scene_list):
        duration = abs(end-i)
        end = i - 1
        if duration > longest:
            longest = duration
    return longest

def KLsamples(distribution,k,l):
    """
    k: number of samples to draw
    l: length of consecutive integers to list.
    
    returns a length k list of lists of length l. 
    """
    num_bins = len(distribution)/l
    bins = range(num_bins)
    k_to_sample = min(num_bins,k)
    sampled_bins = random.sample(bins,k_to_sample)
    
    returnLists = []
    for b in sampled_bins:
        segment = distribution[b*l:(b+1)*l]
        assert len(segment) == l
        returnLists.append(segment)
    return returnLists
def KLsamples_invalidList(distribution,k,l, ranges):
    """
    k: number of samples to draw
    l: length of consecutive integers to list.
    ranges: list of tuples [ (min, max), (min, max)]
            segments can only be a member of a single range.
    
    returns a length k list of lists of length l. 
    """
        
    def isInSingleRange(segment, ranges):
        """
        segment: list of consecutive integers increasing integers.
        Elements in the segment list can only belong to a single range.
        """
        def intInRange(num, theRange):
            #theRange is a tuple: (lower_bound, upper_bound)
            return num in xrange(*theRange)
        def inWhichRange(num,ranges):
            for i in xrange(len(ranges)):
                if intInRange(num,ranges[i]):
                    return i
            return -1
        #checks if the min and max of the segment are in the same range.
        return inWhichRange(segment[0],ranges) == inWhichRange(segment[-1],ranges)

    
    num_bins = len(distribution)/l
    bins = range(num_bins)
    
    
    returnLists = []
    seen = set()
    while len(returnLists) < k:
        #print '(dist, bins, k, returnList)', len(distribution), len(bins),k, len(returnLists)
        #This is the case where there is no way to select the k sets of length l
        if len(bins) < k-len(returnLists): 
            return False
        sampled_bins = random.sample(bins,k-len(returnLists))
        for b in sampled_bins:
            segment = distribution[b*l:(b+1)*l]
            assert len(segment) == l
            if isInSingleRange(segment,ranges):
                returnLists.append(segment)
            del bins[bins.index(b)]
    assert len(returnLists) == k
    return returnLists

def makeListConsecutiveFrames(data_dir, save_list, vid_map, num_samples, num_frames):

    """
    data_dir: directory of the data. such as ./train or ./test
    save_list: full path to the list we want to output.
    vid_map: dictionary between the videoname and class id.
    
    num_samples: The number of sets to frames to sample from the videos.
    num_frames: The number of frames per set.
    """
    def isUCFvideo(videoname):
        return videoname[:2] == 'v_'
    
    def write_frames(segments, out_writer):
        for segment in segments:
            for num in segment:
                frame_name = '%s/%08d.jpg' % (d,num) #from 14 >> videoname/00000014.jpg
                frame_index = vid_map[d]
                out_writer.writerow([frame_name, frame_index])

    with open(save_list,'wb') as f:
        out = csv.writer(f, delimiter=' ')
        videos = os.listdir(data_dir)
        random.shuffle(videos)
        for d in videos: #d is the video name.
            video_name_path = os.path.join(data_dir,d)
            
            #Returns the frames that are in the video directory as a list of integers.
            frameNums = [int(frame.split('.')[0]) for frame in os.listdir(video_name_path) \
                         if len(frame.split('.')) > 1 and frame.split('.')[1] != "pkl"]
        
            if isUCFvideo(d): #then we don't want to use the scene information.
                sets_of_frames = KLsamples(frameNums,num_samples,num_frames)
                write_frames(sets_of_frames,out)
                
            else: #Then we want to use the scene information.
                frame_map_path = os.path.join(video_name_path, "time_stamp_map.pkl")
                if os.path.exists(frame_map_path):
                    frame_map = pickle.load( open(frame_map_path, 'rb'))
                    maxFrame = max(frame_map.keys())
                    
                    scene_list_path = os.path.join(sceneTransitions, d+".pkl")
                    if os.path.exists(scene_list_path): #make sure the scene transition list exists
                        scene_list = pickle.load( open(scene_list_path, "rb" ) )
                        #if the scene list is empty, then entire video was beneath the threshold.
                        if len(scene_list) > 0:
                            #list of possible frames to sample from.
                            #Hueristic to guess the number of frames in a scene threshold above which
                            # we consider a valid scene.
                            for divisor in range(2,50):
                                threshold = maxSceneDuration(scene_list, maxFrame)/divisor
                                validFrames, ranges = sampleRange(scene_list, maxFrame, threshold=threshold)
                                if len(validFrames) > num_samples*num_frames: #minimum number of frames needed for this requested sample
                                    break
                            
                            frames_to_sample_from = list(set(validFrames).intersection(frameNums))
                            frames_to_sample_from = sorted(frames_to_sample_from, reverse=False)
                            #print "valid frames %d, In directory %d, intersection %d, scene_list_length %d, threshold %d" % \
                            #(len(validFrames),len(frameNums),len(frames_to_sample_from), len(scene_list), threshold)
                            
                            sets_of_frames = KLsamples_invalidList(frames_to_sample_from,num_samples,num_frames, ranges)
                            if sets_of_frames: #Check to make sure this isn't false. If so, then skip this video.
                                write_frames(sets_of_frames,out)
                        else: #entire video was beneath the threshold.
                            sets_of_frames = KLsamples(frameNums,num_samples,num_frames)
                            write_frames(sets_of_frames,out)

                            
                            
#Script like part                            
num_samples=5
num_frames = 10
intermediate_lists = "./intermediate_lists/"


#Make Train data set.
#naming convention: "consecutive_5samples_10frames
train_consecutive_list = "consecutive_%dsamples_%dframes_train_list.txt" % (num_samples,num_frames)
train_consecutive_list_path = os.path.join(intermediate_lists, train_consecutive_list)
makeListConsecutiveFrames(train_dir,train_consecutive_list_path,Train_map,num_samples,num_frames)



#make Test data set.

##naming convention: "consecutive_5samples_10frames
#test_consecutive_list = "consecutive_%dsamples_%dframes_test_list.txt" % (num_samples,num_frames)
#test_consecutive_list_path = os.path.join(intermediate_lists, test_consecutive_list)
#makeListConsecutiveFrames(test_dir,test_consecutive_list_path,Test_map,num_samples,num_frames)