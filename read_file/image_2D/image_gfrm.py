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
def read_header_gfrm(f,import_XRD):
    f_open = open(f, "rb")      
    header_info=[]
    k_alpha=[]
    for i in range(96):
        f_info_line=f_open.read(80).decode("utf-8")
        header_info.append(f_info_line)
        
        f_info=f_info_line.replace(':',' ').split()

        if "ANGLES" in f_info[0]:
            import_XRD.twotheta_center.append(float(f_info[1]))
            import_XRD.omega.append(float(f_info[2]))
            import_XRD.phi.append(float(f_info[3]))
            import_XRD.chi.append(90-float(f_info[4]))  
          
        if "CENTER" in f_info[0]:
            import_XRD.center_row.append(float(f_info[1]))
            import_XRD.center_col.append(float(f_info[2]))
            
        if "NROWS" in f_info[0]:
            nrow=int(f_info[1])
            import_XRD.nrow.append(nrow)
            import_XRD.row_tick.append(list(range(1,nrow+1)))
                
        if "NCOLS" in f_info[0]:
            ncol=int(f_info[1])
            import_XRD.ncol.append(ncol)
            import_XRD.col_tick.append(list(range(1,ncol+1)))
                
        if "WAVELEN" in f_info[0]:
            k_alpha.append(float(f_info[2]))
            k_alpha.append(float(f_info[3]))

        if "DISTANC" in f_info[0]:
            import_XRD.distance.append(float(f_info[1]))
    import_XRD.k_alpha.append(k_alpha)
    import_XRD.file_info.append(header_info)
    import_XRD.nfile.append(import_XRD.i)
    import_XRD.nimage_i.append(0)
    import_XRD.nimage.append(import_XRD.i)
        
#---------------------------------------
def read_data_gfrm(f,nrow,ncol):
    f_open = open(f, "rb")
    nheader_block=None
    for i in range(96):
        f_info_line=f_open.read(80).decode("utf-8")
        f_info=f_info_line.replace(':',' ').split()
        if "HDRBLKS" in f_info[0]:
            nheader_block=int(f_info[1])
            break

    if nheader_block is None:
        return

    f_open = open(f, "rb")
    for i in range(nheader_block):
        f_open.read(512)
        
    data=np.fromstring(f_open.read(nrow*ncol),np.uint8)
    data=data.reshape([nrow,ncol])
    return(data)
