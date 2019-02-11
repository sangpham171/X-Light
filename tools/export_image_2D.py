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
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import markers
from matplotlib import lines
from tkinter.messagebox import *
import numpy as np
import math as math

from read_file.image_2D.read_image_2D import read_data_2D

def export_original_image(nfile,nimage,nimage_i,import_XRD,main):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),
                                                                              ('eps files','.eps'),
                                                                              ('pdf files','.pdf'),
                                                                              ('raw files','.raw'),
                                                                              ('ps files','.ps'),
                                                                              ('rgba files','.rgba'),
                                                                              ('svg files','.svg'),
                                                                              ('svgz files','.svgz')])
    if name is not None and name is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = 2
        
        name=str(name); name=list(name);del(name[-29:]);del(name[:25]); name="".join(name)

        f=import_XRD.file_link[nfile];    f_split=f.split("/");    filename=f_split[len(f_split)-1]
        phi=import_XRD.phi[nimage];        chi=import_XRD.chi[nimage];        omega=import_XRD.omega[nimage]
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
            row_tick=import_XRD.row_tick[nimage]
            col_tick=import_XRD.col_tick[nimage]
                
        if rotate==90:
            data=np.rot90(data,k=1,axes=(0, 1))
            nrow=import_XRD.ncol[nimage]
            ncol=import_XRD.nrow[nimage]
            row_tick=import_XRD.col_tick[nimage]
            col_tick=import_XRD.row_tick[nimage]
                
        if rotate==180:
            data=np.rot90(data,k=2,axes=(0, 1))
            nrow=import_XRD.nrow[nimage]
            ncol=import_XRD.ncol[nimage]
            row_tick=import_XRD.row_tick[nimage]
            col_tick=import_XRD.col_tick[nimage]
                    
        if rotate==270:
            data=np.rot90(data,k=3,axes=(0, 1))
            nrow=import_XRD.ncol[nimage]
            ncol=import_XRD.nrow[nimage]
            row_tick=import_XRD.col_tick[nimage]
            col_tick=import_XRD.row_tick[nimage]

        if flip==1:
            data=np.flip(data,axis=0)
        if flip==2:
            data=np.flip(data,axis=1)

        fig=plt.figure(figsize=(10,10),dpi=100)
        try:
            legend_from= float(import_XRD.legend_from_entry.get())
            legend_to= float(import_XRD.legend_to_entry.get())
        except ValueError:
            plt.imshow(data, cmap="hot",origin='lower')
        else:
            plt.imshow(data,clim=(legend_from, legend_to),cmap="hot",origin='lower')

        plt.title(u'\u03C6='+str(float(phi))+"°"+
                  u'; \u03C7='+str(float(chi))+"°"+
                  u"; \u03C9="+str(float(omega))+"°",fontsize=30)
        plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), ('%0.1f' % row_tick[0],
                                                       '%0.1f' % row_tick[int(nrow*0.25)],
                                                       '%0.1f' % row_tick[int(nrow*0.5)],
                                                       '%0.1f' % row_tick[int(nrow*0.75)],
                                                       '%0.1f' % row_tick[nrow-1]))
        plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), ('%0.1f' % col_tick[0],
                                                           '%0.1f' % col_tick[int(ncol*0.25)],
                                                           '%0.1f' % col_tick[int(ncol*0.5)],
                                                           '%0.1f' % col_tick[int(ncol*0.75)],
                                                           '%0.1f' % col_tick[ncol-1]))
        plt.xlabel("pixel",fontsize=30)
        plt.ylabel("pixel",fontsize=30)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        #plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
        plt.savefig(str(name), bbox_inches="tight")
        plt.close(fig)

        for widget in main.Frame1_2.winfo_children():
            widget.destroy()
    main.root.mainloop()
#-----------------------------------------------------------------------
def export_all_original_image(import_XRD,main):
    location=askdirectory(title="Please choose a directory")
    if location is not None and location is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(import_XRD.nfile)
        for i in range(len(import_XRD.nfile)):
            progress["value"] = progress["value"]+1
            progress.update()

            f=import_XRD.file_link[import_XRD.nfile[i]];    f_split=f.split("/");    filename=f_split[len(f_split)-1]
            phi=import_XRD.phi[i];    chi=import_XRD.chi[i];    omega=import_XRD.omega[i]
            rotate=import_XRD.rotate
            flip=import_XRD.flip

            data=read_data_2D(i,import_XRD)

            if len(data.shape)==3:
                data=data[import_XRD.nimage_i[i]]

            if len(data)==0:
                showinfo(title="Warning",message="Can not read data of "+str(filename))
                return
                            
            if rotate==0:
                nrow=import_XRD.nrow[i]
                ncol=import_XRD.ncol[i]
                row_tick=import_XRD.row_tick[i]
                col_tick=import_XRD.col_tick[i]
                
            if rotate==90:
                data=np.rot90(data,k=1,axes=(0, 1))
                nrow=import_XRD.ncol[i]
                ncol=import_XRD.nrow[i]
                row_tick=import_XRD.col_tick[i]
                col_tick=import_XRD.row_tick[i]
                
                
            if rotate==180:
                data=np.rot90(data,k=2,axes=(0, 1))
                nrow=import_XRD.nrow[i]
                ncol=import_XRD.ncol[i]
                row_tick=import_XRD.row_tick[i]
                col_tick=import_XRD.col_tick[i]
                    
            if rotate==270:
                data=np.rot90(data,k=3,axes=(0, 1))
                nrow=import_XRD.ncol[i]
                ncol=import_XRD.nrow[i]
                row_tick=import_XRD.col_tick[i]
                col_tick=import_XRD.row_tick[i]
                
            if flip==1:
                data=np.flip(data,axis=0)
            if flip==2:
                data=np.flip(data,axis=1)
                
            fig=plt.figure(figsize=(10,10),dpi=100)
            try:
                legend_from= float(import_XRD.legend_from_entry.get())
                legend_to= float(import_XRD.legend_to_entry.get())
            except ValueError:
                plt.imshow(data, cmap="hot",origin='lower')
            else:
                plt.imshow(data,clim=(legend_from, legend_to),cmap="hot",origin='lower')

            plt.title(u'\u03C6='+str(float(phi))+"°"+
                      u'; \u03C7='+str(float(chi))+"°"+
                      u"; \u03C9="+str(float(omega))+"°",fontsize=30)
            plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), ('%0.1f' % row_tick[0],
                                                       '%0.1f' % row_tick[int(nrow*0.25)],
                                                       '%0.1f' % row_tick[int(nrow*0.5)],
                                                       '%0.1f' % row_tick[int(nrow*0.75)],
                                                       '%0.1f' % row_tick[nrow-1]))
            plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), ('%0.1f' % col_tick[0],
                                                               '%0.1f' % col_tick[int(ncol*0.25)],
                                                               '%0.1f' % col_tick[int(ncol*0.5)],
                                                               '%0.1f' % col_tick[int(ncol*0.75)],
                                                               '%0.1f' % col_tick[ncol-1]))
            plt.xlabel("pixel",fontsize=30)
            plt.ylabel("pixel",fontsize=30)
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=30)
            #plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
            plt.savefig(str(location)+'/'+filename.split('.')[0]+'_'+str(import_XRD.nimage_i[i])+".png", bbox_inches="tight")
            plt.close(fig)
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()
    main.root.mainloop()
#-----------------------------------------------------------------------
def export_calib_image(calib_2D,angles_modif,import_XRD,main):
    from residual_stress_2D.calib_XRD_2D import calib_pyFai
    
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),
                                                                              ('eps files','.eps'),
                                                                              ('pdf files','.pdf'),
                                                                              ('raw files','.raw'),
                                                                              ('ps files','.ps'),
                                                                              ('rgba files','.rgba'),
                                                                              ('svg files','.svg'),
                                                                              ('svgz files','.svgz')])
    if name is not None and name is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = 3
        
        name=str(name);        name=list(name);        del(name[-29:]);        del(name[:25]);        name="".join(name)

        progress["value"] = progress["value"]+1
        progress.update()

        f=import_XRD.file_link[import_XRD.nfile[calib_2D.nimage]];            f_split=f.split("/");            filename=f_split[len(f_split)-1]
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

            fig=plt.figure(figsize=(10,10),dpi=100)
            try:
                legend_from= float(calib_2D.Entry_legend_from_3_2.get())
                legend_to= float(calib_2D.Entry_legend_to_3_2.get())
            except ValueError:
                plt.imshow(data, cmap="hot",origin='lower')
            else:
                plt.imshow(data,clim=(legend_from, legend_to),cmap="hot",origin='lower')

            plt.title(u"\u03C6="+str(float(phi))+"°"+
                      u"; \u03C7="+str(float(chi))+"°"+
                      u"; \u03C9="+str(float(omega))+"°",fontsize=30)
            plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %gamma_y[0]),
                                                               str("%0.1f" %gamma_y[int(nrow*0.25)]),
                                                               str("%0.1f" %gamma_y[int(nrow*0.5)]),
                                                               str("%0.1f" %gamma_y[int(nrow*0.75)]),
                                                               str("%0.1f" %gamma_y[int(nrow-1)])))
            plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %twotheta_x[0]),
                                                               str("%0.1f" %twotheta_x[int(ncol*0.25)]),
                                                               str("%0.1f" %twotheta_x[int(ncol*0.5)]),
                                                               str("%0.1f" %twotheta_x[int(ncol*0.75)]),
                                                               str("%0.1f" %twotheta_x[int(ncol-1)])))
            plt.xlabel(r"$2\theta(°)$",fontsize=30)
            plt.ylabel(r"$\gamma(°)$",fontsize=30)
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=30)
            #plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
            plt.savefig(str(name), bbox_inches="tight")
            plt.close(fig)

            for widget in main.Frame1_2.winfo_children():
                widget.destroy() 
    main.root.mainloop()
#-----------------------------------------------------------------------
def export_all_calib_image(calib_2D,angles_modif,import_XRD,main):
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
        for i in range(len(import_XRD.nfile)):
            progress["value"] = progress["value"]+1
            progress.update()

            f=import_XRD.file_link[import_XRD.nfile[i]];            f_split=f.split("/");            filename=f_split[len(f_split)-1]
            rotate=import_XRD.rotate
            flip=import_XRD.flip

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
                nrow=len(gamma_y)
                ncol=len(twotheta_x)

                fig=plt.figure(figsize=(10,10),dpi=100)
                try:
                    legend_from= float(calib_2D.Entry_legend_from_3_2.get())
                    legend_to= float(calib_2D.Entry_legend_to_3_2.get())
                except ValueError:
                    plt.imshow(data, cmap="hot",origin='lower')
                else:
                    plt.imshow(data,clim=(legend_from, legend_to),cmap="hot",origin='lower')

                plt.title(u"\u03C6="+str(float(phi))+"°"+
                          u"; \u03C7="+str(float(chi))+"°"+
                          u"; \u03C9="+str(float(omega))+"°",fontsize=30)
                plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %gamma_y[0]),
                                                                   str("%0.1f" %gamma_y[int(nrow*0.25)]),
                                                                   str("%0.1f" %gamma_y[int(nrow*0.5)]),
                                                                   str("%0.1f" %gamma_y[int(nrow*0.75)]),
                                                                   str("%0.1f" %gamma_y[int(nrow-1)])))
                plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %twotheta_x[0]),
                                                                   str("%0.1f" %twotheta_x[int(ncol*0.25)]),
                                                                   str("%0.1f" %twotheta_x[int(ncol*0.5)]),
                                                                   str("%0.1f" %twotheta_x[int(ncol*0.75)]),
                                                                   str("%0.1f" %twotheta_x[int(ncol-1)])))
                plt.xlabel(r"$2\theta(°)$",fontsize=30)
                plt.ylabel(r"$\gamma(°)$",fontsize=30)
                plt.xticks(fontsize=30)
                plt.yticks(fontsize=30)
                #plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
                plt.savefig(str(location)+'/calib_'+filename.split('.')[0]+'_'+str(import_XRD.nimage_i[i])+".png", bbox_inches="tight")
                plt.close(fig)
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()   
    main.root.mainloop()
#-----------------------------------------------------------------------
def export_fit_graph(i_graph,main_calcul,calib_2D,stress_calcul,main):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),
                                                                              ('eps files','.eps'),
                                                                              ('pdf files','.pdf'),
                                                                              ('raw files','.raw'),
                                                                              ('ps files','.ps'),
                                                                              ('rgba files','.rgba'),
                                                                              ('svg files','.svg'),
                                                                              ('svgz files','.svgz')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)
        
        i=calib_2D.nimage*main_calcul.gamma_number+i_graph
        j_start=int(main_calcul.gamma_f_index+i_graph*main_calcul.gamma_step)
        j_end=int(main_calcul.gamma_f_index+(i_graph+1)*main_calcul.gamma_step)
        
        f=plt.figure(figsize=(10,10),dpi=100)

        try:
            fsize=(main_calcul.Entry_fig[0].get()).split(',')
            float(fsize[0])
            float(fsize[1])
        except ValueError:
            showinfo(title="Warning",message="Figsize format: number,number") 
            pass
        else:
            f.set_size_inches(float(fsize[0]),float(fsize[1]))

        try:
            float(main_calcul.Entry_fig[6].get())
        except ValueError:
            showinfo(title="Warning",message="dpi must be a number") 
            pass
        else:
            f.set_dpi(float(main_calcul.Entry_fig[6].get()))
        
        if float(main_calcul.original.get())==1:
            x=[main_calcul.peaks_position[i],main_calcul.peaks_position[i]]
            y=[min(main_calcul.data_y_net[i]),max(main_calcul.data_y_limit[i])]
            curve=plt.plot(main_calcul.data_x_limit,main_calcul.data_y_limit[i],'ro',markersize=2,label='Original intensity')

            line=curve[0]
            if main_calcul.Entry_fig[2].get() in dict(markers.MarkerStyle.markers):
                line.set_marker(main_calcul.Entry_fig[2].get())
                try:
                    ms=float(main_calcul.Entry_fig[3].get())
                except ValueError:
                    showinfo(title="Warning",message="Markersize muse be a number")
                else:
                    line.set_markersize(ms)
            else:
                showinfo(title="Warning",message=str(main_calcul.Entry_fig[2].get())+" is not a marker keyword"+
                         "\n Matplotlib https://matplotlib.org/api/markers_api.html")
                pass

            if main_calcul.Entry_fig[5].get() in dict(lines.Line2D.lineStyles):
                line.set_linestyle(main_calcul.Entry_fig[5].get())
            else:
                showinfo(title="Warning",message=str(main_calcul.Entry_fig[5].get())+" is not a line style keyword"+
                         "\n Matplotlib https://matplotlib.org/gallery/lines_bars_and_markers/line_styles_reference.html")
                    
        else:
            x=[main_calcul.peaks_position[i],main_calcul.peaks_position[i]]
            y=[min(main_calcul.data_y_net[i]),max(main_calcul.data_y_net[i])]
        if float(main_calcul.background.get())==1:    
            plt.plot(main_calcul.data_x_limit,main_calcul.data_y_background_fit[i],'k',label='Background')
        if float(main_calcul.net_intensity.get())==1:
            curve=plt.plot(main_calcul.data_x_limit,main_calcul.data_y_net[i],'go',markersize=2,label='Net intensity')

            line=curve[0]
            if main_calcul.Entry_fig[4].get() in dict(colors.BASE_COLORS, **colors.CSS4_COLORS):
                line.set_color(main_calcul.Entry_fig[4].get())
            if main_calcul.Entry_fig[2].get() in dict(markers.MarkerStyle.markers):
                line.set_marker(main_calcul.Entry_fig[2].get())
                try:
                    ms=float(main_calcul.Entry_fig[3].get())
                except ValueError:
                    showinfo(title="Warning",message="Markersize muse be a number")
                else:
                    line.set_markersize(ms)
            else:
                showinfo(title="Warning",message=str(main_calcul.Entry_fig[2].get())+" is not a marker keyword"+
                         "\n Matplotlib https://matplotlib.org/api/markers_api.html")
                pass

            if main_calcul.Entry_fig[5].get() in dict(lines.Line2D.lineStyles):
                line.set_linestyle(main_calcul.Entry_fig[5].get())
            else:
                showinfo(title="Warning",message=str(main_calcul.Entry_fig[5].get())+" is not a line style keyword"+
                         "\n Matplotlib https://matplotlib.org/gallery/lines_bars_and_markers/line_styles_reference.html")
                    
        if float(main_calcul.I_alpha1.get())==1:
            plt.plot(main_calcul.data_x_limit,main_calcul.data_y_k1_fit[i],'b',label=r"I($\lambda_{1}$)")
        if float(main_calcul.I_alpha2.get())==1:
            plt.plot(main_calcul.data_x_limit,main_calcul.data_y_k2_fit[i],'c',label=r"I($\lambda_{2}$)")
        if float(main_calcul.I_total.get())==1:
            plt.plot(main_calcul.data_x_limit,main_calcul.data_y_fit_total[i],'m',label=r"I($\lambda_{1}$)"+r" + I($\lambda_{2}$)"+' (r='+str("%0.3f" %main_calcul.r[i])+")")
        plt.plot(x,y,'b--',label=r"peak 2$\theta_{1}$ = "+str('%0.2f' % main_calcul.peaks_position[i])+"°"+"\n"+
                         r"I$_{0}$="+str('%0.1f' % main_calcul.peak_intensity[i])+
                         "; FWHM="+str('%0.1f' % main_calcul.FWHM[i])+"°"+
                         "; a="+str('%0.1f' % main_calcul.a[i]))

        if str(i) in stress_calcul.list_graph_error:
            title=plt.title("This result is not used in stress calcul\n"+
                            u"\u03C6= "+str(main_calcul.phi[calib_2D.nimage])+"°"+
                            u", \u03C7= "+str(main_calcul.chi[calib_2D.nimage])+"°"+
                            u", \u03C9= "+str(main_calcul.omega[calib_2D.nimage])+"°""\n"+
                            r"$\gamma(°)$"+" integrate from "+str("%0.1f" %(main_calcul.gamma_y[j_start]))+
                            "° to "+str("%0.1f" %(main_calcul.gamma_y[j_end]))+"°")
        else:
            title=plt.title(u"\u03C6= "+str(main_calcul.phi[calib_2D.nimage])+"°"+
                            u", \u03C7= "+str(main_calcul.chi[calib_2D.nimage])+"°"+
                            u", \u03C9= "+str(main_calcul.omega[calib_2D.nimage])+"°"+"\n"+
                            r"$\gamma(°)$"+" integrate from "+str("%0.1f" %(main_calcul.gamma_y[j_start]))+
                            "° to "+str("%0.1f" %(main_calcul.gamma_y[j_end]))+"°")

        xlabel=plt.xlabel(r"$2\theta(°)$")
        ylabel=plt.ylabel("Intensity")
        
        plt.legend(loc='upper left', bbox_to_anchor=(-0.2,-0.2,1.2,0),ncol=2,mode="expand",borderaxespad=0.)

        try:
            fs=float(main_calcul.Entry_fig[1].get())
        except ValueError:
            pass
        else:   
            xlabel.set_fontsize(fs)
            ylabel.set_fontsize(fs)
            plt.xticks(fontsize=fs)
            plt.yticks(fontsize=fs)
            title.set_fontsize(fs)
            plt.legend(loc='upper left', bbox_to_anchor=(-0.2, -0.2, 1.2, 0),ncol=2,mode="expand",borderaxespad=0.,fontsize=fs)
                
        plt.subplots_adjust(bottom=0.3)
        plt.savefig(str(name), bbox_inches="tight")
        plt.close()
    main.root.mainloop()
#-----------------------------------------------------------------------
def export_all_fit_graph(main_calcul,calib_2D,stress_calcul,main):
    location=askdirectory(title="Please choose a directory")
    if location is not None and location is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(calib_2D.phi)*main_calcul.gamma_number

        for nimage in range(len(main_calcul.phi)):
            for i_graph in range(main_calcul.gamma_number):
                progress["value"] = progress["value"]+1
                progress.update()

                f=plt.figure(figsize=(10,10),dpi=100)
                try:
                    fsize=(main_calcul.Entry_fig[0].get()).split(',')
                    float(fsize[0])
                    float(fsize[1])
                except ValueError:
                    pass
                else:
                    f.set_size_inches(float(fsize[0]),float(fsize[1]))

                try:
                    float(main_calcul.Entry_fig[6].get())
                except ValueError:
                    pass
                else:
                    f.set_dpi(float(main_calcul.Entry_fig[6].get()))
                
                i=nimage*main_calcul.gamma_number+i_graph
                j_start=int(main_calcul.gamma_f_index+i_graph*main_calcul.gamma_step)
                j_end=int(main_calcul.gamma_f_index+(i_graph+1)*main_calcul.gamma_step)
                   
                try:
                    if float(main_calcul.original.get())==1:
                        x=[main_calcul.peaks_position[i],main_calcul.peaks_position[i]]
                        y=[min(main_calcul.data_y_net[i]),max(main_calcul.data_y_limit[i])] 
                        curve=plt.plot(main_calcul.data_x_limit,main_calcul.data_y_limit[i],'ro',markersize=2,label='Original intensity')

                        line=curve[0]
                        if main_calcul.Entry_fig[2].get() in dict(markers.MarkerStyle.markers):
                            line.set_marker(main_calcul.Entry_fig[2].get())
                            try:
                                ms=float(main_calcul.Entry_fig[3].get())
                            except ValueError:
                                pass
                            else:
                                line.set_markersize(ms)

                        if main_calcul.Entry_fig[5].get() in dict(lines.Line2D.lineStyles):
                            line.set_linestyle(main_calcul.Entry_fig[5].get())
                        
                    else:
                        x=[main_calcul.peaks_position[i],main_calcul.peaks_position[i]]
                        y=[min(main_calcul.data_y_net[i]),max(main_calcul.data_y_net[i])] 
                except (IndexError,ValueError): 
                    pass
                else:
                    try:
                        if float(main_calcul.background.get())==1:
                            plt.plot(main_calcul.data_x_limit,main_calcul.data_y_background_fit[i],'k',label='Background')
                        if float(main_calcul.net_intensity.get())==1:
                            curve=plt.plot(main_calcul.data_x_limit,main_calcul.data_y_net[i],'go',markersize=2,label='Net intensity')

                            line=curve[0]
                            if main_calcul.Entry_fig[4].get() in dict(colors.BASE_COLORS, **colors.CSS4_COLORS):
                                line.set_color(main_calcul.Entry_fig[4].get())

                            if main_calcul.Entry_fig[2].get() in dict(markers.MarkerStyle.markers):
                                line.set_marker(main_calcul.Entry_fig[2].get())
                                try:
                                    ms=float(main_calcul.Entry_fig[3].get())
                                except ValueError:
                                    pass
                                else:
                                    line.set_markersize(ms)

                            if main_calcul.Entry_fig[5].get() in dict(lines.Line2D.lineStyles):
                                line.set_linestyle(main_calcul.Entry_fig[5].get())
                        
                    except (IndexError,ValueError): 
                        pass
                    else:
                        try:
                            if float(main_calcul.I_alpha1.get())==1:
                                plt.plot(main_calcul.data_x_limit,main_calcul.data_y_k1_fit[i],'b',label=r"I($\lambda_{1}$)")
                            if float(main_calcul.I_alpha2.get())==1:
                                plt.plot(main_calcul.data_x_limit,main_calcul.data_y_k2_fit[i],'c',label=r"I($\lambda_{2}$)")
                            if float(main_calcul.I_total.get())==1:
                                plt.plot(main_calcul.data_x_limit,main_calcul.data_y_fit_total[i],'m',label=r"I($\lambda_{1}$)"+r" + I($\lambda_{2}$)"+' (r='+str("%0.3f" %main_calcul.r[i])+")")
                            plt.plot(x,y,'b--',label=r"peak 2$\theta_{1}$ = "+str('%0.2f' % main_calcul.peaks_position[i])+"°"+"\n"+
                                     r"I$_{0}$="+str('%0.1f' % main_calcul.peak_intensity[i])+
                                        "; FWHM="+str('%0.1f' % main_calcul.FWHM[i])+"°"+
                                         "; a="+str('%0.1f' % main_calcul.a[i]))
                        except (IndexError,ValueError): 
                            pass
                        else:
                            if str(i) in stress_calcul.list_graph_error:
                                title=plt.title("This result is not used in stress calcul\n"+
                                                u"\u03C6= "+str(main_calcul.phi[nimage])+"°"+
                                                u", \u03C7= "+str(main_calcul.chi[nimage])+"°"+
                                                u", \u03C9= "+str(main_calcul.omega[nimage])+"°""\n"+
                                                r"$\gamma(°)$"+" integrate from "+str("%0.1f" %(main_calcul.gamma_y[j_start]))+
                                                "° to "+str("%0.1f" %(main_calcul.gamma_y[j_end]))+"°")
                            else:
                                title=plt.title(u"\u03C6= "+str(main_calcul.phi[nimage])+"°"+
                                                u", \u03C7= "+str(main_calcul.chi[nimage])+"°"+
                                                u", \u03C9= "+str(main_calcul.omega[nimage])+"°"+"\n"+
                                                r"$\gamma(°)$"+" integrate from "+str("%0.1f" %(main_calcul.gamma_y[j_start]))+
                                                "° to "+str("%0.1f" %(main_calcul.gamma_y[j_end]))+"°")
                            
                            xlabel=plt.xlabel(r"$2\theta(°)$")
                            ylabel=plt.ylabel("Intensity")
                            plt.legend(loc='upper left', bbox_to_anchor=(0,-0.2,1,0),ncol=2,mode="expand",borderaxespad=0.)
                            try:
                                fs=float(main_calcul.Entry_fig[1].get())
                            except ValueError:
                                pass
                            else:   
                                xlabel.set_fontsize(fs)
                                ylabel.set_fontsize(fs)
                                plt.xticks(fontsize=fs)
                                plt.yticks(fontsize=fs)
                                title.set_fontsize(fs)
                                plt.legend(loc='upper left', bbox_to_anchor=(-0.2, -0.2, 1.2, 0),ncol=2,mode="expand",borderaxespad=0.,fontsize=fs)
                            
                            plt.subplots_adjust(bottom=0.3)
                            plt.savefig(str(location)+"/"+str(nimage)+"_"+str(i_graph)+"_Fitting_phi="+str(float(main_calcul.phi[nimage]))+"; chi="+str(float(main_calcul.chi[nimage]))+".png", bbox_inches="tight")
                plt.close()
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()   
    main.root.mainloop()
#--------------------------------------------------------------------
def export_stress_graph(i_stress,main_calcul,stress_calcul,main):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),
                                                                              ('eps files','.eps'),
                                                                              ('pdf files','.pdf'),
                                                                              ('raw files','.raw'),
                                                                              ('ps files','.ps'),
                                                                              ('rgba files','.rgba'),
                                                                              ('svg files','.svg'),
                                                                              ('svgz files','.svgz')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)
        
        f=plt.figure(figsize=(10,10),dpi=100)
        try:
            fsize=(stress_calcul.Entry_fig[0].get()).split(',')
            float(fsize[0])
            float(fsize[1])
        except ValueError:
            showinfo(title="Warning",message="Figsize format: number,number") 
            pass
        else:
            f.set_size_inches(float(fsize[0]),float(fsize[1]))

        try:
            float(stress_calcul.Entry_fig[6].get())
        except ValueError:
            showinfo(title="Warning",message="dpi must be a number") 
            pass
        else:
            f.set_dpi(float(stress_calcul.Entry_fig[6].get()))

        try:
            float(stress_calcul.Entry_fig[1].get())
        except ValueError:
            fs=None
        else:
            fs=float(stress_calcul.Entry_fig[1].get())
        
        i=-1
        if float(main_calcul.experimental.get())==1:
            for j in range(len(main_calcul.phi)):
                sinpsi_2=[]
                strain=[]
                error_strain=[]
                for k in range(main_calcul.gamma_number):
                    if (j*main_calcul.gamma_number+k) in stress_calcul.index_peak[i_stress]:
                        i=i+1
                        if float(main_calcul.annotate.get())==1:
                            if fs is not None:
                                plt.annotate(str(k+1),xy=(stress_calcul.sinpsi_2[i_stress][i],stress_calcul.strain[i_stress][i]),fontsize=fs)
                            else:
                                plt.annotate(str(k+1),xy=(stress_calcul.sinpsi_2[i_stress][i],stress_calcul.strain[i_stress][i]))
                        sinpsi_2.append(stress_calcul.sinpsi_2[i_stress][i])
                        strain.append(stress_calcul.strain[i_stress][i])
                        error_strain.append(stress_calcul.error_strain[i_stress][i])
                if len(strain)>0:
                    curve=plt.errorbar(sinpsi_2,strain,yerr=error_strain,fmt='o',capsize=4,elinewidth=1,label=str(j+1)+u".\u03C6= "+str(main_calcul.phi[j])+u", \u03C7= "+str(main_calcul.chi[j]))

                    line=curve[0]
                    if stress_calcul.Entry_fig[2].get() in dict(markers.MarkerStyle.markers):
                        line.set_marker(stress_calcul.Entry_fig[2].get())
                        try:
                            ms=float(stress_calcul.Entry_fig[3].get())
                        except ValueError:
                            showinfo(title="Warning",message="Markersize muse be a number")
                        else:
                            line.set_markersize(ms)
                    else:
                        showinfo(title="Warning",message=str(stress_calcul.Entry_fig[2].get())+" is not a marker keyword"+
                                 "\n Matplotlib https://matplotlib.org/api/markers_api.html")
                        pass

                    if stress_calcul.Entry_fig[5].get() in dict(lines.Line2D.lineStyles):
                        line.set_linestyle(stress_calcul.Entry_fig[5].get())
                    else:
                        showinfo(title="Warning",message=str(stress_calcul.Entry_fig[5].get())+" is not a line style keyword"+
                                 "\n Matplotlib https://matplotlib.org/gallery/lines_bars_and_markers/line_styles_reference.html")
                        
        if stress_calcul.stress_valid>=1:
            if float(main_calcul.stress_behaviour.get())==1 and float(main_calcul.sin2khi_method.get())==1:
                plt.plot(stress_calcul.sinpsi_2_sorted[i_stress],stress_calcul.strain_linear_fit[i_stress],'b',linestyle="-",label=u'Sin\u00B2\u03A8 method')
            if float(main_calcul.stress_behaviour.get())==2 and float(main_calcul.sin2khi_method.get())==1:
                plt.plot(stress_calcul.sinpsi_2_sorted[i_stress],stress_calcul.strain_elliptical_fit[i_stress],'b',linestyle="-",label=u'Sin\u00B2\u03A8 method')

        if len(stress_calcul.liste_phi)>=1:
            if float(main_calcul.stress_dimension.get())==2:
                if stress_calcul.length_strain>=3 and float(main_calcul.stress_behaviour.get())==1 and float(main_calcul.fundamental_method.get())==1:
                    plt.plot(stress_calcul.sinpsi_2_sorted[i_stress],stress_calcul.strain_biaxial[i_stress],'m',linestyle="--",label='Fundamental method')
                if stress_calcul.length_strain>=5 and float(main_calcul.stress_behaviour.get())==2 and float(main_calcul.fundamental_method.get())==1:
                    plt.plot(stress_calcul.sinpsi_2_sorted[i_stress],stress_calcul.strain_biaxial_shear[i_stress],'m',linestyle="--",label='Fundamental method')
            if float(main_calcul.stress_dimension.get())==3:
                if stress_calcul.length_strain>=6 and float(main_calcul.fundamental_method.get())==1:
                    plt.plot(stress_calcul.sinpsi_2_sorted[i_stress],stress_calcul.strain_triaxial[i_stress],'m',linestyle="--",label='Fundamental method')
            
        xlabel=plt.xlabel(r"$sin^{2}\psi$")
        ylabel=plt.ylabel('Lattice strain '+r"$\varepsilon$")
        title=plt.title(u"\u03D5 = "+str(stress_calcul.liste_phi[i_stress])+"°")
        plt.legend(loc='upper center', bbox_to_anchor=(-0.2,-0.3,1.2,0),ncol=2,mode="expand",borderaxespad=0.)
        if fs is not None:   
            xlabel.set_fontsize(fs)
            ylabel.set_fontsize(fs)
            plt.xticks(fontsize=fs)
            plt.yticks(fontsize=fs)
            title.set_fontsize(fs)
            plt.legend(loc='upper left', bbox_to_anchor=(-0.2, -0.3, 1.2, 0),ncol=2,mode="expand",borderaxespad=0.,fontsize=fs)
            
        plt.subplots_adjust(bottom=0.4)
        plt.subplots_adjust(left=0.2)
        plt.savefig(str(name), bbox_inches="tight")
        plt.close()
    main.root.mainloop()
    
#-------------------------------------------
def export_all_stress_graph(main_calcul,stress_calcul,main):
    location=askdirectory(title="Please choose a directory")
    if location is not None and location is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(stress_calcul.liste_phi)
        
        for c in range(len(stress_calcul.liste_phi)):
            progress["value"] = progress["value"]+1
            progress.update()

            f=plt.figure(figsize=(10,10),dpi=100)
            try:
                fsize=(stress_calcul.Entry_fig[0].get()).split(',')
                float(fsize[0])
                float(fsize[1])
            except ValueError:
                pass
            else:
                f.set_size_inches(float(fsize[0]),float(fsize[1]))

            try:
                float(stress_calcul.Entry_fig[6].get())
            except ValueError:
                pass
            else:
                f.set_dpi(float(stress_calcul.Entry_fig[6].get()))

            try:
                float(stress_calcul.Entry_fig[1].get())
            except ValueError:
                fs=None
            else:
                fs=float(stress_calcul.Entry_fig[1].get())
                
            i=-1
            if float(main_calcul.experimental.get())==1:
                for j in range(len(main_calcul.phi)):
                    sinpsi_2=[]
                    strain=[]
                    error_strain=[]
                    for k in range(main_calcul.gamma_number):
                        if (j*main_calcul.gamma_number+k) in stress_calcul.index_peak[c]:
                            i=i+1
                            if float(main_calcul.annotate.get())==1:
                                if fs is not None:
                                    plt.annotate(str(k+1),xy=(stress_calcul.sinpsi_2[c][i],stress_calcul.strain[c][i]),fontsize=fs)
                                else:
                                    plt.annotate(str(k+1),xy=(stress_calcul.sinpsi_2[c][i],stress_calcul.strain[c][i]))  
                            sinpsi_2.append(stress_calcul.sinpsi_2[c][i])
                            strain.append(stress_calcul.strain[c][i])
                            error_strain.append(stress_calcul.error_strain[c][i])
                    if len(strain)>0:
                        curve=plt.errorbar(sinpsi_2,strain,yerr=error_strain,fmt='o',capsize=4, elinewidth=1,label=str(j+1)+u".\u03C6= "+str(main_calcul.phi[j])+u", \u03C7= "+str(main_calcul.chi[j]))
                        line=curve[0]                        
                        if stress_calcul.Entry_fig[2].get() in dict(markers.MarkerStyle.markers):
                            line.set_marker(stress_calcul.Entry_fig[2].get())
                            try:
                                ms=float(stress_calcul.Entry_fig[3].get())
                            except ValueError:
                                pass
                            else:
                                line.set_markersize(ms)

                        if stress_calcul.Entry_fig[5].get() in dict(lines.Line2D.lineStyles):
                            line.set_linestyle(stress_calcul.Entry_fig[5].get())

            try:
                if stress_calcul.stress_valid>=1:
                    if float(main_calcul.stress_behaviour.get())==1 and float(main_calcul.sin2khi_method.get())==1:
                        plt.plot(stress_calcul.sinpsi_2_sorted[c],stress_calcul.strain_linear_fit[c],'b',linestyle="-",label=u'Sin\u00B2\u03A8 method')
                    if float(main_calcul.stress_behaviour.get())==2 and float(main_calcul.sin2khi_method.get())==1:
                        plt.plot(stress_calcul.sinpsi_2_sorted[c],stress_calcul.strain_elliptical_fit[c],'b',linestyle="-",label=u'Sin\u00B2\u03A8 method')

                if len(stress_calcul.liste_phi)>=1:
                    if float(main_calcul.stress_dimension.get())==2:
                        if stress_calcul.length_strain>=3 and float(main_calcul.stress_behaviour.get())==1 and float(main_calcul.fundamental_method.get())==1:
                            plt.plot(stress_calcul.sinpsi_2_sorted[c],stress_calcul.strain_biaxial[c],'m',linestyle="--",label='Fundamental method')
                        if stress_calcul.length_strain>=5 and float(main_calcul.stress_behaviour.get())==2 and float(main_calcul.fundamental_method.get())==1:
                            plt.plot(stress_calcul.sinpsi_2_sorted[c],stress_calcul.strain_biaxial_shear[c],'m',linestyle="--",label='Fundamental method')

                    if float(main_calcul.stress_dimension.get())==3:
                        if stress_calcul.length_strain>=6 and float(main_calcul.fundamental_method.get())==1:
                            plt.plot(stress_calcul.sinpsi_2_sorted[c],stress_calcul.strain_triaxial[c],'m',linestyle="--",label='Fundamental method')
            except ValueError:
                continue
                
            xlabel=plt.xlabel(r"$sin^{2}\psi$")
            ylabel=plt.ylabel('Lattice strain '+r"$\varepsilon$")
            title=plt.title(u"\u03D5 = "+str(stress_calcul.liste_phi[c])+"°")
            plt.legend(loc='best', bbox_to_anchor=(-0.2,-0.3,1.2,0),ncol=2,mode="expand",borderaxespad=0.)

            if fs is not None:  
                xlabel.set_fontsize(fs)
                ylabel.set_fontsize(fs)
                plt.xticks(fontsize=fs)
                plt.yticks(fontsize=fs)
                plt.legend(loc='upper left', bbox_to_anchor=(-0.2, -0.3, 1.2, 0),ncol=2,mode="expand",borderaxespad=0.,fontsize=fs)
            
            plt.subplots_adjust(bottom=0.4)
            plt.subplots_adjust(left=0.2)
            plt.savefig(str(location)+"/stress_phi="+str(float(stress_calcul.liste_phi[c]))+".png", bbox_inches="tight")
            plt.close()
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()   
    main.root.mainloop()
