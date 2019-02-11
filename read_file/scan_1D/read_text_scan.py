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

from read_file.scan_1D.scan_txt_xlight import read_txt_xlight
from read_file.scan_1D.scan_txt_binary import read_txt_binary
#from read_file.scan_1D.scan_txt_new import read_txt_new

def read_text_scan(f,self):
    filename=f.split('/')
    filename=filename[len(filename)-1]

    f_open = open(f, "r", encoding="utf-8",errors='ignore')
    text=f_open.readline()

    #test if file is binary 2theta intensity
    binary=True
    line_text=text
    for i in range(10):
        line_text=line_text.split()
        if len(line_text)==2:
            try:
                float(line_text[0])
                float(line_text[1])
            except ValueError:
                binary=False
                break
        else:
            binary=False
            break
        line_text=f_open.readline()
    #---------------------------

    if binary==True:
        read_txt_binary(f,self)
    elif 'Wavelength' in text:
        read_txt_xlight(f,self)
    #elif 'text' in text:
        #read_txt_new(f,self)
    else:
        showinfo(title="Warning",message="File format "+str(filename)+" is not supported ")

