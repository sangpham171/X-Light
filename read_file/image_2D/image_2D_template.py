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
def read_header_2D_template(f,import_XRD):
    for i in range(number of image in one file):
        header_info=[] # where all header information can be append
        header_info.append('No header information available')
        import_XRD.file_info.append(header_info)

        import_XRD.nrow.append(nrow) # number of pixel in horizontal axis, must be defined, if not must have read_data_2D_template_1 module
        import_XRD.ncol.append(ncol) # number of pixel in vertical axis, must be defined, if not must have read_data_2D_template_1 module
        import_XRD.row_tick.append(list(range(1,nrow+1))) # row tick
        import_XRD.col_tick.append(list(range(1,ncol+1))) # col tick

        # all information about angle and wavelength doesn't need to appear
        # if header doesn't have these information, you must define in the software
        import_XRD.phi.append(float('NaN'))
        import_XRD.chi.append(float('NaN'))
        import_XRD.twotheta_center.append(float('NaN'))
        import_XRD.omega.append(float('NaN'))
        k_alpha=[]
        k_alpha.append(float('NaN'))
        k_alpha.append(float('NaN'))

        import_XRD.center_row.append(nrow/2) # modify if not centered
        import_XRD.center_col.append(ncol/2) # modify if not centered

        import_XRD.distance.append(float('NaN'))

        import_XRD.k_alpha.append(k_alpha)
        import_XRD.nfile.append(import_XRD.i) # index of file
        import_XRD.nimage_i.append(0) # number of image in file, if n images, append(n-1)
        import_XRD.image=import_XRD.image+1
        import_XRD.nimage.append(import_XRD.image) #index of image in total
    
#--------------------------------------
def read_data_2D_template_1(f,nrow,ncol,main,import_XRD):
    tk=Tk()
    Label(tk,text="Dim1=").grid(row=0,column=0) # horizontal dimension of detector
    Label(tk,text="Dim2=").grid(row=1,column=0) # vertical dimension of detector
    Label(tk,text="dtype=").grid(row=2,column=0) #dtype to decode, can be change by other, which is depend on the format
    Label(tk,text="sep=").grid(row=3,column=0) # sep to decode
    Entry_dim1=Entry(tk)        # horizontal dimension of detector
    Entry_dim1.grid(row=0,column=1)
    Entry_dim2=Entry(tk)        # vertical dimension of detector
    Entry_dim2.grid(row=1,column=1)
    Entry_sep=Entry(tk)         # sep to decode
    Entry_sep.grid(row=3,column=1)

    variable = StringVar(tk)
    variable.set('uint32') # default value
    list_var=['uint4','uint8','uint16','uint32','uint64','uint128']     #dtype to decode
    optionmenu1=OptionMenu(tk, variable,*list_var) # option menu for multi choices
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
        import_XRD.dtyp=dtyp    #dtype to decode
        import_XRD.sep=sep      # sep to decode
        
        import_XRD.intensity=np.fromfile(f,dtype=import_XRD.dtyp,sep=import_XRD.sep) # decode data, can be change by the format
        import_XRD.intensity=import_XRD.intensity.reshape([dim1,dim2]) # reshape the image dimension

        for i in range(len(import_XRD.nrow)):
            import_XRD.nrow[i]=dim1     #modify the image dimension
            import_XRD.ncol[i]=dim2      #modify the image dimension
            import_XRD.center_row[i]=dim1/2      #modify the center of image
            import_XRD.center_col[i]=dim2/2      #modify the center of image
            import_XRD.row_tick[i]=list(range(1,dim1+1))     #modify the row tick
            import_XRD.col_tick[i]=list(range(1,dim2+1))     #modify the col tick
        
    button=Button(tk,text="OK",command=lambda: open_data(var,Entry_dim1,Entry_dim2,import_XRD)) # button ok to open data with decode parameters
    button.grid(row=2,column=1)

    main.root.wait_variable(var) # pause the execution until button is clicked

    tk.quit() # quit and destroy the new window
    tk.destroy()
    
    return(import_XRD.intensity)

def read_data_2D_template(f,nrow,ncol,import_XRD): # for image doesn't have dimension in header
    data=np.fromfile(f,dtype=import_XRD.dtyp,sep=import_XRD.sep) # must be change follow the format
    data=data.reshape([nrow,ncol])
    # data can be np.array 2 dimension => one image in one file
    # or data can be np.array 3 dimension => multi image in one file
    # the decode of date depend on your format
    # you can follow the existant format to have an idea
    return(data)

def read_data_2D_template(f,nrow,ncol): # for image have dimension in header
    data=np.fromfile(f) # # must be change follow the format
    data=data.reshape([nrow,ncol])
    # data can be np.array 2 dimension => one image in one file
    # or data can be np.array 3 dimension => multi image in one file
    # the decode of date depend on your format
    # you can follow the existant format to have an idea
    return(data)
    
    

