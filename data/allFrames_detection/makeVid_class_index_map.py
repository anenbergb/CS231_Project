import os,collections,csv,pickle

#### LOAD MAPS
class_index_map = pickle.load( open("./detection_class_index.pkl", "rb" ) )




annotations = ["/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/annotation", \
               "/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/annotation"]
SAVE_NAMES = ["./VALID_TSmap.pkl","./TEST_TSmap.pkl"]

def makeMap(filename,theMap):
    """
    For every line:
    [video_name starting_time ending_time]
    populates:
    theMap[video_name][starting_time] ... theMap[video_name][ending_time] with class_index.
    """
    class_index = class_index_map[0]
    
    class_name = os.path.basename(filename).split('.')[0].split('_')[0]
    if class_name != "Ambiguous": #We don't want to process the Ambiguous class.
        with open(filename, 'r+') as f:
            data = csv.reader(f, delimiter=' ')
            for row in data:
                #print row
                videoName = row[0]
                startTS = int(round(float(row[2]),1)*10)
                endTS = int(round(float(row[3]),1)*10)
                #print startTS, endTS
                for i in xrange(startTS,endTS):
                    theMap[videoName][round(i*0.1,1)]= class_index[class_name]
    return theMap

def saveMap(theMap,SAVED_NAME):
    with open(SAVED_NAME,'w+') as f:
        pickle.dump(theMap,f)




for annotation, SAVE_NAME in zip(annotations,SAVE_NAMES):
    theMap = collections.defaultdict(dict)
    for f in os.listdir(annotation):
        theMap = makeMap(os.path.join(annotation,f),theMap)
    saveMap(theMap,SAVE_NAME)  