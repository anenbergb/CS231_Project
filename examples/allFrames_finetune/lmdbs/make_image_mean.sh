#!/usr/bin/env sh
# Compute the mean image from the imagenet training leveldb
# N.B. this is available in data/ilsvrc12

#./build/tools/compute_image_mean examples/imagenet/ilsvrc12_train_leveldb \
#  data/ilsvrc12/imagenet_mean.binaryproto

CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

for f in train_lmdb*; 
	do echo "Processing $f file.."; 
	TAG=${f#train_lmdb};

	echo "Writing mean$TAG.binaryproto from train_lmdb$TAG"
	$CAFFE/build/tools/compute_image_mean train_lmdb$TAG mean$TAG.binaryproto

	NUMPY_OUTFILE="mean$TAG.npy";
	
	python ../../../convert_protomean.py mean$TAG.binaryproto $NUMPY_OUTFILE
done
echo "Done."

