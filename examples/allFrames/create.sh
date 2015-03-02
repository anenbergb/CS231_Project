#!/usr/bin/env sh
# Create the imagenet lmdb inputs
# N.B. set the path to the imagenet train + val data dirs
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe
PROJECT=/afs/cs.stanford.edu/u/anenberg/scr/CS231N

EXAMPLE=$PROJECT/examples/UCFff
DATA=$PROJECT/data/UCFff
TOOLS=$CAFFE/build/tools

TRAIN_DATA_ROOT=/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/firstFrame_train/
VAL_DATA_ROOT=/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/firstFrame_val/





# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.
RESIZE=true
if $RESIZE; then
  RESIZE_HEIGHT=224
  RESIZE_WIDTH=224
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

if [ ! -d "$TRAIN_DATA_ROOT" ]; then
  echo "Error: TRAIN_DATA_ROOT is not a path to a directory: $TRAIN_DATA_ROOT"
  echo "Set the TRAIN_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet training data is stored."
  exit 1
fi

if [ ! -d "$VAL_DATA_ROOT" ]; then
  echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
  echo "Set the VAL_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet validation data is stored."
  exit 1
fi

echo "Creating train lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $TRAIN_DATA_ROOT \
    $DATA/UCF_train.txt \
    $EXAMPLE/train_lmdb224

echo "Creating val lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $VAL_DATA_ROOT \
    $DATA/UCF_test.txt \
    $EXAMPLE/val_lmdb224

echo "Done."
