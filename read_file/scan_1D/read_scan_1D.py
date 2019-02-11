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

from read_file.scan_1D.scan_uxd_bruker import read_uxd_bruker
from read_file.scan_1D.scan_nja_seifert import read_nja_seifert
from read_file.scan_1D.scan_raw_bruker import read_raw_bruker
from read_file.scan_1D.scan_profile_proto import read_profile_proto
#from read_file.scan_1D.scan_new_xxx import read_new_xxx
from read_file.scan_1D.read_text_scan import read_text_scan

def read_scan_1D(f,self):
    filename=f.split('/')
    filename=filename[len(filename)-1]
    try:
        f_ext=filename.split('.')[1]
    except IndexError:
        f_ext=" "

    #f_ext is the name of file format
    if f_ext in ("uxd","UXD"):
        read_uxd_bruker(f,self)
    elif f_ext in ("nja","NJA"):
        read_nja_seifert(f,self)
    elif f_ext in ("raw","RAW"):
        read_raw_bruker(f,self)
    elif f_ext in ("Profile","PROFILE"):
        read_profile_proto(f,self)
    elif f_ext in ("txt","TXT"):
        read_text_scan(f,self)
    #elif f_ext in ("new","NEW"):
        #read_new_xxx(f,self)
    else:
        showinfo(title="Warning",message="File format "+str(filename)+" is not supported ")
