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
from tkinter.filedialog import *
from tkinter.ttk import Progressbar
import math as math
import numpy as np
from read_file.image_2D.read_image_2D import read_data_2D

############################################
def export_original_data(nfile,nimage,nimage_i,import_XRD,main):
    f=asksaveasfile(title="Export data",mode='w',defaultextension=".xlf",filetypes=[('X-Light format','.xlf'),('all files','.*')])
    if f is not None and f is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = 3

        f_split=(import_XRD.file_link[nfile]).split("/");    filename=f_split[len(f_split)-1]
        rotate=import_XRD.rotate
        flip=import_XRD.flip

        progress["value"] = progress["value"]+1
        progress.update()

        data=read_data_2D(nimage,import_XRD)
        if len(data.shape)==3:
            data=data[nimage_i]

        if len(data)==0:
            showinfo(title="Warning",message="Can not read data of "+str(filename))
            return

        progress["value"] = progress["value"]+1
        progress.update()

        if rotate==0:
            nrow=import_XRD.nrow[nimage]
            ncol=import_XRD.ncol[nimage]
            center_row=import_XRD.center_row[nimage]
            center_col=import_XRD.center_col[nimage]
            row_tick=import_XRD.row_tick[nimage]
            col_tick=import_XRD.col_tick[nimage]
                
        if rotate==90:
            data=np.rot90(data,k=1,axes=(0, 1))
            nrow=import_XRD.ncol[nimage]
            ncol=import_XRD.nrow[nimage]
            center_row=import_XRD.center_col[nimage]
            center_col=import_XRD.center_row[nimage]
            row_tick=import_XRD.col_tick[nimage]
            col_tick=import_XRD.row_tick[nimage]
                
        if rotate==180:
            data=np.rot90(data,k=2,axes=(0, 1))
            nrow=import_XRD.nrow[nimage]
            ncol=import_XRD.ncol[nimage]
            center_row=import_XRD.center_row[nimage]
            center_col=import_XRD.center_col[nimage]
            row_tick=import_XRD.row_tick[nimage]
            col_tick=import_XRD.col_tick[nimage]
                    
        if rotate==270:
            data=np.rot90(data,k=3,axes=(0, 1))
            nrow=import_XRD.ncol[nimage]
            ncol=import_XRD.nrow[nimage]
            center_row=import_XRD.center_col[nimage]
            center_col=import_XRD.center_row[nimage]
            row_tick=import_XRD.col_tick[nimage]
            col_tick=import_XRD.row_tick[nimage]

        if flip==1:
            data=np.flip(data,axis=0)
        if flip==2:
            data=np.flip(data,axis=1)
                
        f.write("Phi="+str(import_XRD.phi[nimage])+"\n")
        f.write("Chi="+str(import_XRD.chi[nimage])+"\n")
        f.write("Omega="+str(import_XRD.omega[nimage])+"\n")
        f.write("2theta="+str(import_XRD.twotheta_center[nimage])+"\n")
        f.write("Wavelength="+str(import_XRD.k_alpha[nimage])+"\n")
        f.write("Distance="+str(import_XRD.distance[nimage])+"\n")
        f.write("------------------------------------------\n")
        f.write("NRow="+str(nrow)+"\n")
        f.write("Center Row="+str(center_row)+"\n")
        for i in range(nrow):
            f.write(str(row_tick[i])+" ")
        f.write("\n")
        f.write("NCol="+str(ncol)+"\n")
        f.write("Center Col="+str(center_col)+"\n")
        for i in range(ncol):
            f.write(str(col_tick[i])+" ")
        f.write("\n")
        f.write("------------------------------------------\n")
        f.write("------------------------------------------\n")

        progress["value"] = progress["value"]+1
        progress.update()

        for i in range(nrow):
            f.write(" ".join(str(e) for e in data[i]))
            if i<nrow-1:
                f.write("\n")

        progress["value"] = progress["value"]+1
        progress.update()

    f.close()
    for widget in main.Frame1_2.winfo_children():
        widget.destroy()
    main.root.mainloop()


def export_all_original_data(import_XRD,main):
    location=askdirectory(title="Please choose a directory")
    if location is not None and location is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(import_XRD.nfile)

        rotate=import_XRD.rotate
        flip=import_XRD.flip

        for i in range(len(import_XRD.nfile)):   
            progress["value"] = progress["value"]+1
            progress.update()
                    
            f_split=(import_XRD.file_link[import_XRD.nfile[i]]).split("/");    filename=f_split[len(f_split)-1]                    
            name=str(location)+'/'+str(filename.split('.')[0])+'_'+str(import_XRD.nimage_i[i])+'.xlf'                    
            f=open(name,'w')

            data=read_data_2D(i,import_XRD)
            if len(data.shape)==3:
                data=data[import_XRD.nimage_i[i]]

            if len(data)==0:
                showinfo(title="Warning",message="Can not read data of "+str(filename))
                return

            if rotate==0:
                nrow=import_XRD.nrow[i]
                ncol=import_XRD.ncol[i]
                center_row=import_XRD.center_row[i]
                center_col=import_XRD.center_col[i]
                row_tick=import_XRD.row_tick[i]
                col_tick=import_XRD.col_tick[i]
                    
            if rotate==90:
                data=np.rot90(data,k=1,axes=(0, 1))
                nrow=import_XRD.ncol[i]
                ncol=import_XRD.nrow[i]
                center_row=import_XRD.center_col[i]
                center_col=import_XRD.center_row[i]
                row_tick=import_XRD.col_tick[i]
                col_tick=import_XRD.row_tick[i]
                    
            if rotate==180:
                data=np.rot90(data,k=2,axes=(0, 1))
                nrow=import_XRD.nrow[i]
                ncol=import_XRD.ncol[i]
                center_row=import_XRD.center_row[i]
                center_col=import_XRD.center_col[i]
                row_tick=import_XRD.row_tick[i]
                col_tick=import_XRD.col_tick[i]
                        
            if rotate==270:
                data=np.rot90(data,k=3,axes=(0, 1))
                nrow=import_XRD.ncol[i]
                ncol=import_XRD.nrow[i]
                center_row=import_XRD.center_col[i]
                center_col=import_XRD.center_row[i]
                row_tick=import_XRD.col_tick[i]
                col_tick=import_XRD.row_tick[i]

            if flip==1:
                data=np.flip(data,axis=0)
            if flip==2:
                data=np.flip(data,axis=1)
                    
            f.write("Phi="+str(import_XRD.phi[i])+"\n")
            f.write("Chi="+str(import_XRD.chi[i])+"\n")
            f.write("Omega="+str(import_XRD.omega[i])+"\n")
            f.write("2theta="+str(import_XRD.twotheta_center[i])+"\n")
            f.write("Wavelength="+str(import_XRD.k_alpha[i])+"\n")
            f.write("Distance="+str(import_XRD.distance[i])+"\n")
            f.write("------------------------------------------\n")
            f.write("NRow="+str(nrow)+"\n")
            f.write("Center Row="+str(center_row)+"\n")
            for j in range(nrow):
                f.write(str(row_tick[j])+" ")
            f.write("\n")
            f.write("NCol="+str(ncol)+"\n")
            f.write("Center Col="+str(center_col)+"\n")
            for j in range(ncol):
                f.write(str(col_tick[j])+" ")
            f.write("\n")
            f.write("------------------------------------------\n")
            f.write("------------------------------------------\n")

            progress["value"] = progress["value"]+1
            progress.update()

            for i in range(nrow):
                f.write(" ".join(str(e) for e in data[i]))
                if i<nrow-1:
                    f.write("\n")
            
            f.close()
                        
    for widget in main.Frame1_2.winfo_children():
        widget.destroy()
    main.root.mainloop()


def export_calib_data(calib_2D,angles_modif,import_XRD,main):
    from residual_stress_2D.calib_XRD_2D import calib_pyFai
    
    f=asksaveasfile(title="Export data",mode='w',defaultextension=".xlf",filetypes=[('X-Light format','.xlf'),('all files','.*')])
    if f is not None and f is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = 3
        
        rotate=import_XRD.rotate
        flip=import_XRD.flip

        if calib_2D.angles_modif_valid==True:
            twotheta_x=angles_modif.twotheta_x
            gamma_y=angles_modif.gamma_y
            phi=angles_modif.phi[calib_2D.nimage]
            chi=angles_modif.chi[calib_2D.nimage]
            omega=angles_modif.omega[calib_2D.nimage]
            twotheta_center=angles_modif.twotheta_center[calib_2D.nimage]
        else:
            twotheta_x=calib_2D.twotheta_x
            gamma_y=calib_2D.gamma_y
            phi=calib_2D.phi[calib_2D.nimage]
            chi=calib_2D.chi[calib_2D.nimage]
            omega=calib_2D.omega[calib_2D.nimage]
            twotheta_center=calib_2D.twotheta_center[calib_2D.nimage]

        progress["value"] = progress["value"]+1
        progress.update()
    
        data=read_data_2D(calib_2D.nimage,import_XRD)

        if len(data.shape)==3:
            data=data[import_XRD.nimage_i[calib_2D.nimage]]

        if len(data)==0:
            showinfo(title="Warning",message="Can not read data of "+str(filename))
            return

        if rotate==0:
            nrow=import_XRD.nrow[calib_2D.nimage]
            ncol=import_XRD.ncol[calib_2D.nimage]
            center_row=import_XRD.center_row[calib_2D.nimage]
            center_col=import_XRD.center_col[calib_2D.nimage]
                                          
        if rotate==90:
            data=np.rot90(data,k=1,axes=(0, 1))
            nrow=import_XRD.ncol[calib_2D.nimage]
            ncol=import_XRD.nrow[calib_2D.nimage]
            center_row=import_XRD.center_col[calib_2D.nimage]
            center_col=import_XRD.center_row[calib_2D.nimage]
                
        if rotate==180:
            data=np.rot90(data,k=2,axes=(0, 1))
            nrow=import_XRD.nrow[calib_2D.nimage]
            ncol=import_XRD.ncol[calib_2D.nimage]
            center_row=import_XRD.center_row[calib_2D.nimage]
            center_col=import_XRD.center_col[calib_2D.nimage]
                    
        if rotate==270:
            data=np.rot90(data,k=3,axes=(0, 1))
            nrow=import_XRD.ncol[calib_2D.nimage]
            ncol=import_XRD.nrow[calib_2D.nimage]
            center_row=import_XRD.center_col[calib_2D.nimage]
            center_col=import_XRD.center_row[calib_2D.nimage]
            
        if flip==1:
            data=np.flip(data,axis=0)
            
        if flip==2:
            data=np.flip(data,axis=1)

        progress["value"] = progress["value"]+1
        progress.update()
        calib=calib_pyFai(import_XRD,data,nrow,ncol,center_row,center_col,twotheta_center)

        if len(calib)>0:
            data=calib[0]
        else:
            showinfo(title="Warning",message="Can not calib file "+str(filename))
            return

        if float(calib_2D.Check_twotheta_flip.get())==1:
            data=np.flip(data,axis=1)
        
        if len(data)>0:
            progress["value"] = progress["value"]+1
            progress.update()
            nrow=len(gamma_y)
            ncol=len(twotheta_x)
            
            f.write("Phi="+str(phi)+"\n")
            f.write("Chi="+str(chi)+"\n")
            f.write("Omega="+str(omega)+"\n")
            f.write("2theta="+str(twotheta_center)+"\n")
            f.write("Wavelength="+str(import_XRD.k_alpha[calib_2D.nimage])+"\n")
            f.write("Distance="+str(import_XRD.distance[calib_2D.nimage])+"\n")
            f.write("------------------------------------------\n")
            f.write("NRow="+str(nrow)+"\n")
            f.write("Center Row="+str(center_row)+"\n")
            for i in range(nrow):
                f.write(str(gamma_y[i])+" ")
            f.write("\n")
            f.write("NCol="+str(ncol)+"\n")
            f.write("Center Col="+str(center_col)+"\n")
            for i in range(ncol):
                f.write(str(twotheta_x[i])+" ")
            f.write("\n")
            f.write("------------------------------------------\n")
            f.write("------------------------------------------\n")

            progress["value"] = progress["value"]+1
            progress.update()

            for i in range(nrow):
                f.write(" ".join(str(e) for e in data[i]))
                f.write("\n")

            progress["value"] = progress["value"]+1
            progress.update()
    for widget in main.Frame1_2.winfo_children():
        widget.destroy()
    f.close()
    main.root.mainloop()

def export_all_calib_data(calib_2D,angles_modif,import_XRD,main):
    from residual_stress_2D.calib_XRD_2D import calib_pyFai
    
    location=askdirectory(title="Please choose a directory")
    if location is not None and location is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(import_XRD.nfile)

        rotate=import_XRD.rotate
        flip=import_XRD.flip

        for i in range(len(import_XRD.nfile)):
            progress["value"] = progress["value"]+1
            progress.update()

            f_split=(import_XRD.file_link[import_XRD.nfile[i]]).split("/");    filename=f_split[len(f_split)-1]                    
            name=str(location)+'/calib_'+str(filename.split('.')[0])+'_'+str(import_XRD.nimage_i[i])+'.xlf'                    
            f=open(name,'w')

            if calib_2D.angles_modif_valid==True:
                twotheta_x=angles_modif.twotheta_x
                gamma_y=angles_modif.gamma_y
                phi=angles_modif.phi[i]
                chi=angles_modif.chi[i]
                omega=angles_modif.omega[i]
                twotheta_center=angles_modif.twotheta_center[i]
            else:
                twotheta_x=calib_2D.twotheta_x
                gamma_y=calib_2D.gamma_y
                phi=calib_2D.phi[i]
                chi=calib_2D.chi[i]
                omega=calib_2D.omega[i]
                twotheta_center=calib_2D.twotheta_center[i]
        
            data=read_data_2D(i,import_XRD)

            if len(data.shape)==3:
                data=data[import_XRD.nimage_i[i]]

            if len(data)==0:
                showinfo(title="Warning",message="Can not read data of "+str(filename))
                return

            if rotate==0:
                nrow=import_XRD.nrow[i]
                ncol=import_XRD.ncol[i]
                center_row=import_XRD.center_row[i]
                center_col=import_XRD.center_col[i]
                                              
            if rotate==90:
                data=np.rot90(data,k=1,axes=(0, 1))
                nrow=import_XRD.ncol[i]
                ncol=import_XRD.nrow[i]
                center_row=import_XRD.center_col[i]
                center_col=import_XRD.center_row[i]
                    
            if rotate==180:
                data=np.rot90(data,k=2,axes=(0, 1))
                nrow=import_XRD.nrow[i]
                ncol=import_XRD.ncol[i]
                center_row=import_XRD.center_row[i]
                center_col=import_XRD.center_col[i]
                        
            if rotate==270:
                data=np.rot90(data,k=3,axes=(0, 1))
                nrow=import_XRD.ncol[i]
                ncol=import_XRD.nrow[i]
                center_row=import_XRD.center_col[i]
                center_col=import_XRD.center_row[i]
                
            if flip==1:
                data=np.flip(data,axis=0)
                
            if flip==2:
                data=np.flip(data,axis=1)

            calib=calib_pyFai(import_XRD,data,nrow,ncol,center_row,center_col,twotheta_center)
            if len(calib)>0:
                data=calib[0]   
            else:
                showinfo(title="Warning",message="Can not calib file "+str(filename))
                return
            
            if float(calib_2D.Check_twotheta_flip.get())==1:
                data=np.flip(data,axis=1)
                
            if len(data)>0:
                progress["value"] = progress["value"]+1
                progress.update()
                data=calib[0]
                nrow=len(gamma_y)
                ncol=len(twotheta_x)
                
                f.write("Phi="+str(phi)+"\n")
                f.write("Chi="+str(chi)+"\n")
                f.write("Omega="+str(omega)+"\n")
                f.write("2theta="+str(twotheta_center)+"\n")
                f.write("Wavelength="+str(import_XRD.k_alpha[i])+"\n")
                f.write("Distance="+str(import_XRD.distance[i])+"\n")
                f.write("------------------------------------------\n")
                f.write("NRow="+str(nrow)+"\n")
                f.write("Center Row="+str(center_row)+"\n")
                for j in range(nrow):
                    f.write(str(gamma_y[j])+" ")
                f.write("\n")
                f.write("NCol="+str(ncol)+"\n")
                f.write("Center Col="+str(center_col)+"\n")
                for j in range(ncol):
                    f.write(str(twotheta_x[j])+" ")
                f.write("\n")
                f.write("------------------------------------------\n")
                f.write("------------------------------------------\n")

                progress["value"] = progress["value"]+1
                progress.update()

                for i in range(nrow):
                    f.write(" ".join(str(e) for e in data[i]))
                    f.write("\n")
            f.close()

    for widget in main.Frame1_2.winfo_children():
        widget.destroy()   
    main.root.mainloop()

    
def export_fit_data(i_graph,main_calcul,calib_2D,main):
    f=asksaveasfile(title="Export data",mode='w',defaultextension=".text",filetypes=[('text files','.txt'),('all files','.*')])
    if f is not None and f is not '':
        i=calib_2D.nimage*main_calcul.gamma_number+i_graph
        j_start=int(main_calcul.gamma_f_index+i_graph*main_calcul.gamma_step)
        j_end=int(main_calcul.gamma_f_index+(i_graph+1)*main_calcul.gamma_step)
        
        f.write("Phi="+str(main_calcul.phi[calib_2D.nimage])+"°\n")
        f.write("Chi="+str(main_calcul.chi[calib_2D.nimage])+"°\n")
        f.write("Omega="+str(main_calcul.omega[calib_2D.nimage])+"°\n")
        f.write("Peak position="+str(main_calcul.peaks_position[i])+"+ +/- "+str(main_calcul.error_peaks_position[i])+"°\n")
        f.write("FWHM="+str(main_calcul.FWHM[i])+"° +/- "+str(main_calcul.error_FWHM[i])+"°\n")
        f.write("Peak intensity="+str(main_calcul.peak_intensity[i])+" +/- "+str(main_calcul.error_peak_intensity[i])+"\n")
        f.write("a="+str(main_calcul.a[i])+"\n")
        f.write("r="+str(main_calcul.r[i])+"\n")
        f.write("gamma integrate from "+str(int(main_calcul.gamma_y[j_start]))+"° to "+str(int(main_calcul.gamma_y[j_end]))+"°\n")
        f.write(" two_theta(°)\t")
        f.write("instensity\t")
        f.write("background\t")
        f.write("substrat_background\t")
        f.write("   I_kalpha1\t")
        f.write("   I_kalpha2\t")
        f.write("I_Pearson_VII fit\t")
        f.write("\n")

        for j in range(len(main_calcul.data_x_limit)):
            f.write(str("%10.4g" % main_calcul.data_x_limit[j])+"\t")
            f.write(str("%10.4g" % main_calcul.data_y_limit[i][j])+"\t")
            f.write(str("%10.4g" % main_calcul.data_y_background_fit[i][j])+"\t")
            f.write(str("%19.4g" % main_calcul.data_y_net[i][j])+"\t")
            f.write(str("%10.4g" % main_calcul.data_y_k1_fit[i][j])+"\t")
            f.write(str("%10.4g" % main_calcul.data_y_k2_fit[i][j])+"\t")
            f.write(str("%19.4g" % main_calcul.data_y_fit_total[i][j])+"\t")
            f.write("\n")
    f.close()
    main.root.mainloop()
#-------------------------------------------
def export_all_fit_data(main_calcul,calib_2D,main):
    f=asksaveasfile(title="Export data",mode='w',defaultextension=".text",filetypes=[('text files','.txt'),('all files','.*')])
    if f is not None and f is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(main_calcul.phi)*main_calcul.gamma_number

        for nimage in range(len(main_calcul.phi)):
            for i_graph in range(main_calcul.gamma_number):
                progress["value"] = progress["value"]+1
                progress.update()
                
                i=calib_2D.nimage*main_calcul.gamma_number+i_graph
                j_start=int(main_calcul.gamma_f_index+i_graph*main_calcul.gamma_step)
                j_end=int(main_calcul.gamma_f_index+(i_graph+1)*main_calcul.gamma_step)
          
                f.write("Phi="+str(main_calcul.phi[nimage])+"°\n")
                f.write("Chi="+str(main_calcul.chi[nimage])+"°\n")
                f.write("Omega="+str(main_calcul.omega[nimage])+"°\n")
                f.write("peak position="+str(main_calcul.peaks_position[i])+"° +/- "+str(main_calcul.error_peaks_position[i])+"°\n")
                f.write("FWHM="+str(main_calcul.FWHM[i])+"° +/- "+str(main_calcul.error_FWHM[i])+"°\n")
                f.write("Peak intensity="+str(main_calcul.peak_intensity[i])+" +/- "+str(main_calcul.error_peak_intensity[i])+"\n")
                f.write("a="+str(main_calcul.a[i])+"\n")
                f.write("r="+str(main_calcul.r[i])+"\n")
                f.write("gamma integrate from "+str(int(main_calcul.gamma_y[j_start]))
                             +"° to "+str(int(main_calcul.gamma_y[j_end]))+"°\n")
                f.write(" two_theta(°)\t")
                f.write("instensity\t")
                f.write("background\t")
                f.write("substrat_background\t")
                f.write("   I_kalpha1\t")
                f.write("   I_kalpha2\t")
                f.write("I_Pearson_VII fit\t")
                f.write("\n")

                for j in range(len(main_calcul.data_x_limit)):
                    try:
                        f.write(str(main_calcul.data_x_limit[j])+"\t")
                        f.write(str(main_calcul.data_y_limit[i][j])+"\t")
                        f.write(str(main_calcul.data_y_background_fit[i][j])+"\t")
                        f.write(str(main_calcul.data_y_net[i][j])+"\t")
                        f.write(str(main_calcul.data_y_k1_fit[i][j])+"\t")
                        f.write(str(main_calcul.data_y_k2_fit[i][j])+"\t")
                        f.write(str(main_calcul.data_y_fit_total[i][j])+"\t")
                        f.write("\n")
                    except (IndexError,ValueError):
                        pass
                f.write("--------------------------------------\n")
                f.write("--------------------------------------\n")
        f.close()
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()  
    main.root.mainloop()
#----------------------------------------------
def export_all_stress_data(calib_2D,main_calcul,stress_calcul,main):
    f=asksaveasfile(title="Export data",mode='w',defaultextension=".text",filetypes=[('text files','.txt'),('all files','.*')])
    if f is not None and f is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(stress_calcul.phi)+2

        if stress_calcul.stress_valid>=1:
            f.write("SIN2PSI METHOD\n")
            for i in range(len(stress_calcul.liste_phi)):
                f.write("Phi= "+str(stress_calcul.liste_phi[i])+"°")
                f.write("Linear fit: "+"sigma= "+str(stress_calcul.sigma_phi_linear[i])+"+/-"+str(stress_calcul.error_sigma_phi_linear[i])+"MPa"+"\n")
                f.write("Elliptic fit: "+"sigma= "+str(stress_calcul.sigma_phi_elliptic[i])+"+/-"+str(stress_calcul.error_sigma_phi_elliptic[i])+"MPa"+"\n")
                f.write("Elliptic fit: "+"shear= "+str(stress_calcul.shear_phi_elliptic[i])+"+/-"+str(stress_calcul.error_shear_phi_elliptic[i])+"MPa"+"\n")
                f.write("-------------------\n")
        f.write("---------------------------------------------------- \n")
        f.write("---------------------------------------------------- \n")
        
        progress["value"] = progress["value"]+1
        progress.update()
        f.write("FUNDAMENTAL METHOD \n")
        if len(stress_calcul.liste_phi)==1 and stress_calcul.length_strain>=2:
            f.write("---Uniaxial stress----- \n")
            f.write('sigma = '+str('%0.1f' % stress_calcul.sigma_phi_uniaxial[0])+"+/-"+str('%0.1f' % stress_calcul.error_sigma_phi_uniaxial[0])+"MPa"+"\n")

        if len(stress_calcul.liste_phi)==1 and stress_calcul.length_strain>=3:
            f.write("---Uniaxial+Shear stress----- \n")
            f.write('sigma = '+str('%0.1f' % stress_calcul.sigma_phi_uniaxial_shear[0])+"+/-"+str('%0.1f' % stress_calcul.error_sigma_phi_uniaxial_shear[0])+"MPa"+"\n")
            f.write('shear = '+str('%0.1f' % stress_calcul.shear_phi_uniaxial_shear[0])+"+/-"+str('%0.1f' % stress_calcul.error_shear_phi_uniaxial_shear[0])+"MPa"+"\n")

        if len(stress_calcul.liste_phi)>=2 and stress_calcul.length_strain==3:
            f.write("---Biaxial stress----- \n")
            f.write('sigma 11 = '+str(stress_calcul.tensor_biaxial[0][0])+"+/-"+str(stress_calcul.tensor_biaxial[1][0,0]**0.5)+"MPa"+"\n")
            f.write('sigma 22 = '+str(stress_calcul.tensor_biaxial[0][1])+"+/-"+str(stress_calcul.tensor_biaxial[1][1,1]**0.5)+"MPa"+"\n")     
            f.write("---------------------- \n")

        if len(stress_calcul.liste_phi)>=2 and stress_calcul.length_strain>=4:
            f.write("---Biaxial stress----- \n")
            f.write('sigma 11 = '+str(stress_calcul.tensor_biaxial[0][0])+"+/-"+str(stress_calcul.tensor_biaxial[1][0,0]**0.5)+"MPa"+"\n")
            f.write('sigma 22 = '+str(stress_calcul.tensor_biaxial[0][2])+"+/-"+str(stress_calcul.tensor_biaxial[1][2,2]**0.5)+"MPa"+"\n")     
            f.write('sigma 12 = sigma 21 = '+str(stress_calcul.tensor_biaxial[0][1])+"+/-"+str(stress_calcul.tensor_biaxial[1][1,1]**0.5)+"MPa"+"\n")
            f.write("---------------------- \n")

        if len(stress_calcul.liste_phi)>=2 and stress_calcul.length_strain==5:     
            f.write("---Biaxial+shear stress----- \n")
            f.write('sigma 11 = '+str(stress_calcul.tensor_biaxial_shear[0][0])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][0,0]**0.5)+"MPa"+"\n")
            f.write('sigma 22 = '+str(stress_calcul.tensor_biaxial_shear[0][1])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][1,1]**0.5)+"MPa"+"\n")     
            f.write('sigma 13 = sigma 31 = '+str(stress_calcul.tensor_biaxial_shear[0][2])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][2,2]**0.5)+"MPa"+"\n")
            f.write('sigma 23 = sigma 32 = '+str(stress_calcul.tensor_biaxial_shear[0][3])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][3,3]**0.5)+"MPa"+"\n")
            f.write("---------------------- \n")

        if len(stress_calcul.liste_phi)>=2 and stress_calcul.length_strain>=6:  
            f.write("---Biaxial+shear stress----- \n")
            f.write('sigma 11 = '+str(stress_calcul.tensor_biaxial_shear[0][0])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][0,0]**0.5)+"MPa"+"\n")   
            f.write('sigma 22 = '+str(stress_calcul.tensor_biaxial_shear[0][2])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][2,2]**0.5)+"MPa"+"\n")
            f.write('sigma 12 = sigma 12 = '+str(stress_calcul.tensor_biaxial_shear[0][1])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][1,1]**0.5)+"MPa"+"\n") 
            f.write('sigma 13 = sigma 31 = '+str(stress_calcul.tensor_biaxial_shear[0][3])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][3,3]**0.5)+"MPa"+"\n")
            f.write('sigma 23 = sigma 32 = '+str(stress_calcul.tensor_biaxial_shear[0][4])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][4,4]**0.5)+"MPa"+"\n")
            f.write("---------------------- \n")

        if len(stress_calcul.liste_phi)>=3 and stress_calcul.length_strain>=6:
            f.write("---Triaxial stress----- \n")
            f.write('sigma 11 = '+str(stress_calcul.tensor_triaxial[0][0])+"+/-"+str(stress_calcul.tensor_triaxial[1][0,0]**0.5)+"MPa"+"\n")
            f.write('sigma 22 = '+str(stress_calcul.tensor_triaxial[0][2])+"+/-"+str(stress_calcul.tensor_triaxial[1][2,2]**0.5)+"MPa"+"\n")     
            f.write('sigma 12 = sigma 21 = '+str(stress_calcul.tensor_triaxial[0][1])+"+/-"+str(stress_calcul.tensor_triaxial[1][1,1]**0.5)+"MPa"+"\n")
            f.write('sigma 13 = sigma 31 = '+str(stress_calcul.tensor_triaxial[0][3])+"+/-"+str(stress_calcul.tensor_triaxial[1][3,3]**0.5)+"MPa"+"\n")
            f.write('sigma 23 = sigma 32 = '+str(stress_calcul.tensor_triaxial[0][4])+"+/-"+str(stress_calcul.tensor_triaxial[1][4,4]**0.5)+"MPa"+"\n")
            f.write('sigma 33 = '+str(stress_calcul.tensor_triaxial[0][5])+"+/-"+str(stress_calcul.tensor_triaxial[1][5,5]**0.5)+"MPa"+"\n")
            f.write("---------------------- \n")
                
        f.write("---------------------------------------------------- \n")
        f.write("---------------------------------------------------- \n")                

        f.write("phi(°)    psi(°)    omega(°)     gamma(°)   peak_2theta(°)    phi_gamma(°)     psi_gamma(°)\n")
        for i in range(len(stress_calcul.phi)):
            progress["value"] = progress["value"]+1
            progress.update()
            for j in range(main_calcul.gamma_number):
                gamma_range=int(main_calcul.gamma_f_index+j*main_calcul.gamma_step+main_calcul.gamma_step/2)
                try:
                    f.write(str("%3.4g" % main_calcul.phi[i]))
                    f.write(str("%10.4g" % main_calcul.chi[i]))
                    f.write(str("%12.4g" % main_calcul.omega[i]))
                    f.write(str("%15.4g" % main_calcul.gamma_y[gamma_range]))
                    f.write(str("%15.4g" % main_calcul.peaks_position[i*main_calcul.gamma_number+j]))
                    f.write(str("%15.4g" % stress_calcul.phi_regroup[i*main_calcul.gamma_number+j]))
                    f.write(str("%15.4g" % stress_calcul.psi_regroup[i*main_calcul.gamma_number+j]))
                except TypeError:
                    pass
                f.write("\n")
        f.close()
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()  
    main.root.mainloop()
        
def export_strain_sin2psi_data(i_stress,main_calcul,stress_calcul,main):
    f=asksaveasfile(title="Export strain",mode='w',defaultextension=".EC",filetypes=[('.EC','.EC'),('all files','.*')])
    if f is not None and f is not '':
        f.write("Linear_fit: a="+str(stress_calcul.a[i_stress])+"   b="+str(stress_calcul.b[i_stress])+"\n")
        f.write("Linear_fit_erros: error_a="+str(stress_calcul.er_a[i_stress])+"   error_b="+str(stress_calcul.er_b[i_stress])+"\n")
        f.write("sin2psi      strain\n")
        i=-1
        for j in range(len(main_calcul.phi)):
            for k in range(main_calcul.gamma_number):
                if (j*main_calcul.gamma_number+k) in stress_calcul.index_peak[i_stress]:
                    i=i+1
                    f.write(str(stress_calcul.sinpsi_2[i_stress][i]))
                    f.write("        ")
                    f.write(str(stress_calcul.strain[i_stress][i]))
                    f.write("\n")
        f.close()
    main.root.mainloop()
        
        
        
