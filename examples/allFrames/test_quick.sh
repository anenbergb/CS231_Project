#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

$CAFFE/build/tools/caffe test --model=./quick_train_test.prototxt --weights=./quick224_iter_2000.caffemodel --iterations=300 --gpu=1
