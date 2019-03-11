import matplotlib.pyplot as plt
import skimage.io
import numpy as np


#this assumes that a tif_stack has been created
#(e.g. with plot_example_time_course.py)

#update this with desired file location.
save_location='/Users/tim/Dropbox/2p_analysis/video'

num_frames=len(tif_stack[:,0,0])
for crframe in np.arange(num_frames):
	plt.figure()
	plt.imshow(im_cut_all[crframe,:])
	savefig(save_location+'frame%d.png'%crframe)