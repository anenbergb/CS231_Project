import sys
sys.path.append("/afs/cs.stanford.edu/u/anenberg/scr/caffe/python/")
import caffe
import leveldb
import numpy as np
import Image
import numpy
import os
import pandas as pd


import os, subprocess, pickle

save_dirs = ['./optical_flow_images', './optical_flow_images2','./optical_flow_images3', './optical_flow_images4', \
             './optical_flow_images5', './optical_flow_images6', './optical_flow_images7', \
             './optical_flow_images8', './optical_flow_images9', './optical_flow_images10']



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
            return (True, dX, dY)
    return (False, None, None)


    
for key in meta:
    # change this
    video_list, video_dir = meta[key]

    df = pd.read_csv(video_list, delimiter = ' ', header = None, names = ['name', 'class_id'])
    df['video'] = df.name.apply(lambda x: x.split('/')[0])
    df['frame1'] = df.name.apply(lambda x: x.split('/')[1])
    NUM_FRAMES_AHEAD = 30
    df['frame2'] = df.frame1.apply(lambda x: '%08d.jpg'%(int(x.split('.')[0]) + NUM_FRAMES_AHEAD))    
   

    db_path = os.path.join('./examples/shot_detect_optical_flow_5/leveldb/', key)
    print db_path
    db = leveldb.LevelDB(db_path)
    
       
    
    counter = 0
    for idx in df.index: #df.ix gets row
        image_filename_list = [os.path.join(video_dir, df.ix[idx].video, name) for name in [df.ix[idx].frame1, df.ix[idx].frame2]]
        

        #print "processing %s"%df.ix[idx].video
        #Check if we have already previously created the dX/dY images.
        is_success, dX, dY = path_exists(save_dirs, df.ix[idx].video, df.ix[idx].frame1.split('.')[0])
        if is_success:
            optical_flow_filename_list = [dX,dY] 
            stacked_image = stack_images(optical_flow_filename_list)
            label = df.ix[idx].class_id
        
            db.Put('%08d'%counter, caffe.io.array_to_datum(stacked_image, label=label).SerializeToString())
            counter += 1
            if idx % 50 == 0:
                print 'Done with %d'%idx




