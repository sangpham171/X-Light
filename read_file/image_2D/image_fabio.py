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
import fabio
from tkinter.messagebox import *
def read_header_fabio(f,import_XRD):
    img=fabio.open(f)
    header_info=img.header
    import_XRD.file_info.append(list(header_info.items()))
    import_XRD.nrow.append(img.dim1)
    import_XRD.ncol.append(img.dim2)

    import_XRD.row_tick.append(list(range(1,img.dim1+1)))
    import_XRD.col_tick.append(list(range(1,img.dim2+1)))
    
    header_key=list(header_info.keys())
    angles=["ANGLES"]
    center=["CENTER"]
    wavelength=["WAVELEN"]
    distance=["DISTANC"]
         
    k_alpha=[]
    for i in range(len(header_key)):
        key=header_key[i]
        if key in angles:
            f_info=header_info[key].split()
            import_XRD.twotheta_center.append(float(f_info[0]))
            import_XRD.omega.append(float(f_info[1]))
            import_XRD.phi.append(float(f_info[2]))
            import_XRD.chi.append(90-float(f_info[3]))  
          
        if key in center:
            f_info=header_info[key].split()
            import_XRD.center_row.append(float(f_info[0]))
            import_XRD.center_col.append(float(f_info[1]))
                
        if key in wavelength:
            f_info=header_info[key].split()
            k_alpha.append(float(f_info[1]))
            k_alpha.append(float(f_info[2]))

        if key in distance:
            f_info=header_info[key].split()
            import_XRD.distance.append(float(f_info[1]))

    if "ANGLES" not in header_key:
        if "Phi" not in header_key:
            import_XRD.phi.append(float('NaN'))
        if "Chi" not in header_key:
            import_XRD.chi.append(float('NaN'))
        if "2Theta" not in header_key:
            import_XRD.twotheta_center.append(float('NaN'))
        if "Theta" not in header_key:
            import_XRD.omega.append(float('NaN'))
    if "WAVELEN" not in header_key:
        k_alpha.append(float('NaN'))
        k_alpha.append(float('NaN'))
    if "CENTER" not in header_key:
        import_XRD.center_row.append(img.dim1/2)
        import_XRD.center_col.append(img.dim2/2)
    if "DISTANC" not in header_key:
        import_XRD.distance.append(float('NaN'))

    import_XRD.k_alpha.append(k_alpha)
    import_XRD.nfile.append(import_XRD.i)
    import_XRD.nimage_i.append(0)
    import_XRD.nimage.append(import_XRD.i)
    
#---------------------------------------
def read_data_fabio(f):
    img=fabio.open(f)
    data=img.data
    return(data)
