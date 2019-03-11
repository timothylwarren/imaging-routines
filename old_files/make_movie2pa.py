


import skimage.io
import matplotlib.pyplot as plt 
import numpy as np
import pdb
#needs to be updated for your data location 
data_path='/Users/tim/Dropbox/'
file_name='Streaming Phasor Capture - 2_XY0_Z0_T000_C0.tif'


class Make_Movie():

	def run(self):
		
		self.crfig=pylab.figure()
        gs = gridspec.GridSpec(8, 8)
        
        self.vidax=pylab.subplot(gs[0:7,0:7])



		self.make_frames()

	
	def make_frames(self):
		
		self.tif_array=skimage.io.imread(data_path+file_name)
		for self.video_frame_raw in self.tif_array:
			self.crfig=pylab.figure()
        	gs = gridspec.GridSpec(8, 8)
        
        	self.vidax=pylab.subplot(gs[0:7,0:7])

			self.vidax.imshow(self.video_frame_raw,cmap=pylab.get_cmap('gray'),origin='lower')

            #self.initialize_figure()
            
            #self.read_in_video_file()
            #self.plot_video_and_data()
            
            
            #self.crfig.savefig(self.get_fig_name())
            
            #pylab.close('all')
 	
 		    

if __name__ == '__main__':
    import sys
    make_movie = Make_Movie()
    datind=make_movie.run()
