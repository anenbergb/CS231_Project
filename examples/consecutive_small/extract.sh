#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

#$CAFFE/build/tools/extract_features.bin ./snapshots2/quick_shuffle_sampled_iter_12000.caffemodel ./quick_train_test.prototxt fc8_allFrames ./extracted/test_features/ 7840 lmdb GPU 2

#$CAFFE/build/tools/extract_features.bin ./snapshots2/quick_shuffle_sampled_100frames_iter_20000.caffemodel ./quick_train_test_100frames.prototxt fc8_allFrames ./extracted/features_100frames/ 156800 lmdb GPU 2

$CAFFE/build/tools/extract_features.bin ../snapshots2/UCF_iter_40000.caffemodel ./quick_train_test.prototxt fc8_allFrames ../extracted/features_UCF/ 3755 lmdb GPU 2