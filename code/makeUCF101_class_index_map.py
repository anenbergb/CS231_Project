import numpy as np
import subprocess, os, string, sys
from tempfile import TemporaryFile
import argparse
import pickle

import csv

"""
class_index:
Computes a map from class name to class index.
dict{ class_name: class_index}

index_class:
Opposite mapping from the class_index map.
dict{ class_index: class_name}

Example usage:
python compute_UCF101_class_index.py ./

"""


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("class_index", help="File of class index", type=str)
  parser.add_argument("class_out", help="File of saved class index map", type=str)
  parser.add_argument("-p", "--pickle", help="Save to pickle", action="store_true")
  parser.add_argument("-z", "--zero", help="Enforce zero indexing", action="store_true")

  args = parser.parse_args()

  class_index = {}
  index_class = {}
  with open(args.class_index, 'r+') as f:
    data = csv.reader(f, delimiter=' ')
    for row in data:
      class_name = string.lower(row[1])
      class_id = int(row[0])
      if args.zero:
        class_id -= 1
      class_index[class_name] = class_id
      index_class[class_id] = class_name
  
  if args.pickle:
    SAVE_FILE = args.class_out + ".pkl"
    with open(SAVE_FILE, 'w+') as f:
      map_tuple = (class_index, index_class)
      pickle.dump(map_tuple,f)
  else:
    SAVE_FILE = args.class_out + ".npz"
    np.savez(args.class_out, class_index=class_index, index_class=index_class)
