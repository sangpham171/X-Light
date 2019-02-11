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

def read_1D_template(f,self):
    f_open = open(f, "r",errors='ignore')
    # Some python code for beginners:
    #text=f_open.readline() # read line by line in a text document format ASCII
    #text=text.split() # split text in list by space
    #text=text.split('=') # split text in list by =
    #....
    #text=text.strip([char]) # removes characters from both left and right
    #text=text.replace('=',',') # replace = by ,
    #number=float('0.5') #return number from text
    #number=int('0.5') #return integer from text

    #### for byte file use f_open = open(f, "rb") ### more exemple in raw
    #### f_open.seek(0, SEEK_SET)  # to set the position of byte
    #### f_open.read(8) # read 8 bytes
    
    ######read file header
    kalpha1=float('NaN')
    kalpha2=float('NaN')
    kalpha_ratio=0
    
    file_info=[]
    #file_info.append('to be defined')
    #find the value of wavelength####
        #if Anode => path = os.path.dirname(__file__)
                    #path=path.split('\\')
                    #del path[len(path)-1]
                    #path='\\'.join(path)
                            
                    #filename = 'x_ray_source.xrs'
                    #filepath=os.path.join(path, filename)
                    #line_text=f.readline()
                    #while line_text is not None and line_text is not "":
                        #line_text=line_text.split()
                        #if line_text[0] in text:
                            #kalpha1=float(line_text[1])
                            #kalpha2=float(line_text[2])
                            #kalpha_ratio=0.5
                            #break
                        #line_text=f.readline()
        #or directly find the value of kalpha 1, 2, ratio
    
    self.file_info.append(file_info)
    
    self.k_alpha.append(kalpha1)
    self.k_alpha.append(kalpha2)
    self.k_alpha.append(kalpha_ratio)

    #for each scan in the file
        range_info=[]
        self.range_info.append(range_info)
        
        chi=float('NaN')
        phi=float('NaN')
        omega=float('NaN')
        twotheta=float('NaN')

        #find the value of angles phi, khi, omega, theta
            #chi=
            #phi=
            #omega=
            #twotheta=

        self.chi.append(chi)
        self.phi.append(phi)
        self.omega.append(omega)
        self.twotheta.append(twotheta)
        
        data_x=[]
        data_y=[]
        data_y.append('to be defined')
        data_x.append('to be defined')

        self.data_x.append(data_x)
        self.data_y.append(data_y)
