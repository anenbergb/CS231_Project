"""
Given a list of data files, we want to partition it into test and training data sets.

Training videos could be listed in multiple .txt files. Returns a list of the videos with
the full path to each video.



python consolidateFiles.py $UCF_DIR $UCF_list $Valid_DIR $Valid_list $Background_DIR $Back_list



"""
import argparse, os, string


def as_list(*args):
    """
    Example usage:
    X_train_basenames, y_train  = as_list(UCF_list,VALID_list)

    ________________________________________________________
    Given a variable number of video list viles of the format
    ['vid_name'] [class#]

    Returns 2 items:
    1. list of basenames of each video
    2. class of each video
    """
    X = []
    Y = []
    for li in args:
        f = open(li, 'r')
        videos = f.readlines()
        f.close()
        videos = [video.strip() for video in videos]
        #We assume all of the lines in the list file have the struture: ['vid_name'] [class#]
        for line in videos:
            l = line.split()
            Y.append(int(l[1]))
            title=os.path.basename(l[0])
            X.append(title.split('.')[0])
    toReturn = (X,Y)
    return toReturn

def UCF_missing_y_as_list(vid_list, class_index):
    """
    Similar useage to as_list, except that now we expect the videos in the given list
    to not have an associated class:
    struture: ['vid_name']

     class_index: dictionary from video name to the class.
    """

    X = []
    Y = []
    f = open(vid_list, 'r')
    videos = f.readlines()
    f.close()
    videos = [video.strip() for video in videos]
    #We assume all of the lines in the list file have the struture: ['vid_name']
    for line in videos:
        l = line.split()
        title=os.path.basename(l[0])
        X.append(title.split('.')[0])
        index_name = string.lower(title.split('_')[1])
        Y.append(class_index[index_name])

    toReturn = (X,Y)
    return toReturn




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Data directory", type=str, nargs='+')
    parser.add_argument('-l', '--list', help="List of video files", type=str, nargs='+')
    parser.add_argument("-f", "--out_file", help="Text file to save output", type=str)

    args = parser.parse_args()
    if len(args.directory)!=len(args.list):
        raise ValueError("Each list must have an associated data directory not allowed")

    #Open each file and concatenate the files into an output list.
    output = []  
    for directory, li in zip(args.directory,args.list):
        f = open(li, 'r')
        videos = f.readlines()
        f.close()
        videos = [video.strip() for video in videos]
        #We assume all of the lines in the list file have the struture: ['vid_name'] [class#]
        for line in videos:
            l = line.split()
            num = int(l[1])
            title = l[0]
            #the ['vid_name'] could have a '/' which we want to remove.
            # or the ['vid_name'] might not have an extension. In this case we will add .mp4
            title=os.path.basename(title)
            if '.' not in title:
                title = title+'.mp4'
            title = os.path.join(directory,title)
            output.append(title+" "+str(num))
    if args.out_file is None:
        for line in output:
            print line
    else:
        f = open(args.out_file,'w')
        for line in output:
            print >>f, line