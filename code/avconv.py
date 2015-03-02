# python wrapper for basic avconv operations
# resize video, check if a video is corrupted, etc.

import subprocess, re, os

# provide your own ffmpeg here
avconv = 'avconv'


def getDuration(videoName):
    #Returns the duration of the video in seconds.
    if not os.path.exists(videoName):
        print '%s does not exist!' % videoName
        return False
    # avconv -i video 2>&1 | grep 'Duration' | awk '{print $2}' | sed s/,//

    p = subprocess.Popen(['avconv', '-i', videoName],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = p.communicate()
    output = err.split()
    for i in xrange(len(output)):
        if output[i]=='Duration:':
            timestr_list = output[i+1].strip(',').replace('.',':').split(':')
            ftr = [3600,60,1,0.01]
            return sum([a*b for a,b in zip(ftr, map(int,timestr_list))])

def getSize(videoName):
    #Returns the duration of the video in seconds.
    if not os.path.exists(videoName):
        print '%s does not exist!' % videoName
        return False
    p = subprocess.Popen(['avconv', '-i', videoName],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = p.communicate()
    output = err.split()
    for i in xrange(len(output)):
        if output[i]=='Video:':
            return output[i+4].strip(',')





def basicResize(videoName,resizedName):
    if not os.path.exists(videoName):
        print '%s does not exist!' % videoName
        return False

    # call avconv again to resize
    subprocess.call([avconv, '-i', videoName, '-s', '320x240', '-b', '64k', resizedName])
    return check(resizedName)

# resize videoName to 320x240 and store in resizedName
# if succeed return True
def resize(videoName, resizedName):
    if not os.path.exists(videoName):
        print '%s does not exist!' % videoName
        return False
    # call ffmpeg and grab its stderr output
    p = subprocess.Popen([avconv, "-i", videoName], stderr=subprocess.PIPE)
    out, err = p.communicate()
    # search resolution info
    if err.find('differs from') > -1:
        return False
    reso = re.findall(r'Video.*, ([0-9]+)x([0-9]+)', err)
    print 'FFMPEG: Reso', reso
    if len(reso) < 1:
        return False
    # call avconv again to resize
    subprocess.call([avconv, '-i', videoName, '-s', '320x240', '-b', '64k', resizedName])
    return check(resizedName)

# check if the video file is corrupted or not
def check(videoName):
    if not os.path.exists(videoName):
        return False
    p = subprocess.Popen([avconv, "-i", videoName], stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err.find('Invalid') > -1:
        return False
    return True

def extract_frame(videoName,frameName):
    """Doc
    Extracts the first frame from the input video (videoName)
    and saves it at the location (frameName)
    """
    #forces extracted frames to be 320x240 dim.
    if not os.path.exists(videoName):
        print '%s does not exist!' % videoName
        return False
    # call ffmpeg and grab its stderr output
    p = subprocess.call('ffmpeg -i %s -r 1 -s qvga -t 1 -f image2 %s' % (videoName,frameName), shell=True)
    return p



def extract_frames(video,dataSetDir):
    """
    Splits the video into frames of .png and .ppm format.

    video: input video (full path to file)
    dataSetDir: directory where the videoName directory will be located.
            e.g. UCF
    Extracts the first frame from the input video (videoName)
    and saves it at the location (frameName)
    """
    #forces extracted frames to be 320x240 dim.
    if not os.path.exists(video):
        print '%s does not exist!' % video
        return False
    # '/afs/.../video_validation_0001001.mp4' >> video_validation_0001001
    name = os.path.basename(video).split('.')[0]

    videoDir = os.path.join(dataSetDir,name)

    PNG_dir = os.path.join(videoDir,"Frames")
    PPM_dir = os.path.join(videoDir,"ppm")

    if not os.path.isdir(videoDir):
        os.makedirs(videoDir)
        os.makedirs(PNG_dir)
        os.makedirs(PPM_dir)
    else:
        if not os.path.isdir(PNG_dir):
            os.makedirs(PNG_dir)
        if not os.path.isdir(PPM_dir):
            os.makedirs(PPM_dir)

    # call ffmpeg and grab its stderr output
    p = subprocess.call([avconv, '-i', video, PNG_dir+'/%05d.png'])
    p = subprocess.call([avconv, '-i', video, PPM_dir+'/%05d.ppm'])

    return p

def extract_frames_jpg(video,dataSetDir):
    """
    Splits the video into frames of .jpg format

    video: input video (full path to file)
    dataSetDir: directory where the videoName directory will be located.
            e.g. UCF
    Extracts the first frame from the input video (videoName)
    and saves it at the location (frameName)
    """
    #forces extracted frames to be 320x240 dim.
    if not os.path.exists(video):
        print '%s does not exist!' % video
        return False
    # '/afs/.../video_validation_0001001.mp4' >> video_validation_0001001
    name = os.path.basename(video).split('.')[0]

    videoDir = os.path.join(dataSetDir,name)

    JPG_dir = os.path.join(videoDir,"JPG")

    if not os.path.isdir(videoDir):
        os.makedirs(videoDir)
        os.makedirs(JPG_dir)
    else:
        if not os.path.isdir(JPG_dir):
            os.makedirs(JPG_dir)
    # call ffmpeg and grab its stderr output
    p = subprocess.call([avconv, '-i', video, JPG_dir+'/%08d.jpg'])
    return p

def extractFrames(video,vidFrameDir, format='jpg', resize=None):
    """
    Splits the video into frames of the specified format

    video: input video (full path to file)
    vidFrameDir: full path to the directory to store the
                .jpg frames.

    """
    #forces extracted frames to be 320x240 dim.

    if not os.path.exists(video):
        print '%s does not exist!' % video
        return False
    if not os.path.isdir(vidFrameDir):
        os.makedirs(vidFrameDir)
    # call avconv and grab its stderr output
    vid_type = '/'+'%05d.'+format

    if resize is not None:
        #e.g., resize='224x224'
        p = subprocess.call([avconv, '-i', video, '-s', resize, vidFrameDir+vid_type])
    else:
        p = subprocess.call([avconv, '-i', video, vidFrameDir+vid_type])
    return p
