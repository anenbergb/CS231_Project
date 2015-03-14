#!/bin/bash
g++ brox_optical_flow.cpp -o brox_optical_flow -I /usr/local/include/opencv2 -L /usr/local/lib -lopencv_core -lopencv_flann \
-lopencv_imgproc -lopencv_highgui -lopencv_ml -lopencv_video -lopencv_objdetect \
-lopencv_features2d -lopencv_calib3d -lopencv_legacy -lopencv_contrib -lopencv_gpu

#-lm -lcv -lhighgui -lcvaux -lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_objdetect -lopencv_gpu

#g++ -I/usr/local/include/opencv -I/usr/local/include/opencv2 -L/usr/local/lib/ -g -o binary  main.cpp -lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_ml -lopencv_video -lopencv_features2d -lopencv_calib3d -lopencv_objdetect -lopencv_contrib -lopencv_legacy -lopencv_stitching