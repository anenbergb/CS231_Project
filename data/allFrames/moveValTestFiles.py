"""
Extracts the frames from the Validation and Test video collections and 
creates a map from the extracted frame to the corresponding time stamp:
v_ApplyEyeMakeup_g01_c02_00000001.jpg : 0.4

Observations:
It appears that the first frame doesn't correspond to time stamp 0.00. 

"""
import subprocess, os
import pickle


"""
Helper functions:
"""

def extract_frame_for_vid(video,directory):
	"""
	video: path to input video.
	directory: path to directory to save the video frames.

	Returns:
	frame_to_ts: dictionary of frame to time stamp.
			e.g. 	v_ApplyEyeMakeup_g01_c02_00000001.jpg : 0.4
	"""
	resize='224x224'
	vid_name = os.path.basename(video).split('.')[0]
	frameNames = vid_name+'_'+'%08d.jpg'
	framePath = os.path.join(directory,frameNames)
	
	frame_to_ts = {}
	
	p = subprocess.Popen(['avconv', '-i', video, '-s', resize,'-an', '-vf', 'showinfo', framePath],
	                     stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	out, err = p.communicate()
	maxI = 0
	maxframe = None
	for l in err.split('\n'):
	    if l[:9] =='[showinfo' and 'n:' in l:
	        #The .jpg files are saved with +1 offset
	        frameIndex = int(l.split(' ')[3].split(':')[1]) +1
	        timeStamp = float(l.split(' ')[5].split(':')[1])
	        frame_00jpg = '%08d.jpg' % frameIndex
	        frameName = vid_name+'_'+frame_00jpg
	        frame_to_ts[frameName] = timeStamp
	        if frameIndex > maxI:
	            maxI = frameIndex
	            maxframe = frameName
	
	#Remove the max, entry in each of the maps. It is an invalid frame.
	del frame_to_ts[maxframe]

	return frame_to_ts


"""
Script begins here:
"""
testVid = "/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/videos/v_ApplyEyeMakeup_g01_c02.avi"
TESTDIR = "./Test"

extract_frame_for_vid(testVid,TESTDIR)


