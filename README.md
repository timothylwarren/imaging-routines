# elife_larvae_2019
Code associated with Elife Submission 2019:

Regulation of subcellular dendritic synapse specificity by axon guidance cues

Emily C. Sales, Emily L. Heckman, Timothy L. Warren, and Chris Q. Doe


Repository consists of Python scripts written by
Timothy Warren, timlwarren AT gmail
as well as R script (PairwiseWilcoxTest.R ) written by Emily Sales and Heckman
and MATLAB Code by Brandon Mark  (supplemental_matlab_code.txt)

Python scripts are to analyze data collected in Slidebook.

Workflow is to 
(1) Read in raw data from tif files and manually select ROIs.
**make_roi.py**

This saves a .pck file with data associated from the experiment.

(2) Make plots of data for different ROIs
**misc_py_files/just_plotting.py**

(3) Example traces from Paper in
**misc_py_files/plot_example_traces_unc5_animal3.py**
**misc_py_files/plot_example_traces_wt_animal1.py**

(4) Summary data in
**summary_py_files/summary_plot_unc5.py**
**sumarray_py_files/summary_plot.py**




