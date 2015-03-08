#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

$CAFFE/build/tools/extract_features.bin ./quick_shuffle_sampled1_iter_10000.caffemodel ./quick_train_test.prototxt ip2 ./extracted/features8/ 30 lmdb