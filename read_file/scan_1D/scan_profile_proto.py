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
import os.path
import sys
import numpy as np
from tkinter.messagebox import *

def read_profile_proto(f,self):
    f_open = open(f, "r",errors='ignore')
    kalpha1=float('NaN')
    kalpha2=float('NaN')
    kalpha_ratio=0
    #read file header
    file_info=[]
    text=f_open.readline()
    while ("Tube" not in text) and (text is not None) and (text is not ''):   
        if text is not "\n":
            file_info.append(str(text).strip())
        if "Number Of Beta Angles" in text:
            num_scan=int(text.split(":")[1])
        if "Number Of Detector" in text:
            num_detector=int(text.split(":")[1])
        if "Wavelength" in text:
            text=text.split(":")[1]

            if getattr(sys, 'frozen', False):
                path = sys._MEIPASS
            elif __file__:
                path = os.path.dirname(__file__)
                path=path.split('\\')
                del path[len(path)-1]
                path='\\'.join(path)
            
            filename = 'x_ray_source.xrs'
            filepath=os.path.join(path, filename)

            f= open(filepath, "r")

            line_text=f.readline()
            while line_text is not None and line_text is not "":
                line_text=line_text.split()
                if line_text[0] in text:
                    kalpha1=float(line_text[1])
                    kalpha2=float(line_text[2])
                    kalpha_ratio=0.5
                    break
                line_text=f.readline()

        text=f_open.readline()

    self.file_info.append(file_info)

    self.k_alpha.append(kalpha1)
    self.k_alpha.append(kalpha2)
    self.k_alpha.append(kalpha_ratio)

    for i in range(num_scan):
        range_info=[]

        chi=float('NaN')
        phi=float('NaN')
        omega=float('NaN')
        twotheta=float('NaN')

        text=f_open.readline()
        range_info.append(str(text).strip())
        if "Phi" in text:
            text=text.split()
            for j in range(num_detector):
                phi=float(text[1].split("=")[1])

        text=f_open.readline()
        range_info.append(str(text).strip())
        if "Psi" in text:
            text=text.split()
            for j in range(num_detector):
                chi=float(text[4*j+3])

        self.chi.append(chi)
        self.phi.append(phi)
        
        self.range_info.append(range_info)

        data_x=[]
        data_y=[]
        for i in range(num_detector):
            data_x.append([])
            data_y.append([])
        text=f_open.readline()
        while ("********" not in text) and (text is not '') and (text is not None):
            data=text.split()
            if len(data)>0:
                try:
                    for j in range(num_detector):
                        data_x[j].append(float(data[j*2]))
                        data_y[j].append(float(data[j*2+1]))
                except ValueError:
                    pass
            
            text=f_open.readline()

        for j in range(num_detector):
            self.data_x.append(data_x[j])
            self.data_y.append(data_y[j])
            self.twotheta.append(np.mean(data_x[j]))
            self.omega.append(np.mean(data_x[j])/2)
