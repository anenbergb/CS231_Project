#!/bin/bash

CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

for count in {6000..40000..1000} 
    do echo "working on $count"
    $CAFFE/build/tools/extract_features.bin ./snapshots/fine_iter_$count.caffemodel ./quick_train_test_TEST.prototxt fc8_allFrames ./extracted/fine_test_features_$count/ 7765 lmdb GPU 1
done
#$CAFFE/build/tools/extract_features.bin ./snapshots/run3_iter_40000.caffemodel ./quick_train_test.prototxt fc8_allFrames ./extracted/features1/ 7765 lmdb GPU 2