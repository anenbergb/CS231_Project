"""
findTubelets.py is a utility that will eventually be merged with
 extracFrames.py to process the tubelets from videos in an online
 manner.

 Precondition: There exist dataSet directories such as UCF,
 Validation, Test that contain directories corresponding to video
 names such as v_ApplyEyeMakeup_g08_c01.
 Each directory contains 2 subdirectories:
 1. Frames
 2. ppm

 1st: 
 - Use libsvx.v3.0 to get intial supervoxels, e.g. libsvx.v3.0/gbh/gbh 200 0 500 0.5 0  Diving-
 Side_001/ppm  Diving-Side_001/ppm_c200_sz500/

- Use Motion2D to pixelwise compute IME values between every two consecutive frames, 
e.g.  Motion2D -p Diving-Side_001/Frames/%05d.png  -m AC -f 0 -i 54 -w Diving-Side_001/AC_IMEmap/%05d.png

Run as follows:
[svoxboxes priority] = Videoshow2HierarchicalGrouping_3D_frm('Diving-Side_001');

svoxboxes is nx1 cell array, s=1:n-1 are for different chosen strategies (in setup_paths.m) and svoxboxes{n} is for initial voxels.

svoxboxes{s} is: nr_tubelets X nr_frames X 4 

'nr_tubelets' is number of tubelets in the video for strategy 's'
'nr_frames' is number of frames in video 'v'.

For each tubelet in each frame we have a bounding box as: [ymin xmin ymax xmax].
If tubelet is not present in a frame then we have [0 0 0 0].

"""


import os, csv, sys, subprocess


DestinationDir = "./" #Directory that contains the DataSetDirs [UCF, Validation, Test]



def runMotion2D(frameDir):
    """
    frameDir: path to the directory containing the different frames.
            e.g. ./UCF/v_ApplyEyeMakeup_g08_c01/

    Example command line call:
    $SCR"Motion2D-1.3.11.1/bin/Linux/Motion2D" -p UCF/v_ApplyEyeMakeup_g08_c01/Frames/%05d.png \
      -m AC -f 1 -i 54 -w UCF/v_ApplyEyeMakeup_g08_c01/AC_IMEmap/%05d.png
    """
    AC_IMEmap = os.path.join(frameDir,"AC_IMEmap")
    if not os.path.isdir(AC_IMEmap):
        os.makedirs(AC_IMEmap)
        src = "/afs/cs.stanford.edu/u/anenberg/scr/"
        motion2D = os.path.join(src,"Motion2D-1.3.11.1/bin/Linux/Motion2D")
        p_arg = os.path.join(frameDir,"Frames/%05d.png")
        Frames = os.path.join(frameDir, "Frames")
        i_arg = subprocess.check_output("ls %s | wc -l" %(Frames), shell=True).strip()
        w_arg = os.path.join(AC_IMEmap,"%05d.png")
        p = subprocess.call([motion2D, '-p', p_arg, '-m', 'AC', '-f', '1', '-i', i_arg, '-w', w_arg])

        
def runGBSeg(frameDir):
    """
    Example command line call:
    $SCR"libsvx.v3.0/gbh/gbh" 200 0 500 0.5 0  UCF/v_ApplyEyeMakeup_g08_c01/ppm \
    UCF/v_ApplyEyeMakeup_g08_c01/ppm_c200_sz500/
    """

    #First make the ppm_c200_sz500 directory
    GBdir = os.path.join(frameDir,"ppm_c200_sz500")
    if not os.path.isdir(GBdir):
        os.makedirs(GBdir)
        src = "/afs/cs.stanford.edu/u/anenberg/scr/"
        gbh_exec = os.path.join(src,"libsvx.v3.0/gbh/gbh")
        PPMdir = os.path.join(frameDir,"ppm")
        p = subprocess.call([gbh_exec, '200', '0', '500', '0.5', '0', PPMdir, GBdir])


def runMatlabTubelet(frameDir):
    """
    Example command line call:
    #vid='/afs/cs.stanford.edu/u/anenberg/scr/snrThesis/examples/Feb22/UCF/v_ApplyEyeMakeup_g08_c01'
    #tubelet='/afs/cs.stanford.edu/u/anenberg/scr/snrThesis/examples/Feb22/UCF/v_ApplyEyeMakeup_g08_c01/tubelet2'
    #matlab  -nosplash -nodisplay -nojvm -r \
    #"[svoxboxes priority] = Videoshow2HierarchicalGrouping_3D_frm('$vid');,save('$tubelet');,quit()"


    #for f in *.BMP; do
    #    matlab -nosplash -nodisplay -nojvm -r "my_command('$f'),quit()"
    #done

    """
    svoxDir= os.path.join(frameDir,"svox")
    if not os.path.isdir(svoxDir):
        os.makedirs(svoxDir)
    frameDir_absPath = os.path.abspath(frameDir)
    tubelet = os.path.join(frameDir_absPath,"tubelet")
    if not os.path.exists(tubelet+".mat"):
        script = 'matlab -nosplash -nodisplay -nojvm -r \"[svoxboxes priority] = Videoshow2HierarchicalGrouping_3D_frm(\'%s\');,save(\'%s\');,quit()\"'% (frameDir_absPath, tubelet)
        subprocess.call(script,shell=True)



dataSets = ["UCF", "Validation", "Test"]
for dataSet in dataSets[:2]:
    dataSetDir = os.path.join(DestinationDir,dataSet)
    frameDirs = [os.path.join(dataSetDir,f) for f in os.listdir(dataSetDir) if os.path.isdir(os.path.join(dataSetDir,f))]
    for frameDir in frameDirs:
        runGBSeg(frameDir)
        runMotion2D(frameDir)
        runMatlabTubelet(frameDir)

"""
frameDir="./UCF/v_ApplyEyeMakeup_g08_c02/"
runGBSeg(frameDir)
runMotion2D(frameDir)
runMatlabTubelet(frameDir)
"""








