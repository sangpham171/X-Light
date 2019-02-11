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
def read_header_raw(f,import_XRD): 
    header_info=[]
    header_info.append('No header information available')
    import_XRD.file_info.append(header_info)
    
    import_XRD.nrow.append(float('NaN'))
    import_XRD.ncol.append(float('NaN'))
    import_XRD.row_tick.append(None)
    import_XRD.col_tick.append(None)

    import_XRD.phi.append(float('NaN'))
    import_XRD.chi.append(float('NaN'))
    import_XRD.twotheta_center.append(float('NaN'))
    import_XRD.omega.append(float('NaN'))
    k_alpha=[]
    k_alpha.append(float('NaN'))
    k_alpha.append(float('NaN'))

    import_XRD.center_row.append(float('NaN'))
    import_XRD.center_col.append(float('NaN'))

    import_XRD.distance.append(float('NaN'))

    import_XRD.k_alpha.append(k_alpha)
    import_XRD.nfile.append(import_XRD.i)
    import_XRD.nimage_i.append(0)
    import_XRD.nimage.append(import_XRD.i)
    
#--------------------------------------
def read_data_raw_1(f,nrow,ncol,main,import_XRD):
    tk=Tk()
    Label(tk,text="Dim1=").grid(row=0,column=0)
    Label(tk,text="Dim2=").grid(row=1,column=0)
    Label(tk,text="dtype=").grid(row=2,column=0)
    Label(tk,text="sep=").grid(row=3,column=0)
    Entry_dim1=Entry(tk)
    Entry_dim1.grid(row=0,column=1)
    Entry_dim2=Entry(tk)
    Entry_dim2.grid(row=1,column=1)
    Entry_sep=Entry(tk)
    Entry_sep.grid(row=3,column=1)

    variable = StringVar(tk)
    variable.set('uint32') # default value
    list_var=['uint4','uint8','uint16','uint32','uint64','uint128']
    optionmenu1=OptionMenu(tk, variable,*list_var)
    optionmenu1.grid(row=2,column=1,sticky=W)
    
    var=IntVar()
    import_XRD.intensity=[]
    def open_data(var,Entry_dim1,Entry_dim2,import_XRD):
        var.set(1)
        try:
            dim1=int(Entry_dim1.get())
            dim2=int(Entry_dim2.get())
            dtyp=str(variable.get())
            sep=str(Entry_sep.get())
        except Exception:
            dim1=240
            dim2=560
            dtyp='uint32'
            sep=''
        import_XRD.dtyp=dtyp
        import_XRD.sep=sep
        
        import_XRD.intensity=np.fromfile(f,dtype=import_XRD.dtyp,sep=import_XRD.sep)
        import_XRD.intensity=import_XRD.intensity.reshape([dim1,dim2])

        for i in range(len(import_XRD.nrow)):
            import_XRD.nrow[i]=dim1
            import_XRD.ncol[i]=dim2
            import_XRD.center_row[i]=dim1/2
            import_XRD.center_col[i]=dim2/2
            import_XRD.row_tick[i]=list(range(1,dim1+1))
            import_XRD.col_tick[i]=list(range(1,dim2+1))
        
    button=Button(tk,text="OK",command=lambda: open_data(var,Entry_dim1,Entry_dim2,import_XRD))
    button.grid(row=4,column=1)

    main.root.wait_variable(var)

    tk.quit()
    tk.destroy()
    
    return(import_XRD.intensity)

def read_data_raw(f,nrow,ncol,import_XRD):
    data=np.fromfile(f,dtype=import_XRD.dtyp,sep=import_XRD.sep)
    data=data.reshape([nrow,ncol])
    return(data)
    
    

