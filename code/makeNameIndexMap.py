"""
Script to build a map from the video name to the associated class index.

Also builds a map from the class number to the associated list of videos
where that class occurs.

Saves each of the maps in a Pickle file.

"""
import csv, pickle, collections, os


UCF_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/train_set.txt"
VALID_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/validation_primaryclass.txt"
TEST_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/test_primaryclass.txt"

SAVE_DIR="../data/allFrames"
zeroIndex = False



def vid_dict(filename):
    id_to_vid = collections.defaultdict(list)
    vid_to_id = collections.defaultdict(int)

    with open(filename, 'r+') as f:
        data = csv.reader(f, delimiter=' ')
        for row in data:
            #e.g, filename.avi we want filename
            videoName = row[0].split(".")[0]
            class_id = int(row[1])
            if zeroIndex:
                class_id -= 1
            id_to_vid[class_id].append(videoName)
            vid_to_id[videoName] = class_id
    return id_to_vid, vid_to_id

dataLists = [UCF_FULL, VALID_FULL, TEST_FULL]
mapNames = ["UCF_vidmap.pkl", "VALID_vidmap.pkl", "TEST_vidmap.pkl"]

for dataList, mapName in zip(dataLists,mapNames):
    vid_map = vid_dict(dataList)
    mapSavePath = os.path.join(SAVE_DIR,mapName)
    with open(mapSavePath,'w+') as f:
        pickle.dump(vid_map,f)





