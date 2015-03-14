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
#meta['test'] = ('./data/allFrames/lists/shuffle_shotdetect_sampled_5_test_list.txt', './data/allFrames/test/')

#meta['test'] = ('./data/allFrames/intermediate_lists/consecutive_5samples_10frames_test_list.txt', './data/allFrames/test/')


tmp_optical_flow_images = './optical_flow_images'
if not os.path.exists(tmp_optical_flow_images):
    os.makedirs(tmp_optical_flow_images)

    
for key in meta:
    # change this
    video_list, video_dir = meta[key]

    df = pd.read_csv(video_list, delimiter = ' ', header = None, names = ['name', 'class_id'])
    df['video'] = df.name.apply(lambda x: x.split('/')[0])
    df['frame1'] = df.name.apply(lambda x: x.split('/')[1])
    NUM_FRAMES_AHEAD = 30
    df['frame2'] = df.frame1.apply(lambda x: '%08d.jpg'%(int(x.split('.')[0]) + NUM_FRAMES_AHEAD))    
   
    """
    db_path = os.path.join('./examples/shot_detect_optical_flow/leveldb1/', key)
    print db_path
    db = leveldb.LevelDB(db_path)
    """
    
    successful_inserts = []
    
    counter = 0
    for idx in df.index[:20]: #df.ix gets row
        image_filename_list = [os.path.join(video_dir, df.ix[idx].video, name) for name in [df.ix[idx].frame1, df.ix[idx].frame2]]
        # create the optical flow files
        
        savePath = os.path.join(os.path.join(tmp_optical_flow_images,'%s_%s'%(df.ix[idx].video, df.ix[idx].frame1.split('.')[0])))
        dX = savePath+"dX.jpg"
        dY = savePath+"dY.jpg"
        is_success = False
        print "processing %s"%df.ix[idx].video
        #Check if we have already previously created the dX/dY images.
        if os.path.exists(dX) and os.path.exists(dY):
            is_success=True
            print "found %s"%df.ix[idx].video
        else:
            is_success = opticalFlow(image_filename_list[0], image_filename_list[1], savePath = savePath)
            print "not found %s"%df.ix[idx].video

            
        """
        if is_success:
            try:
                optical_flow_filename_list = [dX,dY] 
                stacked_image = stack_images(optical_flow_filename_list)
                label = df.ix[idx].class_id
        
                db.Put('%08d'%counter, caffe.io.array_to_datum(stacked_image, label=label).SerializeToString())
                counter += 1
                successful_inserts.append((image_filename_list[0], label))
                if idx % 50 == 0:
                    print 'Done with %d'%idx
            except:
                pass
    pd.DataFrame(successful_inserts).to_csv('successful_inserts.csv', delimiter=' ', header=None)
        """




