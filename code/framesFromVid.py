import avconv
import numpy as np
import os, sys


#The video data can come from a number of different directories.
UCF_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/videos/"
VALID_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/videos/"
BACK_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Background/videos/"
TEST_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/videos/"


#Full data sets
UCF_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/train_set.txt"
VALID_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/validation_primaryclass.txt"
BACK_FULL=""
TEST_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/test_primaryclass.txt"

#The training and testing cuts.
UCF_train1="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/ucfTrainTestlist/trainlist01.txt"
UCF_test1="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/ucfTrainTestlist/testlist01.txt"


UCF_firstFrame_10_train = "/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/firstFrame_10_train"
UCF_firstFrame_10_val = "/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/firstFrame_10_val"

UCF_firstFrame_train = "/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/firstFrame_train"
UCF_firstFrame_val = "/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/firstFrame_val"


def extract_frames(vidlist,vidDir,outputDir, outputList):
    """
    vidList: python list of tuples (videos,class_id)
    vidDir: directory of videos
    outputList: .txt file with format [videoName classID]
    
    """
    with open(outputList, 'w+') as f:
        for vid, class_id in vidlist:
            videoName = os.path.join(vidDir,vid)
            frameBase = vid.split('.')[0]+".jpeg"
            frameName = os.path.join(outputDir, frameBase)
            #avconv.extract_frame(videoName,frameName)
            f.write('%s %s\n'%(frameBase, class_id-1))

def extract_by_class(filename, N = 10):
    import csv
    import collections
    d = collections.defaultdict(list)
    with open(filename, 'r+') as f:
        data = csv.reader(f, delimiter=' ')
        for row in data:
            class_id = int(row[1])
            video_filename = row[0]
            d[class_id].append(video_filename)
            
    return {k: v if N==-1 else v[:N] for k, v in d.items()}

# example usage:
sampled_ucf_full = extract_by_class(UCF_FULL, -1)
num_train_percent = .7
sampled_ucf_train = {k:v[:int(num_train_percent*len(v))] for k,v in sampled_ucf_full.items()} 
sampled_ucf_test = {k:v[int(num_train_percent*len(v)):] for k,v in sampled_ucf_full.items()} 

def example_dict_to_flat_list(example_dict):
    ucf_filename_class = []
    for k, v in example_dict.items():
        class_id = k
        for video_filename in v:
            ucf_filename_class.append((video_filename, class_id))
    return ucf_filename_class

ucf_filename_class_train = example_dict_to_flat_list(sampled_ucf_train)
ucf_filename_class_test = example_dict_to_flat_list(sampled_ucf_test)

extract_frames(ucf_filename_class_train,UCF_DIR,UCF_firstFrame_train, '../data/UCFff/UCF_train.txt')
extract_frames(ucf_filename_class_test,UCF_DIR,UCF_firstFrame_val, '../data/UCFff/UCF_test.txt')

import pickle
UCF_firstFrames = '../data/UCFff/UCF_firstFrames.pkl';
with open(UCF_firstFrames, 'w+') as f:
    pickle.dump(sampled_ucf_full,f)
    
