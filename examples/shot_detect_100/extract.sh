#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

#$CAFFE/build/tools/extract_features.bin ./snapshots2/quick_shuffle_sampled_iter_12000.caffemodel ./quick_train_test.prototxt fc8_allFrames ./extracted/test_features/ 7840 lmdb GPU 2

#$CAFFE/build/tools/extract_features.bin ./snapshots2/quick_shuffle_sampled_100frames_iter_20000.caffemodel ./quick_train_test_100frames.prototxt fc8_allFrames ./extracted/features_100frames/ 156800 lmdb GPU 2

$CAFFE/build/tools/extract_features.bin ./snapshots/run3_iter_10000.caffemodel ./quick_train_test.prototxt fc8_allFrames ./extracted/features1/ 155293 lmdb GPU 1