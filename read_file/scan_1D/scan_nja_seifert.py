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
def read_nja_seifert(f,self):
    f_open = open(f, "r", encoding="utf-8",errors='ignore')
    kalpha1=float('NaN')
    kalpha2=float('NaN')
    kalpha_ratio=0
    #read file header
    file_info=[]
    text=f_open.readline()
    while "#ScanTable" not in text:
        file_info.append(str(text).strip())

        if "Anode" in text:
            text=text.split()[0]

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

    while text is not None and text is not '':
        range_info=[]
        chi=float('NaN')
        phi=float('NaN')
        omega=float('NaN')
        twotheta=float('NaN')
        while "NoValues" not in text:
            text=f_open.readline()
            range_info.append(str(text).strip())

            if "&Axis=C	&Task=Drive" in text:
                text=text.split()
                chi=float(text[2].split("=")[1])
            if "&Axis=P	&Task=Drive" in text:
                text=text.split()
                phi=float(text[2].split("=")[1])
            #if "_OMEGA" in text:
            #self.omega.append(0)
            #if "_2THETA" in text:
            #self.twotheta.append(0)
            if "&Start=" in text:
                text=text.split()
                twotheta_start=float(text[0].split("=")[1])
                step_size=float(text[2].split("=")[1])
                twotheta_end=float(text[1].split("=")[1])
                twotheta=twotheta_start+(twotheta_end-twotheta_start)/2
                omega=twotheta/2

        self.chi.append(chi)
        self.phi.append(phi)
        self.omega.append(omega)
        self.twotheta.append(twotheta)

        self.range_info.append(range_info)

        data_x=[]
        data_y=[]
        step_count=-1
        text=f_open.readline()
        while (text is not '') and (text is not '\n'):
            data=text.split()
            step_count=step_count+1
            data_x.append(twotheta_start+step_count*step_size)
            if len(data)==1:
                data_y.append(float(data[0]))                  
            if len(data)==2:
                data_y.append(float(data[1]))
            if len(data)==3:
                data_y.append(float(data[2]))

            text=f_open.readline()

        self.data_x.append(data_x)
        self.data_y.append(data_y)    
