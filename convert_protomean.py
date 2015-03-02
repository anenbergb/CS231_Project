import numpy as np
import sys
sys.path.append("/afs/cs.stanford.edu/u/anenberg/scr/caffe/python/")
import caffe
if len(sys.argv) != 3:
	print "Usage: python convert_protomean.py proto.mean out.npy"

blob = caffe.proto.caffe_pb2.BlobProto()
data = open( sys.argv[1] , 'rb' ).read()
blob.ParseFromString(data)
arr = np.array( caffe.io.blobproto_to_array(blob) )
out = arr[0]
print 'Converted %s and wrote output to %s'%(sys.argv[1], sys.argv[2])
np.save( sys.argv[2] , out )
