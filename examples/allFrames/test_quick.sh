#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

$CAFFE/build/tools/caffe test --model=./quick_train_test.prototxt.scores --weights=./quick_shuffle_sampled1_iter_10000.caffemodel --iterations=1 --gpu=1
