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
def read_txt_binary(f,self):
    f_open = open(f, "r", encoding="utf-8",errors='ignore')
    #read file header
    file_info=[]
    self.file_info.append(file_info)

    self.k_alpha.append(float('NaN'))
    self.k_alpha.append(float('NaN'))
    self.k_alpha.append(0)

    self.chi.append(float('NaN'))
    self.phi.append(float('NaN'))
    self.omega.append(float('NaN'))
    self.twotheta.append(float('NaN'))

    range_info=[]
    self.range_info.append(range_info)

    data_x=[]
    data_y=[]
    text=f_open.readline()
    while (text is not '\n') and (text is not '') and (text is not None):
        data=text.split()
        data_x.append(float(data[0]))
        data_y.append(float(data[1]))                  

        text=f_open.readline()

    self.data_x.append(data_x)
    self.data_y.append(data_y)    
