import sys
sys.path.append("/afs/cs.stanford.edu/u/anenberg/scr/caffe/python/")
import caffe
import leveldb
import numpy as np
import Image
import numpy
import os
import pandas as pd

def stack_images(image_filename_list):
    # datum.channels, datum.height, datum.width = arr.shape
    return np.concatenate([np.array(Image.open(image_filename)) for image_filename in image_filename_list], axis = 2).transpose(2,1,0)

meta = {}
# change this
#meta['train'] = ('./data/allFrames/intermediate_lists/consecutive_5samples_10frames_train_list.txt', './data/allFrames/train/')
meta['test'] = ('./data/allFrames/intermediate_lists/consecutive_5samples_10frames_test_list.txt', './data/allFrames/test/')


for key in meta:
    # change this
    video_list, video_dir = meta[key]

    df = pd.read_csv(video_list, delimiter = ' ', header = None, names = ['name', 'class_id'])
    df['video'] = df.name.apply(lambda x: x.split('/')[0])
    df['frame'] = df.name.apply(lambda x: x.split('/')[1])
    FRAMES_PER_GROUP = 10


    # change this
    db_path = os.path.join('./examples/consecutive/leveldb/', key)
    print db_path
    db = leveldb.LevelDB(db_path)

    for group_id, i in enumerate(range(0, len(df), FRAMES_PER_GROUP)):
        image_filename_list = [os.path.join(video_dir, name) for name in df.name.values[i:i+FRAMES_PER_GROUP]]
        stacked_image = stack_images(image_filename_list)
        labels = list(set(df.class_id.values[i:i+FRAMES_PER_GROUP]))
        assert len(labels) == 1
        db.Put('%08d'%group_id, caffe.io.array_to_datum(stacked_image, label=labels[0]).SerializeToString())
        if group_id % 50 == 0:
            print 'Done with %d'%group_id

    
    
    
    