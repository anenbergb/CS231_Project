"""
    Constructs the data lists of image to id with the following format.
    [video_name/%08d] [class_id]
    stores them in:
    "./Train_list.txt"
    "./Test_list.txt"

"""
import subprocess, os, pickle, csv, argparse



##HARD coded in the dictionaries from the video name to the class index.
UCF_vidmap_PATH = "./UCF_vidmap.pkl"
VALID_vidmap_PATH = "./VALID_vidmap.pkl"
TEST_vidmap_PATH = "./TEST_vidmap.pkl"


UCF_vidmap = pickle.load( open(UCF_vidmap_PATH, "rb" ) )
VALID_vidmap = pickle.load( open(VALID_vidmap_PATH, "rb" ) )
TEST_vidmap = pickle.load( open(TEST_vidmap_PATH, "rb" ) )
# Train_map: map from individual video name to class label for
# UCF and Validation videos.
# Test_map: same thing, but for Test videos.
Train_map = UCF_vidmap[1]
Train_map.update(VALID_vidmap[1])
Test_map = TEST_vidmap[1]

VID_MAPS = [Train_map,Test_map]

def makeList(data_dir,out_list, vid_map):
    """
    out_list: directory to populate with list files. 1 list file per video, and contains the mapping
              between frame and class index.
    """
    if not os.path.exists(out_list):
        os.makedirs(out_list)
    for d in os.listdir(data_dir):
        video_list_txt = os.path.join(out_list,d)+".txt"
        if not os.path.exists(video_list_txt): #Just making sure this video_list.txt file doesn't exist
            with open(video_list_txt,'wb') as f:
                out = csv.writer(f,delimiter=' ')
                for f in os.listdir(os.path.join(data_dir,d)): #iterates over the frames.
                    get_dot_jpg = f.split('.')
                    if len(get_dot_jpg) > 1 and get_dot_jpg[1] != "pkl":
                        frame_name = d+"/"+f
                        #Now we need to know the label of this image.
                        frame_index = vid_map[d]
                        #print frame_name, frame_index
                        #toListFile.append((frame_name,frame_index))
                        out.writerow([frame_name, frame_index])



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("directory", help="Video directory for this project", type=str, nargs=2)
  parser.add_argument('-l', '--list', help="Lists to create from this directory", type=str, nargs=2)

  args = parser.parse_args()
  for directory, out_list, vid_map in zip(args.directory,args.list,VID_MAPS):
      if os.path.exists(directory):
          makeList(directory,out_list,vid_map)






