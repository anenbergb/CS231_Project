#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe


$CAFFE"/build/tools/extract_features.bin" ./snapshots/quick_shuffle_sampled_afMean_startAt10000_iter_10000.caffemodel \
./quick_train_test.prototxt fc8_allFrames ./temp/features2 10 lmdb