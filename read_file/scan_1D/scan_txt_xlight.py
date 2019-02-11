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
def read_txt_xlight(f,self):
    f_open = open(f, "r", encoding="utf-8",errors='ignore')
    kalpha1=float('NaN')
    kalpha2=float('NaN')
    kalpha_ratio=0
    #read file header
    file_info=[]
    text=f_open.readline()
    file_info.append(str(text).strip())
    
    text=text.split('=')[1]
    text=text.split()

    kalpha1=float(text[0])
    kalpha2=float(text[1])
    kalpha_ratio=float(text[2])

    self.file_info.append(file_info)

    self.k_alpha.append(kalpha1)
    self.k_alpha.append(kalpha2)
    self.k_alpha.append(kalpha_ratio)

    text=f_open.readline()
    while text is not None and text is not '':
        range_info=[]
        chi=float('NaN')
        phi=float('NaN')
        omega=float('NaN')
        twotheta=float('NaN')
        while "twotheta" not in text and text is not None and text is not '':
            text=f_open.readline()
            range_info.append(str(text).strip())

            if "Phi" in text:
                phi=float(text.split('=')[1])
            if "Chi" in text:
                chi=float(text.split('=')[1])
            if "Omega" in text:
                omega=float(text.split('=')[1])
            if "2theta" in text:
                twotheta=float(text.split('=')[1])

        self.chi.append(chi)
        self.phi.append(phi)
        self.omega.append(omega)
        self.twotheta.append(twotheta)

        self.range_info.append(range_info)

        data_x=[]
        data_y=[]
        text=f_open.readline()
        while ('-----' not in text) and (text is not '') and (text is not None):
            data=text.split()
            data_x.append(float(data[0]))
            data_y.append(float(data[1]))                  

            text=f_open.readline()

        self.data_x.append(data_x)
        self.data_y.append(data_y)    
