import subprocess, os, pickle, csv

UCF_Frames="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/Frames/"
dataDir="./"
TRAIN_DIR="Train_ln_hard"
OUT_LIST = "UCF_ln_hard.txt"

UCF_vidmap = pickle.load( open(os.path.join(dataDir,"UCF_vidmap.pkl"), "rb" ) )
TrainDir=os.path.join(dataDir,TRAIN_DIR)
if not os.path.isdir(TrainDir):
    os.makedirs(TrainDir) 

#makes a list of vid_name, path_to_vid_dir
UCF_vids = [(d,os.path.join(UCF_Frames,d)) for d in os.listdir(UCF_Frames) if os.path.isdir(os.path.join(UCF_Frames,d))]

#This is a list of frame #class_index lines.
UCF_Frames_train = os.path.join(dataDir,OUT_LIST)

UCF_Frames_list = []
for vid_name, vid_path in UCF_vids:
    vid_index = UCF_vidmap[1][vid_name]
    for f in [f for f in os.listdir(vid_path) if os.path.isfile(os.path.join(vid_path,f))]:
        path_to_frame = os.path.join(vid_path,f)
        new_frame_name = vid_name+"_"+f.split('.')[0]+".jpg"
        copy_location = os.path.join(TrainDir,new_frame_name)
        UCF_Frames_list.append((new_frame_name,vid_index))
        if not os.path.exists(copy_location):
            #p = subprocess.call(['cp', path_to_frame, copy_location])
            #p = subprocess.call(['ln', '-s', path_to_frame, copy_location])
            p = subprocess.call(['ln', path_to_frame, copy_location])

with open(UCF_Frames_train,'wb') as f:
	out = csv.writer(f, delimiter=' ')
	for frame, index in UCF_Frames_list:
		out.writerow([frame, index])