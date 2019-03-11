import matplotlib.pyplot as plt
import skimage.io
data_path= '/Users/tim/Google Drive/2pdata/01_30_2016/'
im=skimage.io.imread(data_path + 'Streaming Phasor Capture - 5_XY0_Z0_T00_C0.tif')


#plot scale bar
microns_per_pixel=1.47441
pixels_in_50_microns=50./microns_per_pixel
init_scale_height=300
init_scale_x=250

plt.plot([init_scale_x,init_scale_x+pixels_in_50_microns],[init_scale_height, init_scale_height])


#Load GCAMP tif...
im_gcamp=skimage.io.imread(data_path+'A08aGCaMP_SuccessfulStim_AcquisitionPlane_XY0_Z0_T0_C0.tif')
im_chrimson=skimage.io.imread(data_path+'dbdChrimson_SuccessfulStim_StimPlane_XY0_Z0_T0_C0.tif')

#first plot average pixel intensity
zoom_xlim=[150,230]
zoom_ylim=[250,140]


import matplotlib.gridspec as gridspec
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



#then plot variance of pixel intensity