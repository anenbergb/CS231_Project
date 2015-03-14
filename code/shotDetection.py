import os, subprocess, pickle

def findSceneTrans(videoName):
    """
    Given a video, returns a list of frame numbers which are the starting frame of the transition
    between scenes.
    """
    
    #Returns the duration of the video in seconds.
    if not os.path.exists(videoName):
        print '%s does not exist!' % videoName
        return False
    shotdetect = '/afs/cs.stanford.edu/u/anenberg/scr/Shotdetect/build/shotdetect-cmd'
    threshold = 60
    p = subprocess.Popen([shotdetect, '-i', videoName, '-a', 'FOO', '-o', 'shot_FOO', '-s', str(threshold)], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = p.communicate()
    output = err.split()
    frameList = []
    for i in xrange(len(output)):
        if output[i]=='frame::':
            frameList.append(int(output[i+1]))
    return frameList

sceneTransitionDir = "/afs/cs.stanford.edu/u/anenberg/scr/CS231N/data/allFrames/sceneTransitions"
ValidationVideos = "/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/videos"
TestingVideos = "/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/videos"

Video_Repos = [ValidationVideos,TestingVideos]

for vid_repo in Video_Repos[::-1]:
    for video in os.listdir(vid_repo):
        vid_path = os.path.join(vid_repo,video)
        scene_list_path = os.path.join(sceneTransitionDir,video[:-4]+".pkl") #get rid of the .mp4
        if not os.path.exists(scene_list_path): #Ensure that we don't waste time recomputing lists that we already made.
            scene_list = findSceneTrans(vid_path)
            print "completed processing: %s" % video
            pickle.dump(scene_list, open(scene_list_path, 'wb'))