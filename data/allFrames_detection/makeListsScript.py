"""
    Constructs the data lists of image to id with the following format.
    [video_name/%08d] [class_id]
    stores them in:
    "./train_list.txt"
    "./test_list.txt"

    Customized for the detection task.
    The class_id is associated with the particular frame.
    Restricted to the 20 detection classes.

"""
import os, pickle, csv


#directory where the training (UCF, validation) and testing frames are
UCF_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/Frames/"
VALID_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/Frames/"
TEST_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/Frames/"


UCF_vidmap = pickle.load( open("./UCF_vidmap.pkl", "rb" ) )[1]
VALID_vidmap = pickle.load( open("./VALID_vidmap.pkl", "rb") )[1]
TEST_vidmap = pickle.load( open("./TEST_vidmap.pkl", "rb") )[1]


VALID_TSmap = pickle.load( open("./VALID_TSmap.pkl", "rb" ) )
TEST_TSmap = pickle.load( open("./TEST_TSmap.pkl", "rb" ) )


detection_class_index = pickle.load( open("./detection_class_index.pkl", "rb" ) )




def makeUCFList(writer):
    """
    writer: the csv writer to write lines of the output file to.
    Returns the UCF list.
    """
    detection_videos = [d for d in os.listdir(UCF_DIR) if UCF_vidmap[d] in detection_class_index[2]]
    
    for idx, video in enumerate(detection_videos):
        if idx % 50 ==0:
            print "processing video %d" % idx
        path_to_video = os.path.join(UCF_DIR,video)
        for frame in os.listdir(path_to_video):
            get_dot_jpg = frame.split('.')
            if len(get_dot_jpg) > 1 and get_dot_jpg[1] != "pkl":
                frame_name = video+"/"+frame
                #Now we need to know the label of this image.
                
                #UCF_vidmap[d] returns the UCF101 index. detection_class_index[2] returns the detection index (1-20)
                frame_index = detection_class_index[2][UCF_vidmap[video]]
                #print frame_name, frame_index
                writer.writerow([frame_name, frame_index])

def makeValOrTest(writer,data_dir,TS_map):           
    detection_videos = [d for d in os.listdir(data_dir) if d in TS_map]
    for idx, video in enumerate(detection_videos):
        if idx % 50 ==0:
            print "processing video %d" % idx
        #print "processing video %s" %video
        path_to_video = os.path.join(data_dir,video)
        frame_to_TS_map = pickle.load( open(os.path.join(path_to_video, "time_stamp_map.pkl"),"rb"))
        
        count_nonzero = 0
        count = 0
        for frame in os.listdir(path_to_video):
            get_dot_jpg = frame.split('.')
            if len(get_dot_jpg) > 1 and get_dot_jpg[1] != "pkl":
                frame_name = video+"/"+frame
                frame_num = int(frame.split('.')[0])
                #print f, frame_num, maxFrame, d
                if frame_num in frame_to_TS_map: #should always hold.
                    frame_TS = round(frame_to_TS_map[frame_num],1) #Round the time_stamp to 0.1
                    if frame_TS in TS_map[video]:
                        count_nonzero += 1
                        frame_index = TS_map[video][frame_TS]
                    else:
                        frame_index = 0 #Background by default.
                    count += 1
                    writer.writerow([frame_name, frame_index])
        #print "frames nonzero: %02f"%(float(count_nonzero)/count)
                

def makeTrainList():
    save_list = "./lists/train_list.txt"
    with open(save_list,'wb') as f:
        writer = csv.writer(f, delimiter=' ')
        print "processing UCF videos"
        makeUCFList(writer)
        print "processing Validation videos"
        makeValOrTest(writer,VALID_DIR,VALID_TSmap)
    
def makeTestList():
    save_list = "./lists/test_list.txt"
    with open(save_list,'wb') as f:
        writer = csv.writer(f, delimiter=' ')
        print "processing Testing videos"
        makeValOrTest(writer,TEST_DIR,TEST_TSmap)                    
    

    
makeTrainList()
makeTestList()
