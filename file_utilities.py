
import skimage.io
import xmltodict
import numpy as np
import  pdb


def read_in_tif(filename):
    im={}
    im['tifstack']=skimage.io.imread(filename)
    return im

def read_in_tif_and_get_metadata(filename):
#this needs to be set to be location of your tif file.
    im={}
    stim={}
    im['tifstack']=skimage.io.imread(filename)
    (im['time_stamps'],im['frame_nums'],stim['stim_time_stamps'])=get_time_stamps(filename)
    return(im,stim)

	#redataata_path= '/Users/tim/data/2pdata/exported_tifs/'
	#file_name= 'Streaming Phasor Capture - 1_XY0_Z0_T000_C0.tif'

def make_edges(xvls,yvls,imzoom):
    zero_im=np.zeros(np.shape(imzoom))
    
    zero_im[yvls,xvls]=1
    edges=edge_detector(zero_im)
    return edges



def edge_detector(im):
    
    from skimage import feature
 
    #im = io.imread('boat.png')
    edges = feature.canny(im)
    return (edges)
    #skimage.io.imshow(edges)
    #io.show()


def get_time_stamps(filename):
    time_stamps=[]
    image_frame_nums=[]
    stim_times=[]
    with open (filename + '.xml') as fd: 
        doc=xmltodict.parse(fd.read())
      
        all_planes=doc['OME']['Image']['Pixels']['Plane']
        for crplane in all_planes:

            time_stamps.append(crplane['@DeltaT'])
            
            image_frame_nums.append(crplane['@TheT'])
        stim_events=doc['OME']['ROI']
        
        for crstim in stim_events:
            stim_times.append(crstim['Union']['Shape']['@theT'])

        return (time_stamps,image_frame_nums,stim_times)





def get_stim_depths(logfilein):
    
    with open(logfilein,'r') as log_file:
        write_flag=False
        elapsed_on_flag=False
        depths=[]
        times=[]
        for line in log_file:
            pieces=line.split()
            
            print(pieces[0])
            
            if pieces[0] == 'Elapsed':
                elapsed_on_flag=True
            elif elapsed_on_flag:
                write_flag=True
                elapsed_on_flag=False

            if write_flag:
                
                depths.append(pieces[28])
                times.append(pieces[0])

    return (depths,times)

def convert_stim_times(stim_times):
    converted_times=[]
    for i in stim_times:
        vls=i.split(':')
        converted_times.append(float(vls[-1])+60*float(vls[-2]))
    return converted_times

def get_delta_f(stim_tms,mn_roi,frame_tms,PREF_WINDOW,POSTF_WINDOW):
    u, ind = np.unique(stim_tms, return_index=True)
    sorted_tms=u[np.argsort(ind)]
    st={}
    st['sorted_tms']=sorted_tms
    st['pre_f']={}
    st['pst_f']={}
    for cr_roi_ind in np.arange(len(mn_roi)):
        st['pre_f'][cr_roi_ind]=[]
        st['pst_f'][cr_roi_ind]=[]
        

    
    for cr_roi_ind in np.arange(len(mn_roi)):
        for crtm in sorted_tms:
            prewindow=[crtm-PREF_WINDOW[0],crtm-PREF_WINDOW[1]]
            pstwindow=[crtm+POSTF_WINDOW[0],crtm+POSTF_WINDOW[1]]
            
            preframe_inds=np.intersect1d(np.where(frame_tms>=prewindow[0]),np.where(frame_tms<=prewindow[1]))
            postframe_inds=np.intersect1d(np.where(frame_tms>=pstwindow[0]),np.where(frame_tms<=pstwindow[1]))
           
            st['pre_f'][cr_roi_ind].append(np.mean(np.array(mn_roi[cr_roi_ind])[preframe_inds]))
            
            st['pst_f'][cr_roi_ind].append(np.mean(np.array(mn_roi[cr_roi_ind])[postframe_inds]))
           
    return st

           
def get_stim_region(logfilein,unique_events=1):
    roi_collect_flag=False
    initflag=True
    xlist=[]
    ylist=[]
    xpixels=[]
    ypixels=[]
    with open(logfilein,'r') as log_file:
        for line in log_file:
            pieces=line.split()
            if pieces[2]=='events:':
                num_of_events=int(pieces[-1])
                break
                roi_collect_flag=False
        for line in log_file:
            pieces=line.split()

            
            if pieces[0]=='Event:':
                roi_collect_flag=False
                if not initflag:
                    
                    xlist.append(xpixels)
                    ylist.append(ypixels)
                    xpixels=[]
                    ypixels=[]



            if roi_collect_flag:
                initflag=False
                vls=pieces[0].split(',')
                xpixels.append(vls[0])

                try:
                    ypixels.append(vls[1])
                except:
                    pdb.set_trace()
            

            if len(pieces)>2:
                if pieces[2] == 'points:':
                    
                    roi_collect_flag=True
    log_file.close()
    #im['xpixels']=xpixels
    #im['ypixels']=ypixels
    xlist.append(xpixels)
    ylist.append(ypixels)
    
    xreturn_list=[]

    yreturn_list=[]

    for cr_event in np.arange(unique_events):
        


        xreturn_list.append([int(i) for i in xlist[cr_event]])
        yreturn_list.append([int(i) for i in ylist[cr_event]])
    
    return (xreturn_list,yreturn_list)
          

           




