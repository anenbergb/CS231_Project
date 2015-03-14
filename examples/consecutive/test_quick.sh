#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

$CAFFE/build/tools/caffe test --model=./quick_train_test.prototxt --weights=./snapshots/run1_iter_300.caffemodel --iterations=1000 --gpu=1
