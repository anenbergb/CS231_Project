UCF_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/Frames/"
VALID_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/Frames/"
TEST_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/Frames/"

DATA_DIRS = [UCF_DIR,VALID_DIR,TEST_DIR]
DESTINATION_DIRS = ["./Train", "./Train", "./Test"]


##FOR EXPERIMENTING
"""
UCF_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/Frames_OLD/"
VALID_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/Frames_OLD/"
TEST_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/Frames_OLD/"

DATA_DIRS = [UCF_DIR,VALID_DIR,TEST_DIR]
DESTINATION_DIRS = ["./Train_OLD", "./Train_OLD", "./Test_OLD"]
"""


import os, subprocess, argparse

def makeDir(directory):
#make the specified directory if it doesn't already exist.
    if not os.path.exists(directory):
        os.makedirs(directory)

def createLinks(data_dir,dest_dir):
    makeDir(dest_dir)
    for d in os.listdir(data_dir)[:5]:
        fullpath_vid = os.path.join(data_dir,d)
        if os.path.isdir(fullpath_vid):
            vid_link = os.path.join(dest_dir,d)
            p = subprocess.call(['ln', '-s', fullpath_vid, vid_link])    


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("directory", help="Data directory", type=str, nargs='+')
  parser.add_argument('-l', '--list', help="Destination directories where the \
      links to the corresponding videos in the data directory will go.", type=str, nargs='+')

  args = parser.parse_args()
  for directory, dest_dir in zip(args.directory,args.list):
      if os.path.exists(directory):
          createLinks(directory,dest_dir)

