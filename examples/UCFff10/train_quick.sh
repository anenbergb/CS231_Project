#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

$CAFFE/build/tools/caffe train --solver=./UCFff10_quick_solver.prototxt --gpu=1