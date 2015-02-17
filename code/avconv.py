# python wrapper for basic avconv operations
# resize video, check if a video is corrupted, etc.

import subprocess, re, os

# provide your own ffmpeg here
avconv = 'avconv'

# test
def basicResize(videoName,resizedName,height=320,width=240):
    if not os.path.exists(videoName):
        print '%s does not exist!' % videoName
        return False
    dims = '%dx%d'%(height,width)
    # call avconv again to resize
    subprocess.call([avconv, '-i', videoName, '-s', dims, '-b', '64ka', resizedName])
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
    # call avconv and grab its stderr output
    p = subprocess.call('avconv -i %s -r 1 -s qvga -t 1 -f image2 %s' % (videoName,frameName), shell=True)
    return p
