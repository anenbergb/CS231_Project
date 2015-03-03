import subprocess, os, pickle, csv

TRAIN_CHECK_DIR = "./Train_checkingCaffe"
checkingCaffeList = "./checkingCaffe_list.txt"

toListFile = []
counter = 9
for d in os.listdir(TRAIN_CHECK_DIR):
    counter += 1
    for f in os.listdir(os.path.join(TRAIN_CHECK_DIR,d)):
        frame_name = d+"/"+f
        toListFile.append((frame_name,counter))

with open(checkingCaffeList,'wb') as f:
    out = csv.writer(f, delimiter=' ')
    for frame, index in toListFile:
        out.writerow([frame, index])