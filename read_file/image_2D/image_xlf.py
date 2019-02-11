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
import numpy as np
def read_header_xlf(f,import_XRD):
    f_open = open(f, "r")      
    header_info=[]
    k_alpha=[]
    for i in range(13):
        f_info_line=f_open.readline()
        header_info.append(f_info_line)
        
        f_info=f_info_line.split("=")

        if "Phi" in f_info[0]:
            import_XRD.phi.append(float(f_info[1]))
        if "Chi" in f_info[0]:
            import_XRD.chi.append(float(f_info[1]))
        if "Omega" in f_info[0]:
            import_XRD.omega.append(float(f_info[1]))
        if "2theta" in f_info[0]:
            import_XRD.twotheta_center.append(float(f_info[1]))
        if "Wavelength" in f_info[0]:
            data=f_info[1].replace("[","")
            data=data.replace("]","")
            data=data.split(",")
            for j in range(len(data)):
                k_alpha.append(float(data[j]))         
        if "Distance" in f_info[0]:
            import_XRD.distance.append(float(f_info[1])) 
        if "NRow" in f_info[0]:
            import_XRD.nrow.append(int(f_info[1]))     
        if "NCol" in f_info[0]:
            import_XRD.ncol.append(int(f_info[1]))
        if "Center Row" in f_info[0]:
            import_XRD.center_row.append(float(f_info[1]))
            f_info_line=f_open.readline()
            row_tick=np.fromstring(f_info_line,dtype=float, sep=" ")
            import_XRD.row_tick.append(row_tick)
        if "Center Col" in f_info[0]:
            import_XRD.center_col.append(float(f_info[1]))
            f_info_line=f_open.readline()
            col_tick=np.fromstring(f_info_line,dtype=float, sep=" ")            
            import_XRD.col_tick.append(col_tick)
                
    import_XRD.k_alpha.append(k_alpha)
    import_XRD.file_info.append(header_info)
    import_XRD.nfile.append(import_XRD.i)
    import_XRD.nimage_i.append(0)
    import_XRD.nimage.append(import_XRD.i)
        
#---------------------------------------
def read_data_xlf(f,nrow,ncol):
    f_open = open(f, "r")  
    for i in range(15):
        f_open.readline()
        
    intensity_2D=[]
    for i in range(nrow):
        f_data=f_open.readline()
        intensity_2D.append(np.fromstring(f_data,dtype=float, sep=" "))
    intensity_2D=np.array(intensity_2D)
    return(intensity_2D)
