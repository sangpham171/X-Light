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
from tkinter.messagebox import *
from tkinter import *
from nexusformat.nexus import *
def read_header_nxs(f,import_XRD):
    a=nxload(f,'r')

    wavelength=float(a.NXentry[0].NXinstrument[0].NXmonochromator[0]["wavelength"])
    k_alpha=[]
    k_alpha.append(wavelength)
    k_alpha.append(0)
    
    scan_config=a.NXentry[0].NXconfig[0]["name"]
    
    actuator_1_1=a.NXentry[0].NXdata[0]["actuator_1_1"]
    data_04=a.NXentry[0].NXdata[0]["data_04"]
    for i in range(len(actuator_1_1)):
        if "Chi" in scan_config:
            import_XRD.chi.append(90-float('%0.2f' % actuator_1_1[i]))
            import_XRD.omega.append(float('%0.2f' % data_04[i]))
        elif "Omega" in scan_config:
            import_XRD.omega.append(float('%0.2f' % actuator_1_1[i]))
            import_XRD.chi.append(90-float('%0.2f' % data_04[i]))

    data_03=a.NXentry[0].NXdata[0]["data_03"]
    for i in range(len(data_03)):
        if "SOLEIL" in a.NXentry[0].NXuser[0]["address"] and "diffabs" in a.NXentry[0].NXnote[1]["data"]:
            import_XRD.twotheta_center.append(16+float('%0.2f' % data_03[i]))
        else:
            import_XRD.twotheta_center.append(float('%0.2f' % data_03[i]))

    data_05=a.NXentry[0].NXdata[0]["data_05"]
    for i in range(len(data_05)):
        import_XRD.phi.append(float('%0.2f' % data_05[i]))

    data=a.NXentry[0].NXdata[0]["data_06"]
    shape=data.shape
    data_dim=len(shape)
    
    if data_dim==2:
        import_XRD.nrow.append(shape[0])
        import_XRD.ncol.append(shape[1])
        import_XRD.row_tick.append(list(range(1,shape[0]+1)))
        import_XRD.col_tick.append(list(range(1,shape[1]+1)))
        import_XRD.center_row.append(shape[0]/2)
        import_XRD.center_col.append(shape[1]/2)

        import_XRD.nfile.append(import_XRD.i)
        import_XRD.nimage_i.append(0)
        import_XRD.image=import_XRD.image+1
        import_XRD.nimage.append(import_XRD.image)

        import_XRD.distance.append(float('NaN'))

        import_XRD.k_alpha.append(k_alpha)
        
        header_info=[]
        header_info.append('User: '+str(a.NXentry[0].NXuser[0]["address"]))
        header_info.append('Note: '+str(a.NXentry[0].NXnote[1]["data"]))
        header_info.append('Scan config: '+str(a.NXentry[0].NXconfig[0]["full name"]))
        header_info.append('Phi: '+str(data_05[0]))
        if "SOLEIL" in a.NXentry[0].NXuser[0]["address"] and "diffabs" in a.NXentry[0].NXnote[1]["data"]:
            header_info.append('Twotheta: '+str(16+data_03[0]))
        else:
            header_info.append('Twotheta: '+str(data_03[0]))
        if "Chi" in scan_config:
            header_info.append('Chi: '+str(90-actuator_1_1[0]))
            header_info.append('Omega: '+str(data_04[0]))
        elif "Omega" in scan_config:
            header_info.append('Omega: '+str(actuator_1_1[0]))
            header_info.append('Chi: '+str(90-data_04[0]))
        
        import_XRD.file_info.append(header_info)

    elif data_dim==3:
        for i in range(shape[0]):
            import_XRD.nrow.append(shape[1])
            import_XRD.ncol.append(shape[2])
            import_XRD.row_tick.append(list(range(1,shape[1]+1)))
            import_XRD.col_tick.append(list(range(1,shape[2]+1)))
            import_XRD.center_row.append(shape[1]/2)
            import_XRD.center_col.append(shape[2]/2)

            import_XRD.nfile.append(import_XRD.i)
            import_XRD.nimage_i.append(i)
            import_XRD.image=import_XRD.image+1
            import_XRD.nimage.append(import_XRD.image)

            import_XRD.distance.append(float('NaN'))

            import_XRD.k_alpha.append(k_alpha)
            
            header_info=[]
            header_info.append('User: '+str(a.NXentry[0].NXuser[0]["address"]))
            header_info.append('Note: '+str(a.NXentry[0].NXnote[1]["data"]))
            header_info.append('Scan config: '+str(a.NXentry[0].NXconfig[0]["full name"]))
            header_info.append('Phi: '+str(data_05[i]))
            if "SOLEIL" in a.NXentry[0].NXuser[0]["address"] and "diffabs" in a.NXentry[0].NXnote[1]["data"]:
                header_info.append('Twotheta: '+str(16+data_03[i]))
            else:
                header_info.append('Twotheta: '+str(data_03[i]))
            if "Chi" in scan_config:
                header_info.append('Chi: '+str(90-actuator_1_1[i]))
                header_info.append('Omega: '+str(data_04[i]))
            elif "Omega" in scan_config:
                header_info.append('Omega: '+str(actuator_1_1[i]))
                header_info.append('Chi: '+str(90-data_04[i]))
            
            import_XRD.file_info.append(header_info)
    else:
        import_XRD.nrow.append(float('NaN'))
        import_XRD.ncol.append(float('NaN'))
        import_XRD.row_tick.append(float('NaN'))
        import_XRD.col_tick.append(float('NaN'))
        import_XRD.center_row.append(float('NaN'))
        import_XRD.center_col.append(float('NaN'))

        import_XRD.nfile.append(import_XRD.i)
        import_XRD.nimage_i.append(0)
        import_XRD.image=import_XRD.image+1
        import_XRD.nimage.append(import_XRD.image)

        import_XRD.distance.append(float('NaN'))

        import_XRD.k_alpha.append(float('NaN'))
        
        header_info=[]
        header_info.append('Scan config: '+str(a.NXentry[0].NXconfig[0]["full name"]))
        header_info.append('Phi: '+str(data_05[0]))
        header_info.append('Twotheta: '+str(data_03[0]))
        if "Chi" in scan_config:
            header_info.append('Chi: '+str(actuator_1_1[0]))
            header_info.append('Omega: '+str(data_04[0]))
        elif "Omega" in scan_config:
            header_info.append('Omega: '+str(actuator_1_1[0]))
            header_info.append('Chi: '+str(data_04[0]))
        
        import_XRD.file_info.append(header_info)
    
#--------------------------------------
def read_data_nxs(f):
    a=nxload(f,'r')
    data=a.NXentry[0].NXdata[0]["data_06"]
    data=np.array(data)
    return(data)
    
    

