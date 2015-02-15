#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

$CAFFE/build/tools/caffe test --model=./UCFff10_quick_train_test.prototxt --weights=./UCFff10_quick_iter_2000.caffemodel --iterations=100 --gpu=1