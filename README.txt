#READ ME
#----COPYRIGHT NOTICE--------------------------------------------------------
#    Project: DECORD2D / Residual stress determination           
#
#    Copyright (C) PHAM Tu Quoc Sang, Institut Jean Lamour, Nancy, France
#
#    Principal author:       PHAM Tu Quoc Sang (sang.phamtuquoc@gmail.com)
#
#----PERMISSION NOTICE--------------------------------------------------------
#    This software is published under the terms of the GNU GPL-3.0-or-later (https://www.gnu.org/licenses/gpl.txt).
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#

###############################

X-Light is an open-source software that is written in Python with a graphical
user interface. X-Light was developed to determine residual stress by X-ray
diffraction. This software can process the 0D, 1D and 2D diffraction data
obtained with laboratory diffractometers or synchrotron radiation. X-Light
provides several options for stress analysis and five functions to fit a peak: Gauss,
Lorentz, Pearson VII, pseudo-Voigt and Voigt. The residual stress is determined
by the conventional sin2ψ method and the fundamental method.

###############################
How to open the program?
######
- open __main__.py on IDLE python
- run module or F5

###############################
How to import a new format?
######
1D data
- (1) Go to read_file\scan_1D folder
- (2) if the file is in format ".txt", open read_text_scan
	- (3) modify the line #from read_file.scan_1D.scan_txt_new import read_txt_new
	- (4) replace 'new' by the name that you want to name your scan, delete '#" 
	- (5) modify the line #elif 'text' in text:
        		#read_txt_new(f,self)
	- (6) replace 'text' by a part of first line in your file
	- (7) replace 'read_txt_new' by the module in the step (3) and (4)
	- (8) go to python, create a new file named "scan_txt_'your file name'"
	- (9) define a new module names "read_txt_new"
	- (8)+(9) open the file scan_1D_template and follow the guide

- (2) if the file is not in format ".txt", open read_scan_1D
	- (3) modify the line #from read_file.scan_1D.scan_new_xxx import read_new_xxx
	- (4) replace 'new_xxx' by the name that you want to name your scan, delete '#" 
	- (5) modify the line #elif f_ext in ("new","NEW"):
        				#read_new_xxx(f,self)
	- (6) replace 'new' by the new format, and read_new_xxx by the module in (3) and (4)
	- (7) replace 'read_txt_new' by the module in the step (3) and (4)
	- (8) go to python, create a new file named "scan_new_xxx'
	- (9) define a new module names "read_new_xxx"
	- (8)+(9) open the file scan_1D_template and follow the guide

- open residual_stress_1D\import_XRD_1D and add your new format in format_ variable

######
2D data
- (1) Go to read_file\image_2D folder
- (2) open read_image_2D
	- (3) modify the line #from read_file.image_2D.image_new import read_header_new, read_data_new
	- (4) replace 'new' by the name that you want to name your scan, delete '#" 
	- (5) modify the line #elif f_ext in ("new" or "NEW"):
        				#read_header_new(f,import_XRD)
			      #elif f_ext in ("new" or "NEW"):
        				#data=read_data_new(f)
	- (6) replace 'new' by the new format and new module in (3) and (4)
	- (8) go to python, create a new file named "image_new'
	- (9) define a new module names "read_header_new" and "read_data_new"
	- (8)+(9) open the file image_2D_template and follow the guide
	- the module read_data_2D_template_1 is an example when the format don't have the image dimension, the scan is binary, a new window will appears to define the image dimensions
	- the module read_data_2D_template_1 is not obligated
	- (10) if the image need somme corrections: open file image_correction
	- (11) modify #from read_file.image_2D.image_correction_new import image_correction_new
	- (12) modify the line #elif "xxxx" in header[5] and "yyyy" in header[3]: #use header to identify your format
        				#data=image_correction_new(data)
	- (13) create a new module image_correction_new in filename image_correction_new
	- (14) open image_correction_template to follow

- open residual_stress_2D\import_XRD_2D and add your new format in format_ variable


###############################
How to add a new material?
######
- open read_file\mat_database.mdb and modify
- the file is a text format


###############################
How to add a new source XRD?
######
- open read_file\x_ray_source.xrs and modify
- the file is a text format






