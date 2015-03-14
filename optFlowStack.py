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
import ThreadPool



num_workers = 10
worker_id = 0
GPU=1

stacked=5

opt_flow_dir = "./optical_flow_dir"
opt_flow_sub_dirs = [str(i) for i in range(0,60)]
save_dirs = [os.path.join(opt_flow_dir,x) for x in opt_flow_sub_dirs]

if not os.path.exists(opt_flow_dir):
    os.makedirs(opt_flow_dir)
for directory in save_dirs:
    os.makedirs(directory)
    


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


#####UPDATE THIS
meta = {}
# change this
meta['train'] = ('./data/allFrames/lists/shuffle_stacked_5_shotdetect_sampled_t1_5_train_list.txt', './data/allFrames/train/')
meta['test'] = ('./data/allFrames/lists/shuffle_stacked_5_shotdetect_sampled_t1_5_test_list.txt', './data/allFrames/test/')

#Multi-threaded optical flow extraction.
pool = ThreadPool.ThreadPool(numWorkers)




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



pool.wait_completion()

def 
pairs = []
for i in xrange(0,len(A),3):
    for j in xrange(1,3):
        pairs.append((A[i+j-1],A[i+j]))
print pairs
B = [True if i%3==0 else False for i in xrange(len(A)) ]

df = pd.DataFrame(zip(peaks_full[:-1], peaks_full[1:]), columns = ['left', 'right'])

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
    for idx in df.index: #df.ix gets row
        image_filename_list = [os.path.join(video_dir, df.ix[idx].video, name) for name in [df.ix[idx].frame1, df.ix[idx].frame2]]
        # create the optical flow files
        
        is_success = False
        #Check if we have already previously created the dX/dY images.
        if path_exists(save_dirs, df.ix[idx].video, df.ix[idx].frame1.split('.')[0]):
            is_success=True
            #print "found %s"%df.ix[idx].video
        else:
            
            save_dir = random.sample(tmp_optical_flow_images,1)[0]
            savePath = os.path.join(os.path.join(save_dir,'%s_%s'%(df.ix[idx].video, df.ix[idx].frame1.split('.')[0])))
            print "%d extracting to: %s"%(proc_index, savePath)
            pool.add_task(processVideo,line,FISHER_DIR,gmm_list)

            is_success = opticalFlow(image_filename_list[0], image_filename_list[1], savePath = savePath, GPU=GPU)
            

