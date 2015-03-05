"""
Script to build a map from the video name to the associated class index.

Also builds a map from the class number to the associated list of videos
where that class occurs.

Saves each of the maps in a Pickle file.

"""
import csv, pickle, collections, os, argparse



def makeMap(filename, zero_index=False):
    id_to_vid = collections.defaultdict(list)
    vid_to_id = collections.defaultdict(int)

    with open(filename, 'r+') as f:
        data = csv.reader(f, delimiter=' ')
        for row in data:
            #e.g, filename.avi we want filename
            videoName = row[0].split(".")[0]
            class_id = int(row[1])
            if zero_index:
                class_id -= 1
            id_to_vid[class_id].append(videoName)
            vid_to_id[videoName] = class_id
    return (id_to_vid, vid_to_id)


def saveMap(mapTuple,SAVE_FILE):
    with open(SAVE_FILE,'w+') as f:
        pickle.dump(mapTuple,f)



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("vid_lists", help="Video list files", type=str, nargs='+')
  parser.add_argument('-f', '--files', help="Output .pkl files", type=str, nargs='+')
  parser.add_argument("-z", "--zero", help="Enforce zero indexing", action="store_true")

  args = parser.parse_args()
  for vid_list, SAVE_FILE in zip(args.vid_lists,args.files):
      if os.path.exists(vid_list):
          mapTuple = makeMap(vid_list,zero_index=args.zero)
          saveMap(mapTuple,SAVE_FILE)



























