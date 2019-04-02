#march26_animal_9_meta_dt
from py_utilities import tw_filehandling as fh
meta_dt={}
meta_dt['data_path']= '/Volumes/LaCie/2pdata/march26/animal9/'
meta_dt['meta_file_name']='anim9_plotdata.pck'
#file_names=['---Streaming Phasor Capture - 2 - 2_XY0_Z0_T0000_C0.tif']
meta_dt['file_names']=['---Streaming Phasor Capture - 5_XY0_Z0_T0000_C0.tif','---Streaming Phasor Capture - 5 - 1_XY0_Z0_T0000_C0.tif']
meta_dt['roi_to_plot']=1
meta_dt['on_target_depth']=220.64
meta_dt['off_target']=240.64
meta_dt['on_depths']='odd'
meta_dt['off_depths']='even'
fh.save_to_pickle(meta_dt['data_path']+meta_dt['meta_file_name'], meta_dt)


