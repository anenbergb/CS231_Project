"""
    Constructs the data lists of image to id with the following format.
    [video_name/%08d] [class_id]
    stores them in:
    "./Train_list.txt"
    "./Test_list.txt"

    Customized for the detection task.

"""
import subprocess, os, pickle, csv, argparse



##HARD coded in the dictionaries from the video name to the class index.
#map[videoname][time_stamp] = class_id
#detection_class_index = pickle.load( open("./detection_class_index.pkl","rb"))



VALID_TSmap = pickle.load( open("./VALID_TSmap.pkl", "rb" ) )
TEST_TSmap = pickle.load( open("./TEST_TSmap.pkl", "rb" ) )
UCF_vidmap = pickle.load( open("./UCF_vidmap.pkl", "rb" ) )[1]
detection_class_index = pickle.load( open("./detection_class_index.pkl", "rb" ) )





VID_MAPS = [(UCF_vidmap,VALID_TSmap),TEST_TSmap]

def makeTestList(data_dir, vid_map):
    toListFile = []
    for d in os.listdir(data_dir): #d is the name of the video
        path_to_d = os.path.join(data_dir,d)
        frame_to_TS_map = pickle.load( open(os.path.join(path_to_d, "time_stamp_map.pkl"),"rb"))
        maxFrame = max(frame_to_TS_map.keys())
        for f in os.listdir(os.path.join(data_dir,d)):
            get_dot_jpg = f.split('.')
            if len(get_dot_jpg) > 1 and get_dot_jpg[1] != "pkl":
                frame_name = d+"/"+f
                #Now we need to know the label of this image.
                frame_num = int(f.split('.'))
                if frame_num < maxFrame:
                    frame_TS = frame_to_TS_map[frame_num]
                    class_id = vid_map[d][frame_TS]
                    #print frame_name, frame_index
                    toListFile.append((frame_name,class_id))
    return toListFile


def makeTrainList(data_dir, map_tuple):
    UCF_vidmap = map_tuple[0]
    VAL_TSmap = map_tuple[1]

    toListFile = []
    for d in os.listdir(data_dir): #d is the name of the video
        path_to_d = os.path.join(data_dir,d)
        frame_to_TS_map = pickle.load( open(os.path.join(path_to_d, "time_stamp_map.pkl"),"rb"))
        maxFrame = max(frame_to_TS_map.keys())
        for f in os.listdir(os.path.join(data_dir,d)):
            get_dot_jpg = f.split('.')
            if len(get_dot_jpg) > 1 and get_dot_jpg[1] != "pkl":
                frame_name = d+"/"+f
                #If the frame is a UCF vid, then we should just label the frame as the video class label.
                if d in UCF_vidmap.keys():
                    class_id = UCF_vidmap[d]
                    toListFile.append((frame_name,class_id))
                else:
                    #The frame is validation, so look at the time stamp.
                    frame_num = int(f.split('.')[0])
                    #print f, frame_num, maxFrame, d
                    if frame_num in frame_to_TS_map.keys():
                        frame_TS = frame_to_TS_map[frame_num]
                        if frame_TS in VAL_TSmap[d].keys():
                            class_id = VAL_TSmap[d][frame_TS]
                        else:
                            class_id = 0 #Background by default.
                        #print frame_name, frame_index
                        toListFile.append((frame_name,class_id))
    return toListFile

def printList(generated_list,out_file):
    with open(out_file,'wb') as f:
        out = csv.writer(f, delimiter=' ')
        for frame, index in generated_list:
            out.writerow([frame, index])





if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("directory", help="Video directory for this project", type=str, nargs=2)
  parser.add_argument('-l', '--list', help="Lists to create from this directory", type=str, nargs=2)

  args = parser.parse_args()

  if os.path.exists(args.directory[0]):
    trainList = makeTrainList(args.directory[0],VID_MAPS[0])
    printList(trainList,args.list[0])
  if os.path.exists(args.directory[1]):
    testList = makeTestList(args.directory[1],VID_MAPS[1])
    printList(testList,args.list[1])





