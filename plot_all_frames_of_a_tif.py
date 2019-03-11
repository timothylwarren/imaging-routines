import matplotlib.pyplot as plt
import skimage.io
import numpy as np
from roipoly import RoiPoly
import matplotlib.gridspec as gridspec
plt.ion()
#this needs to be set to be location of your tif file.
data_path= '/Users/tim/python_packages/2p_imaging/example_data/'

#read in tif file
im=skimage.io.imread(data_path + 'Streaming Phasor Capture - 5_XY0_Z0_T00_C0.tif')

zoom_xlim=[150,230]
zoom_ylim=[250,140]

###plot all frames as series of rows.
#####

fig = plt.figure()
num_rows=4
num_col=10
rowct=0
colct=0
gs = gridspec.GridSpec(num_rows, num_col, figure=fig)
tmlapse_in_s=.11963
for cr_frame in np.arange(40):
	#col_vl=np.mod(cr_frame,num_rows)
	print('colct=%d'%colct)
	#row_vl=np.mod(cr_frame,num_col)
	ax=fig.add_subplot(gs[rowct,colct])
	plt.imshow(im[cr_frame,:])
	plt.xlim(zoom_xlim)
	plt.ylim(zoom_ylim)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	crtime=cr_frame*tmlapse_in_s
	title_text='%.2f'%crtime
	plt.title(title_text,fontsize=8)
	#ax.tick_params(bottom='off',left='off')

	if colct==num_col-1:
		rowct=rowct+1
		colct=0
	else:
		colct=colct+1

