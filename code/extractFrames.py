"""

Input:
video_list: list of frames in a text file. e.g. ucf_list.txt
video_directory: path to the directory where the videos exist.
(/afs/.../cvgl/../Validation/Videos)


Outputs:
For each video in the video list, populates a subdirectory in the super_directory 
(/afs/.../cvgl/../Validation/)
Frames/video_name where video_name is the name of the video in the video list.
Note: ASSUMES we are populating the Frames subdirectory in the super_directory. 
(/afs/.../cvgl/../Validation) is a valid super_directory.

The videos are extracted by frame in .jpg format.
Hard coded in : 224x224 format.

"""
import os, csv, sys, argparse, pickle
import avconv



def frames_from_vids(listname, dataDir):
    """
    listname: path to list of the input videos.
    dataDir: directory where the actual video exits.
     e.g. : /afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/videos
    num: number of input videos to extract frames from.


    Extracts the video, and also guarentees that all the videos are the same 
    size.

    """
    #First check if the super_directory/Frames exists.
    # /afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/Frames
    head,tail = os.path.split(dataDir)
    if tail=="": #if the original dataDir ended in a /
        #now grab the path up to  /../THUMOS2014/Validation/
        head,tail = os.path.split(head) 
    framesDir = os.path.join(head,"Frames")
    if not os.path.isdir(framesDir):
        os.makedirs(framesDir)


    vid_to_extract = []
    #with open(listname, 'r+') as f:
    f = open(listname, 'r+')
    data = csv.reader(f, delimiter=' ')
    for row in data:
        #e.g, [filename.avi 10] we want filename.avi
        videoName = row[0]
        #the ['vid_name'] could have a '/' which we want to remove.
        # or the ['vid_name'] might not have an extension. In this case we will add .mp4
        name=os.path.basename(videoName)
        if '.' not in name:
            name = name+'.mp4'
        vid_to_extract.append(name)
    f.close()

    for vid in vid_to_extract:
        full_vid_path = os.path.join(dataDir,vid)
        # '/afs/.../video_validation_0001001.mp4' >> video_validation_0001001
        name = os.path.basename(vid).split('.')[0]
        # /afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/Frames/video_validation_0001001
        videoFramesDir = os.path.join(framesDir,name)
        if not os.path.exists(videoFramesDir):
            #Check if the video is less than 2000 seconds (approx. 33 mins)
            duration = avconv.getDuration(full_vid_path)
            if duration < 2000:
                if not os.path.exists(videoFramesDir):
                    os.makedirs(videoFramesDir)
                    print videoFramesDir
                    #If we have not yet extracted frames for this video
                    frame_to_ts = avconv.extract_frame_ts(full_vid_path,videoFramesDir,format='jpg',resize='224x224',withTS=True)
                    pickle_save_path = os.path.join(videoFramesDir,"time_stamp_map.pkl")
                    with open(pickle_save_path,'w+') as f:
                        pickle.dump(frame_to_ts,f)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("directory", help="Data directory", type=str, nargs='+')
  parser.add_argument('-l', '--list', help="List of video files", type=str, nargs='+')

  args = parser.parse_args()
  for directory, li in zip(args.directory,args.list):
    frames_from_vids(li, directory)







