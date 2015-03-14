import sys
sys.path.append("/afs/cs.stanford.edu/u/anenberg/scr/caffe/python/")
import caffe
import leveldb
import numpy as np
import Image
import numpy
import os
import pandas as pd
import random

import os, subprocess, pickle
num_workers = 12
worker_id = 2
GPU=1
tmp_optical_flow_images = ['./optical_flow_images5', './optical_flow_images6', './optical_flow_images7', \
                           './optical_flow_images8', './optical_flow_images9', './optical_flow_images10']

save_dirs = ['./optical_flow_images', './optical_flow_images2','./optical_flow_images3', './optical_flow_images4', \
             './optical_flow_images5', './optical_flow_images6', './optical_flow_images7', \
             './optical_flow_images8', './optical_flow_images9', './optical_flow_images10']

def opticalFlow(frame1, frame2, savePath, GPU=1):
    """
    computes the optical flow between frames 1 and 2.
    Saves the two optical flow images (dX and dY) at the
    target location: savePathdX and savePathdY
    
    GPU: the number of the GPU to run on 
    """
    #Returns the duration of the video in seconds.
    if not os.path.exists(frame1):
        print '%s does not exist!' % frame1
        return False
    if not os.path.exists(frame2):
        print '%s does not exist!' % frame2
        return False
    
    brox_optical_flow = '/afs/cs.stanford.edu/u/anenberg/scr/CS231N/code/OpenCV/brox_optical_flow'
    p = subprocess.Popen([brox_optical_flow, '-l', frame1, '-r', frame2, '-sa', \
                          savePath, '-GPU', str(GPU)], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = p.communicate()
    return True


def stack_images(image_filename_list):
    # datum.channels, datum.height, datum.width = arr.shape
    if len(np.array(Image.open(image_filename_list[0])).shape) == 2:
        is_need_reshape = True
    if is_need_reshape:
        sample_image_array = np.array(Image.open(image_filename_list[0]))
        reshape_size = list(sample_image_array.shape) + [1]
        return np.concatenate([np.array(Image.open(image_filename)).reshape(*reshape_size) for image_filename in image_filename_list], axis = 2).transpose(2,1,0)
    else:
        return np.concatenate([np.array(Image.open(image_filename)) for image_filename in image_filename_list], axis = 2).transpose(2,1,0)


#####UPDATE THIS
meta = {}
# change this
meta['train'] = ('./data/allFrames/lists/shuffle_shotdetect_sampled_5_train_list.txt', './data/allFrames/train/')
meta['test'] = ('./data/allFrames/lists/shuffle_shotdetect_sampled_5_test_list.txt', './data/allFrames/test/')

#meta['test'] = ('./data/allFrames/intermediate_lists/consecutive_5samples_10frames_test_list.txt', './data/allFrames/test/')

for directory in tmp_optical_flow_images:
    if not os.path.exists(directory):
        os.makedirs(directory)

def path_exists(save_dirs,video_name,number):
    """
    save_dests: list of directories where the file could be saved
    """
    for directory in save_dirs:
        savePath = os.path.join(os.path.join(directory,'%s_%s'%(video_name,number)))
        dX = savePath+"dX.jpg"
        dY = savePath+"dY.jpg"
        #Check if we have already previously created the dX/dY images.
        if os.path.exists(dX) and os.path.exists(dY):
            return True
    return False
    
for key in meta:
    # change this
    video_list, video_dir = meta[key]

    df = pd.read_csv(video_list, delimiter = ' ', header = None, names = ['name', 'class_id'])
    df['video'] = df.name.apply(lambda x: x.split('/')[0])
    df['frame1'] = df.name.apply(lambda x: x.split('/')[1])
    NUM_FRAMES_AHEAD = 30
    df['frame2'] = df.frame1.apply(lambda x: '%08d.jpg'%(int(x.split('.')[0]) + NUM_FRAMES_AHEAD))    
   

    successful_inserts = []
    
    counter = 0
    for proc_index, idx in enumerate(df.index): #df.ix gets row
        if (proc_index % num_workers) != worker_id:
            continue
        
        image_filename_list = [os.path.join(video_dir, df.ix[idx].video, name) for name in [df.ix[idx].frame1, df.ix[idx].frame2]]
        # create the optical flow files
        
        is_success = False
        #print "processing %s"%df.ix[idx].video
        #Check if we have already previously created the dX/dY images.
        if path_exists(save_dirs, df.ix[idx].video, df.ix[idx].frame1.split('.')[0]):
            is_success=True
            #print "found %s"%df.ix[idx].video
        else:
            
            save_dir = random.sample(tmp_optical_flow_images,1)[0]
            savePath = os.path.join(os.path.join(save_dir,'%s_%s'%(df.ix[idx].video, df.ix[idx].frame1.split('.')[0])))
            print "%d extracting to: %s"%(proc_index, savePath)
            is_success = opticalFlow(image_filename_list[0], image_filename_list[1], savePath = savePath, GPU=GPU)
            

