# 2p_imaging
Timothy Warren, timlwarren AT gmail
Python scripts to analyze data collected in Slidebook on Doe LAb 2-p
Current version has three core files

**plot_all_frames_of_a_tif.py**
This assumes tif has been exported from within slidebook. This reads frames in from a tif and plots all frames as a series of images.
An example call to this script is in jupyter notebook plot_all_frames.ipynb

**plot_roi_timecourse.py**
Allows you to select an roi (could be modified to select multiple rois) and plots a time course of mean fluorescence at that roi

**make_images_for_video.py**
Saves a series of png files from tif, which could then be used to make video.
    
