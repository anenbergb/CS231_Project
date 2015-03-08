#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

#For no fine tuning the earlier levels.
$CAFFE/build/tools/caffe train -solver ./quick_solver_lr0.prototxt -weights $CAFFE"/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel" -gpu 2
