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

def read_uxd_bruker(f,self):
    f_open = open(f, "r",errors='ignore')
    #read file header
    file_info=[]
    text=f_open.readline()
    while ("Data for" not in text) and (text is not None) and (text is not ''):
        text=f_open.readline()
        if text is not "\n":
            file_info.append(str(text).strip())
        if "_WL1" in text:
            self.k_alpha.append(float(text.split("=")[1]))
        if "_WL2" in text:
            self.k_alpha.append(float(text.split("=")[1]))
        if "_WLRATIO" in text:
            self.k_alpha.append(float(text.split("=")[1]))

    self.file_info.append(file_info)
    
    if len(self.k_alpha)==0:
        showinfo(title="Warning",message="Can not read wavelength info")
        return

    while (text is not None) and (text is not ''):
        range_info=[]
        while "PSD" not in text:
            text=f_open.readline()
            range_info.append(str(text).strip())
            if "_KHI" in text:
                self.chi.append(float(text.split("=")[1]))
            if "_PHI" in text:
                self.phi.append(float(text.split("=")[1]))
            if "_THETA" in text:
                self.omega.append(float(text.split("=")[1]))
            if "_2THETA" in text:
                self.twotheta.append(float(text.split("=")[1]))
            if "_STEPSIZE" in text:
                step_size=float(text.split("=")[1])
            if "_START" in text:
                twotheta_start=float(text.split("=")[1])
            
        self.range_info.append(range_info)

        data_x=[]
        data_y=[]
        step_count=-1
        text=f_open.readline()
        while ("Data for" not in text) and (text is not '') and (text is not None):
            data=text.split()
            if len(data)>0:
                try:
                    data_y.append(float(data[len(data)-1]))
                except ValueError:
                    pass
                else:
                    step_count=step_count+1
                    data_x.append(twotheta_start+step_count*step_size)
            
            text=f_open.readline()

        self.data_x.append(data_x)
        self.data_y.append(data_y)
