#----COPYRIGHT NOTICE--------------------------------------------------------
#    Project: DECORD2D / Residual stress determination           
#
#    Copyright (C) PHAM Tu Quoc Sang, Institut Jean Lamour, Nancy, France
#
#    Principal author:       PHAM Tu Quoc Sang (sang.phamtuquoc@gmail.com  ; tu-quoc-sang.pham@univ-lorraine.fr)
#
#----PERMISSION NOTICE--------------------------------------------------------
#    This software is published under the terms of the GNU GPL-3.0-or-later (https://www.gnu.org/licenses/gpl.txt).
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
from tkinter.messagebox import *

from read_file.image_2D.image_fabio import read_header_fabio, read_data_fabio
from read_file.image_2D.image_gfrm import read_header_gfrm, read_data_gfrm
from read_file.image_2D.image_xlf import read_header_xlf, read_data_xlf
from read_file.image_2D.image_raw import read_header_raw, read_data_raw, read_data_raw_1
from read_file.image_2D.image_nxs import read_header_nxs, read_data_nxs
#from read_file.image_2D.image_new import read_header_new, read_data_new
from read_file.image_2D.image_correction import image_correction

def read_header_2D(i,import_XRD):
    f=import_XRD.file_link[i]
    f_split=f.split('/') 
    filename=f_split[len(f_split)-1]

    try:
        f_ext=filename.split('.')
        f_ext=f_ext[len(f_ext)-1]
    except IndexError:
        f_ext=" "

    if f_ext in ("gfrm" or "GFRM"):
        read_header_gfrm(f,import_XRD)
    elif f_ext in ("xlf" or "XLF"):
        read_header_xlf(f,import_XRD)
    elif f_ext in ("raw" or "RAW"):
        read_header_raw(f,import_XRD)
    elif f_ext in ("nxs" or "NXS"):
        read_header_nxs(f,import_XRD)
    #elif f_ext in ("new" or "NEW"):
        #read_header_new(f,import_XRD)
    else:
        read_header_fabio(f,import_XRD)

def read_data_2D(i,import_XRD):
    f=import_XRD.file_link[import_XRD.nfile[i]]
    nrow=import_XRD.nrow[i]
    ncol=import_XRD.ncol[i]
    
    f_split=f.split('/')
    filename=f_split[len(f_split)-1]

    try:
        f_ext=filename.split('.')
        f_ext=f_ext[len(f_ext)-1]
    except IndexError:
        f_ext=" "

    #f_ext is the extension of the file format
    if f_ext in ("gfrm" or "GFRM"):
        data=read_data_gfrm(f,nrow,ncol)
    elif f_ext in ("xlf" or "XLF"):
        data=read_data_xlf(f,nrow,ncol)
    elif f_ext in ("raw" or "RAW"):
        data=read_data_raw(f,nrow,ncol,import_XRD)
    elif f_ext in ("nxs" or "NXS"):
        data=read_data_nxs(f)
    #elif f_ext in ("new" or "NEW"):
        #data=read_data_new(f)
    else:
        data=read_data_fabio(f)

    if len(data)==0:
        showinfo(title="Warning",message="Can not read data of "+str(filename))
        return

    data=image_correction(import_XRD.file_info[i],data)
            
    return(data)

def read_data_2D_1(i,import_XRD,main):
    f=import_XRD.file_link[import_XRD.nfile[i]]
    nrow=import_XRD.nrow[i]
    ncol=import_XRD.ncol[i]
    
    f_split=f.split('/')
    filename=f_split[len(f_split)-1]

    try:
        f_ext=filename.split('.')
        f_ext=f_ext[len(f_ext)-1]
    except IndexError:
        f_ext=" "
    
    if f_ext in ("gfrm" or "GFRM"):
        data=read_data_gfrm(f,nrow,ncol)
    elif f_ext in ("xlf" or "XLF"):
        data=read_data_xlf(f,nrow,ncol)
    elif f_ext in ("raw" or "RAW"):
        data=read_data_raw_1(f,nrow,ncol,main,import_XRD)
    elif f_ext in ("nxs" or "NXS"):
        data=read_data_nxs(f)
    #elif f_ext in ("new" or "NEW"):
        #data=read_data_new_1(f)
    else:
        data=read_data_fabio(f)

    if len(data)==0:
        showinfo(title="Warning",message="Can not read data of "+str(filename))
        return

    data=image_correction(import_XRD.file_info[i],data)
            
    return(data)
