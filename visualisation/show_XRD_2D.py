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
from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import Progressbar
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import markers
from matplotlib import lines
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math as math
import numpy as np

from tools.export_image_2D import export_original_image, export_all_original_image, export_calib_image, export_all_calib_image, export_fit_graph, export_all_fit_graph, export_stress_graph, export_all_stress_graph
from tools.export_data_2D import export_original_data,export_all_original_data
from tools.export_data_2D import export_calib_data,export_all_calib_data
from tools.export_data_2D import export_fit_data, export_all_fit_data, export_all_stress_data, export_strain_sin2psi_data
from read_file.image_2D.read_image_2D import read_data_2D
from tools.peak_shift_correction import fit_peak_shift_correction

def show_original_image(event,import_XRD,main):
    for widget in main.Frame3_1_2.winfo_children():
        widget.destroy()
    for widget in main.Frame3_1_4.winfo_children():
        widget.destroy()
    for widget in main.Frame1_2.winfo_children():
        widget.destroy()
        
    Label(main.Frame1_2,text="Show").pack(side=LEFT)
    progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
    progress.pack(side=LEFT)
    progress["value"] = 0
    progress["maximum"] = 2
        
    widget = event.widget ;    s=widget.curselection();    s = widget.get(s);    s=s.split(".")
    nimage=int(s[0])-1
    nimage_i=int(s[len(s)-2])-1
    nfile=int(s[len(s)-3])-1

    f=import_XRD.file_link[nfile];    f_split=f.split("/");    filename=f_split[len(f_split)-1]
    phi=import_XRD.phi[nimage];    chi=import_XRD.chi[nimage];    omega=import_XRD.omega[nimage]
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
    
    fig=plt.figure(1,facecolor="0.94")
    cmap_var=import_XRD.cmap_var.get()
    try:
        legend_from= float(import_XRD.legend_from_entry.get())
        legend_to= float(import_XRD.legend_to_entry.get())
    except ValueError:
        plt.imshow(data, cmap=cmap_var,origin='lower')
    else:
        plt.imshow(data,clim=(legend_from, legend_to),cmap=cmap_var,origin='lower')
    plt.title(str(filename)+"\n"+
              u'\u03C6='+str(float(phi))+"°"+
              u'; \u03C7='+str(float(chi))+"°"+
              u"; \u03C9="+str(float(omega))+"°")
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
    plt.xlabel("pixel")
    plt.ylabel("pixel")
    plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
    plt.close()    
    
    canvas = FigureCanvasTkAgg(fig, main.Frame3_1_2)
    canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=YES)

    Frame3_1_4_1=Frame(main.Frame3_1_4)
    Frame3_1_4_1.pack(side=TOP,fill=BOTH, expand=YES)
    Frame3_1_4_2=Frame(main.Frame3_1_4)
    Frame3_1_4_2.pack(side=BOTTOM,fill=BOTH, expand=YES)

    Button(Frame3_1_4_1,compound=CENTER, text="Export all as image",bg="white",command=lambda:export_all_original_image(import_XRD,main)).grid(row=0,column=0,sticky=W)
    Button(Frame3_1_4_1,compound=CENTER, text="Export as image",bg="white",command=lambda:export_original_image(nfile,nimage,nimage_i,import_XRD,main)).grid(row=1,column=0,sticky=W)
    Button(Frame3_1_4_1,compound=CENTER, text="Export as text",bg="white",command=lambda:export_original_data(nfile,nimage,nimage_i,import_XRD,main)).grid(row=2,column=0,sticky=W)
    Button(Frame3_1_4_1,compound=CENTER, text="Export all as text",bg="white",command=lambda:export_all_original_data(import_XRD,main)).grid(row=3,column=0,sticky=W)

    scrollbar = Scrollbar(Frame3_1_4_2)
    scrollbar.pack(side = RIGHT, fill=BOTH) 
    mylist = Listbox(Frame3_1_4_2, yscrollcommand = scrollbar.set)

    for i in range(len(import_XRD.file_info[nimage])):
        mylist.insert(END,str(import_XRD.file_info[nimage][i]))

    mylist.pack(side = LEFT, fill=BOTH,expand=YES)
    scrollbar.config( command = mylist.yview )

    for widget in main.Frame1_2.winfo_children():
        widget.destroy() 
        
    main.root.mainloop()    
#----------------------------
def show_calib_image(event,angles_modif,calib_2D,import_XRD,main_calcul,stress_calcul,Frame_a,main):
    from residual_stress_2D.calib_XRD_2D import calib_pyFai
    
    for widget in main.Frame1_2.winfo_children():
        widget.destroy()
        
    Label(main.Frame1_2,text="Show").pack(side=LEFT)
    progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
    progress.pack(side=LEFT)
    progress["value"] = 0
    progress["maximum"] = 3
        
    widget = event.widget;    s=widget.curselection();    s = widget.get(s);    s=s.split(".")
    calib_2D.nimage=int(s[0])-1
    nimage_i=int(s[len(s)-2])-1
    nfile=int(s[len(s)-3])-1

    progress["value"] = progress["value"]+1
    progress.update()

    f=import_XRD.file_link[nfile];            f_split=f.split("/");            filename=f_split[len(f_split)-1]
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
        data=data[nimage_i]

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
        
        fig=plt.figure(1,facecolor="0.94")
        cmap_var=calib_2D.cmap_var_3_2.get()
        try:
            legend_from= float(calib_2D.Entry_legend_from_3_2.get())
            legend_to= float(calib_2D.Entry_legend_to_3_2.get())
        except ValueError:
            plt.imshow(data, cmap=cmap_var,origin='lower')
        else:
            plt.imshow(data,clim=(legend_from, legend_to),cmap=cmap_var,origin='lower')
        plt.title("Calibration of "+str(filename)+"\n"+
                  u'\u03C6='+str(float(phi))+"°"+
                  u'; \u03C7='+str(float(chi))+"°"+
                  u"; \u03C9="+str(float(omega))+"°")
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
        plt.xlabel(r"$2\theta(°)$")
        plt.ylabel(r"$\gamma(°)$")
        plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
        plt.close()
 
        for widget in Frame_a.winfo_children():
            widget.destroy()
        Button(Frame_a,compound=CENTER, text="Export all as data",bg="white",command=lambda:export_all_calib_data(calib_2D,angles_modif,import_XRD,main)).pack(side=BOTTOM)
        Button(Frame_a,compound=CENTER, text="Export as data",bg="white",command=lambda:export_calib_data(calib_2D,angles_modif,import_XRD,main)).pack(side=BOTTOM)
        Button(Frame_a,compound=CENTER, text="Export all as image",bg="white",command=lambda:export_all_calib_image(calib_2D,angles_modif,import_XRD,main)).pack(side=BOTTOM) 
        Button(Frame_a,compound=CENTER, text="Export as image",bg="white",command=lambda:export_calib_image(calib_2D,angles_modif,import_XRD,main)).pack(side=BOTTOM)
        
        canvas = FigureCanvasTkAgg(fig, Frame_a)
        canvas.get_tk_widget().pack(side=TOP,expand=YES,fill=BOTH)
        try:
            main_calcul.gamma_number
        except AttributeError:
            pass
        else:
            for widget in main.Frame3_5_3_1.winfo_children():
                widget.destroy()
            scrollbar = Scrollbar(main.Frame3_5_3_1,width=10)
            scrollbar.pack( side = RIGHT, fill=Y)          
            mylist = Listbox(main.Frame3_5_3_1, yscrollcommand = scrollbar.set,width=10)
            for i in range(main_calcul.gamma_number):
                mylist.insert(END, str(calib_2D.nimage+1)+".step "+str(i+1))

            mylist.pack( side = LEFT, fill = BOTH )
            mylist.bind("<ButtonRelease-1>", lambda event:show_fit_graph(event,data,main_calcul,calib_2D,stress_calcul,main))                   
            scrollbar.config( command = mylist.yview )

        for widget in main.Frame1_2.winfo_children():
            widget.destroy()         

    main.root.mainloop()    

##################################
def show_fit_graph(event,data,main_calcul,calib_2D,stress_calcul,main):
    for widget in main.Frame3_5_4_1.winfo_children():
        widget.destroy()
    for widget in main.Frame3_5_4_3.winfo_children():
        widget.destroy()
        
    widget = event.widget
    selection=widget.curselection()
    selection = widget.get(selection)
    selection=selection.split()
    i_graph=int(selection[1])-1

    fig=plt.figure(facecolor="0.94")
    
    i=calib_2D.nimage*main_calcul.gamma_number+i_graph
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
                pass
            
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
                    pass
                
        except (IndexError,ValueError):
            showinfo(title="Warning",message="Can not fit background on this graph")
        else:
            try:
                if float(main_calcul.I_alpha1.get())==1:
                    plt.plot(main_calcul.data_x_limit,main_calcul.data_y_k1_fit[i],'b',label=r"I($\lambda_{1}$)")
                if float(main_calcul.I_alpha2.get())==1:
                    plt.plot(main_calcul.data_x_limit,main_calcul.data_y_k2_fit[i],'c',label=r"I($\lambda_{2}$)")
                if float(main_calcul.I_total.get())==1:
                    plt.plot(main_calcul.data_x_limit,main_calcul.data_y_fit_total[i],'m',label=r"I($\lambda_{1}$)"+r" + I($\lambda_{2}$)"+' (r='+str("%0.3f" %main_calcul.r[i])+")")
                for j in range(len(main_calcul.I)):
                    if float(main_calcul.I[j].get())==1:
                        plt.plot(main_calcul.data_x_limit,main_calcul.data_y_fit[i][j],label='I(peak '+str(j+1)+')')
                plt.plot(x,y,'b--',label=r"peak 2$\theta_{1}$ = "+str('%0.2f' % main_calcul.peaks_position[i])+"°"+"\n"+
                         r"I$_{0}$="+str('%0.1f' % main_calcul.peak_intensity[i])+
                         "; FWHM="+str('%0.1f' % main_calcul.FWHM[i])+"°"+
                         "; a="+str('%0.1f' % main_calcul.a[i]))
            except (IndexError,ValueError):
                showinfo(title="Warning",message="Can not fit this graph")
            else:
                Button(main.Frame3_5_4_3,compound=CENTER, text="Export as image",bg="white",command=lambda:export_fit_graph(i_graph,main_calcul,calib_2D,stress_calcul,main)).grid(row=0,column=0) 
                Button(main.Frame3_5_4_3,compound=CENTER, text="Export all as image",bg="white",command=lambda:export_all_fit_graph(main_calcul,calib_2D,stress_calcul,main)).grid(row=1,column=0)
                Button(main.Frame3_5_4_3,compound=CENTER, text="Export as text",bg="white",command=lambda:export_fit_data(i_graph,main_calcul,calib_2D,main)).grid(row=0,column=1)
                Button(main.Frame3_5_4_3,compound=CENTER, text="Export all as text",bg="white",command=lambda:export_all_fit_data(main_calcul,calib_2D,main)).grid(row=1,column=1)

        xlabel=plt.xlabel(r"$2\theta(°)$")
        ylabel=plt.ylabel("Intensity")
    
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
        
        plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0.)

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
            plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0,fontsize=fs)
        
        plt.subplots_adjust(bottom=0.3)
    plt.close(fig)              
    canvas = FigureCanvasTkAgg(fig, master=main.Frame3_5_4_1)
    canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)


    data=data*1

    gamma_start_index=j_start
    gamma_end_index=j_end
    gamma_center_index=int(main_calcul.gamma_f_index+i_graph*main_calcul.gamma_step+main_calcul.gamma_step/2)

    background_f_index=[]
    background_t_index=[]
    for i in range(len(main_calcul.background_f_index)):
        background_f_index=main_calcul.background_f_index
        background_t_index=main_calcul.background_t_index
    twotheta_f_index=main_calcul.twotheta_f_index
    twotheta_t_index=main_calcul.twotheta_t_index
    border_color=max(map(max, data))

    for i in range(len(background_f_index)):
        data[gamma_start_index:gamma_end_index,background_f_index[i]:background_t_index[i]]=0

    #line vertical left and right
    data[gamma_start_index:gamma_end_index,twotheta_f_index-5:twotheta_f_index+6]=border_color*0.75
    data[gamma_start_index:gamma_end_index,twotheta_t_index-5:twotheta_t_index+6]=border_color*0.75
    
    #line center of zone    
    data[gamma_center_index-5:gamma_center_index+6,twotheta_f_index:twotheta_t_index]=border_color
    a=0
    for i in range(len(background_f_index)):
        a=a+background_t_index[i]-background_f_index[i]
    average_line=int(abs(a)/(2*len(background_f_index)))

    #line of zone 
    data[gamma_start_index-5:gamma_start_index+6,twotheta_f_index:twotheta_f_index+average_line]=border_color*0.75
    data[gamma_end_index-5:gamma_end_index+6,twotheta_f_index:twotheta_f_index+average_line]=border_color*0.75

    data[gamma_start_index-5:gamma_start_index+6,twotheta_t_index-average_line:twotheta_t_index]=border_color*0.75
    data[gamma_end_index-5:gamma_end_index+6,twotheta_t_index-average_line:twotheta_t_index]=border_color*0.75

    gamma_y=main_calcul.gamma_y
    twotheta_x=main_calcul.twotheta_x
    nrow=len(gamma_y)
    ncol=len(twotheta_x)
    
    fig=plt.figure(1,facecolor="0.94")
    cmap_var=calib_2D.cmap_var_3_5.get()
    try:
        legend_from= float(calib_2D.Entry_legend_from_3_5.get())
        legend_to= float(calib_2D.Entry_legend_to_3_5.get())
    except ValueError:
        plt.imshow(data, cmap=cmap_var,origin='lower')
    else:
        plt.imshow(data,clim=(legend_from, legend_to),cmap=cmap_var,origin='lower')
 
    plt.title(u"Calib image of \u03C6="+str(main_calcul.phi[calib_2D.nimage])+u"; \u03C7="+str(main_calcul.chi[calib_2D.nimage]))
    plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %gamma_y[0]),str("%0.1f" %gamma_y[int(nrow*0.25)]),str("%0.1f" %gamma_y[int(nrow*0.5)]),str("%0.1f" %gamma_y[int(nrow*0.75)]),str("%0.1f" %gamma_y[int(nrow-1)])))
    plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %twotheta_x[0]),str("%0.1f" %twotheta_x[int(ncol*0.25)]),str("%0.1f" %twotheta_x[int(ncol*0.5)]),str("%0.1f" %twotheta_x[int(ncol*0.75)]),str("%0.1f" %twotheta_x[int(ncol-1)])))
    plt.xlabel(r"$2\theta(°)$")
    plt.ylabel(r"$\gamma(°)$")
    plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
    plt.close()

    for widget in main.Frame3_5_2.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, main.Frame3_5_2)
    canvas.get_tk_widget().pack(side=TOP,expand=YES,fill=BOTH)


    
    main.root.mainloop()
#-----------------------------------------------------------------
def show_stress_graph(event,main_calcul,stress_calcul,calib_2D,main):
    for widget in main.Frame3_6_2_3.winfo_children():
        widget.destroy()
    
    Frame_a=Frame(main.Frame3_6_2_3)
    Frame_a.pack(fill=BOTH, expand=YES)
    Frame_b=Frame(main.Frame3_6_2_3)
    Frame_b.pack(fill=BOTH, expand=YES)
           
    widget = event.widget
    selection=widget.curselection()
    selection = widget.get(selection)
    selection=selection.split(".")
    i_stress=int(selection[0])-1
        
    if stress_calcul.stress_valid>=1:
        Label(Frame_a,text=u'STRESS AT \u03D5 = '+str(stress_calcul.liste_phi[i_stress])+'°').grid(row=0,column=0,sticky=W)
        Label(Frame_a,text="Unit: MPa").grid(row=0,column=1,sticky=W)
        Label(Frame_a,text=u'Sin\u00B2\u03A8 method').grid(row=1,column=0,sticky=W)
        if float(main_calcul.stress_behaviour.get())==1:
            Label(Frame_a,text=u'\u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_linear[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_linear[i_stress])).grid(row=2,column=0,sticky=W)
        if float(main_calcul.stress_behaviour.get())==2:
            Label(Frame_a,text=u'\u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_elliptic[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_elliptic[i_stress])).grid(row=3,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C4\u03D5= '+str('%0.1f' % stress_calcul.shear_phi_elliptic[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_shear_phi_elliptic[i_stress])).grid(row=4,column=0,sticky=W)   

    if len(stress_calcul.liste_phi)>=1:
        Label(Frame_a,text=u'   Fundamental method').grid(row=1,column=2,sticky=W)
        if float(main_calcul.stress_dimension.get())==2:
            if stress_calcul.length_strain>=3 and float(main_calcul.stress_behaviour.get())==1:
                Label(Frame_a,text=u'   \u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_biaxial[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_biaxial[i_stress])).grid(row=2,column=2,sticky=W)
            if stress_calcul.length_strain>=5 and float(main_calcul.stress_behaviour.get())==2:
                Label(Frame_a,text=u'   \u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_biaxial_shear[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_biaxial_shear[i_stress])).grid(row=3,column=2,sticky=W)
                Label(Frame_a,text=u'   \u03C4\u03D5= '+str('%0.1f' % stress_calcul.shear_phi_biaxial_shear[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_shear_phi_biaxial_shear[i_stress])).grid(row=4,column=2,sticky=W)    

        if float(main_calcul.stress_dimension.get())==3:
            if stress_calcul.length_strain>=6:
                Label(Frame_a,text=u'   \u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_triaxial[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_triaxial[i_stress])).grid(row=3,column=2,sticky=W)
                Label(Frame_a,text=u'   \u03C4\u03D5= '+str('%0.1f' % stress_calcul.shear_phi_triaxial[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_shear_phi_triaxial[i_stress])).grid(row=4,column=2,sticky=W)  

    fig=plt.figure(facecolor="0.94")
    ax = fig.add_subplot(111)
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
                        plt.annotate(str(k+1),xy=(stress_calcul.sinpsi_2[i_stress][i],stress_calcul.strain[i_stress][i]))  
                    sinpsi_2.append(stress_calcul.sinpsi_2[i_stress][i])
                    strain.append(stress_calcul.strain[i_stress][i])
                    error_strain.append(stress_calcul.error_strain[i_stress][i])
            if len(strain)>0:
                curve=plt.errorbar(sinpsi_2,strain,yerr=error_strain,fmt='o',capsize=4, elinewidth=1,label=str(j+1)+u".\u03C6= "+str(main_calcul.phi[j])+"°, \u03C7= "+str(main_calcul.chi[j])+'°')

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
                    pass
                
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
    plt.legend(loc='upper left', bbox_to_anchor=(0.0, -0.3, 1, 0),ncol=3,mode="expand",borderaxespad=0.)

    try:
        fs=float(stress_calcul.Entry_fig[1].get())
    except ValueError:
        pass
    else:   
        xlabel.set_fontsize(fs)
        ylabel.set_fontsize(fs)
        plt.xticks(fontsize=fs)
        plt.yticks(fontsize=fs)
        title.set_fontsize(fs)
        plt.legend(loc='upper left', bbox_to_anchor=(0.0, -0.3, 1, 0),ncol=3,mode="expand",borderaxespad=0.,fontsize=fs)
    
    plt.subplots_adjust(bottom=0.4)
    plt.subplots_adjust(left=0.2)
    plt.close(fig)
    
    canvas = FigureCanvasTkAgg(fig, master=Frame_b)
    canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    for widget in main.Frame3_6_3_1.winfo_children():
        widget.destroy()
        
    Button(main.Frame3_6_3_1, text = 'Export as image',bg="white", command = lambda: export_stress_graph(i_stress,main_calcul,stress_calcul,main)).pack()
    Button(main.Frame3_6_3_1, text = 'Export all as image',bg="white", command = lambda: export_all_stress_graph(main_calcul,stress_calcul,main)).pack()
    Button(main.Frame3_6_3_1, text = 'Export all as text',bg="white", command = lambda:export_all_stress_data(calib_2D,main_calcul,stress_calcul,main)).pack()
    Button(main.Frame3_6_3_1, text = 'Export strain',bg="white", command = lambda: export_strain_sin2psi_data(i_stress,main_calcul,stress_calcul,main)).pack()
    
    main.root.mainloop()

def show_stress_tensor(event,main_calcul,stress_calcul,calib_2D,main):
    widget = event.widget
    selection=widget.curselection()
    selection = widget.get(selection)
    
    for widget in main.Frame3_7_2.winfo_children():
        widget.destroy()
    Frame_a=Frame(main.Frame3_7_2)
    Frame_a.pack(fill=BOTH, expand=YES)
    Frame_b=Frame(main.Frame3_7_2)
    Frame_b.pack(fill=BOTH, expand=YES)
    
    for widget in main.Frame3_7_3.winfo_children():
        widget.destroy()
    Frame_c=Frame(main.Frame3_7_3)
    Frame_c.pack(fill=BOTH, expand=YES)
    Frame_d=Frame(main.Frame3_7_3)
    Frame_d.pack(fill=BOTH, expand=YES)
    
    Label(Frame_a,text="Stress at \u03D5(°) = ").grid(row=6,column=0,sticky=W)
    Entry_phi=Entry(Frame_a,width=6)
    Entry_phi.grid(row=6,column=1,sticky=W)
    Entry_phi.insert(0,'0')
    Button(Frame_a, text = 'show',bg="white", command = lambda:simulate_stress_phi(selection,Entry_phi,Frame_a,Frame_c,stress_calcul,main)).grid(row=7,column=1,sticky=W)      

    Label(Frame_c,text=" ").grid(row=6,column=0,sticky=W)
    Label(Frame_c,text=" ").grid(row=7,column=0,sticky=W)

    if selection in "Biaxial":
        Label(Frame_a,text="STRESS TENSOR - Biaxial").grid(row=0,column=0,sticky=W)
        Label(Frame_a,text="Unit: MPa").grid(row=0,column=2,sticky=W) 
         
        Label(Frame_a,text=u'Sin\u00B2\u03A8 method').grid(row=1,column=0,sticky=W)
        if stress_calcul.sigma12_valid==True:
            Label(Frame_a,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_1[1][0,0]))).grid(row=2,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_1[1][1,1]))).grid(row=2,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_1[1][1,1]))).grid(row=3,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_1[1][2,2]))).grid(row=3,column=1,sticky=W)
        if stress_calcul.sigma12_valid==False:
            Label(Frame_a,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_1[1][0,0]))).grid(row=2,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_1[1][1,1]))).grid(row=3,column=1,sticky=W)
            
        fig=plt.figure(facecolor="0.94")
        theta=np.arange(0,math.radians(361),math.radians(5))
        ax = fig.add_subplot(111, polar=True)
        ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial_1))
        ax.set_yticks([max(np.negative(stress_calcul.all_sigma_phi_biaxial_1))])
        ax.set_yticklabels([str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial_1))+'MPa'])
        plt.title(u"Simulation \u03C3 vs \u03D5")
        plt.close(fig)                  
        canvas = FigureCanvasTkAgg(fig, master=Frame_b)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)

        Label(Frame_c,text="").grid(row=0,column=0,sticky=W)
        Label(Frame_c,text="Fundamental method").grid(row=1,column=0,sticky=W)
        if stress_calcul.sigma12_valid==True:
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][0,0]))).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][1,1]))).grid(row=2,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][1,1]))).grid(row=3,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][2,2]))).grid(row=3,column=1,sticky=W)
            #Label(Frame_a,text=u'\u03C3\u209A\u2095= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][3,3]))).grid(row=4,column=0,sticky=W)
        if stress_calcul.sigma12_valid==False:
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][0,0]))).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][1,1]))).grid(row=3,column=1,sticky=W)
            #Label(Frame_a,text=u'\u03C3\u209A\u2095= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][3,3]))).grid(row=4,column=0,sticky=W)
            
        fig=plt.figure(facecolor="0.94")
        theta=np.arange(0,math.radians(361),math.radians(5))
        ax = fig.add_subplot(111, polar=True)
        ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial))
        ax.set_yticks([max(np.negative(stress_calcul.all_sigma_phi_biaxial))])
        ax.set_yticklabels([str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial))+'MPa'])
        plt.title(u"Simulation \u03C3 vs \u03D5")
        plt.close(fig)       
        canvas = FigureCanvasTkAgg(fig, master=Frame_d)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)
#-----------------------------------------------------
    if "shear" in selection:
        Label(Frame_a,text="STRESS TENSOR - Biaxial+shear").grid(row=0,column=0,sticky=W)
        Label(Frame_a,text="Unit: MPa").grid(row=0,column=2,sticky=W)

        Label(Frame_a,text=u'Sin\u00B2\u03A8 method').grid(row=1,column=0,sticky=W)
        if stress_calcul.sigma12_valid==True:
            Label(Frame_a,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][0,0]))).grid(row=2,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][1,1]))).grid(row=2,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][1,1]))).grid(row=3,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][2,2]))).grid(row=3,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][3,3]))).grid(row=2,column=2,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][3,3]))).grid(row=4,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][4])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][4,4]))).grid(row=3,column=2,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][4])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][4,4]))).grid(row=4,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2083= '+str(0)+u"\u00B1"+str(0)).grid(row=4,column=2,sticky=W)
        if stress_calcul.sigma12_valid==False:
            Label(Frame_a,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][0,0]))).grid(row=2,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][1,1]))).grid(row=3,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][2,2]))).grid(row=2,column=2,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][2,2]))).grid(row=4,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][3,3]))).grid(row=3,column=2,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear_1[1][3,3]))).grid(row=4,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2083= '+str(0)+u"\u00B1"+str(0)).grid(row=4,column=2,sticky=W)  
            
        fig=plt.figure(facecolor="0.94")
        theta=np.arange(0,math.radians(361),math.radians(5))
        ax = fig.add_subplot(111, polar=True)
        if stress_calcul.sigma12_valid==True:
            ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial_shear_1))
            ax.set_yticks([max(np.negative(stress_calcul.all_sigma_phi_biaxial_shear_1))])
            ax.set_yticklabels([str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial_shear_1))+'MPa'])
        if stress_calcul.sigma12_valid==False:
            ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial_shear_1))
            ax.set_yticks([max(np.negative(stress_calcul.all_sigma_phi_biaxial_shear_1))])
            ax.set_yticklabels([str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial_shear_1))+'MPa'])
        plt.title(u"Simulation \u03C3 vs \u03D5")
        plt.close(fig)         
        canvas = FigureCanvasTkAgg(fig, master=Frame_b)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)

        Label(Frame_c,text="").grid(row=0,column=0,sticky=W)
        Label(Frame_c,text="Fundamental method").grid(row=1,column=0,sticky=W)
        if stress_calcul.sigma12_valid==True:
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][0,0]))).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][1,1]))).grid(row=2,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][1,1]))).grid(row=3,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][2,2]))).grid(row=3,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][3,3]))).grid(row=2,column=2,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][3,3]))).grid(row=4,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][4])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][4,4]))).grid(row=3,column=2,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][4])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][4,4]))).grid(row=4,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2083= '+str(0)+u"\u00B1"+str(0)).grid(row=4,column=2,sticky=W) 
            #Label(Frame_a,text=u'\u03C3\u209A\u2095= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][5])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][5,5]))).grid(row=5,column=0,sticky=W)
        if stress_calcul.sigma12_valid==False:
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][0,0]))).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][1,1]))).grid(row=3,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][2,2]))).grid(row=2,column=2,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][2,2]))).grid(row=4,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][3,3]))).grid(row=3,column=2,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][3,3]))).grid(row=4,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2083= '+str(0)+u"\u00B1"+str(0)).grid(row=4,column=2,sticky=W) 
            #Label(Frame_a,text=u'\u03C3\u209A\u2095= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][5])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_shear[1][5,5]))).grid(row=5,column=0,sticky=W)
        
        fig=plt.figure(facecolor="0.94")
        theta=np.arange(0,math.radians(361),math.radians(5))
        ax = fig.add_subplot(111, polar=True)
        if stress_calcul.sigma12_valid==True:
            ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial_shear))
            ax.set_yticks([max(np.negative(stress_calcul.all_sigma_phi_biaxial_shear))])
            ax.set_yticklabels([str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial_shear))+'MPa'])
        if stress_calcul.sigma12_valid==False:
            ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial_shear))
            ax.set_yticks([max(np.negative(stress_calcul.all_sigma_phi_biaxial_shear))])
            ax.set_yticklabels([str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial_shear))+'MPa'])
        plt.title(u"Simulation \u03C3 vs \u03D5")
        plt.close(fig)                    
        canvas = FigureCanvasTkAgg(fig, master=Frame_d)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)
#----------------------------------------------------- 
    if selection in "Triaxial":
        Label(Frame_a,text="STRESS TENSOR - Triaxial").grid(row=0,column=0,sticky=W)
        Label(Frame_a,text="Unit: MPa").grid(row=0,column=2,sticky=W)
        
        Label(Frame_a,text=u'Sin\u00B2\u03A8 method').grid(row=1,column=0,sticky=W) 
        Label(Frame_a,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial_1[1][0,0]))).grid(row=2,column=0,sticky=W)
        Label(Frame_a,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial_1[1][1,1]))).grid(row=2,column=1,sticky=W)
        Label(Frame_a,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial_1[1][1,1]))).grid(row=3,column=0,sticky=W)
        Label(Frame_a,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial_1[1][2,2]))).grid(row=3,column=1,sticky=W)
        Label(Frame_a,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial_1[1][3,3]))).grid(row=2,column=2,sticky=W)
        Label(Frame_a,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial_1[1][3,3]))).grid(row=4,column=0,sticky=W)
        Label(Frame_a,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][4])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial_1[1][4,4]))).grid(row=3,column=2,sticky=W)
        Label(Frame_a,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][4])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial_1[1][4,4]))).grid(row=4,column=1,sticky=W)
        Label(Frame_a,text=u'\u03C3\u2083\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][5])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial_1[1][5,5]))).grid(row=4,column=2,sticky=W)

        Label(Frame_a,text=u'unstress peak 2\u03B8= '+str("%0.2f" % stress_calcul.peak_true_1)+'(°)').grid(row=1,column=1,sticky=W)
        
        fig=plt.figure(facecolor="0.94")
        theta=np.arange(0,math.radians(361),math.radians(5))
        ax = fig.add_subplot(111, polar=True)
        ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_triaxial_1))
        ax.set_yticks([max(np.negative(stress_calcul.all_sigma_phi_triaxial_1))])
        ax.set_yticklabels([str('%0.1f' % max(stress_calcul.all_sigma_phi_triaxial_1))+'MPa'])
        plt.title(u"Simulation \u03C3 vs \u03D5")
        plt.close(fig)                   
        canvas = FigureCanvasTkAgg(fig, master=Frame_b)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)

        Label(Frame_c,text="").grid(row=0,column=0,sticky=W)
        Label(Frame_c,text="Fundamental method").grid(row=1,column=0,sticky=W) 
        Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial[1][0,0]))).grid(row=2,column=0,sticky=W)
        Label(Frame_c,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial[1][1,1]))).grid(row=2,column=1,sticky=W)
        Label(Frame_c,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial[1][1,1]))).grid(row=3,column=0,sticky=W)
        Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial[1][2,2]))).grid(row=3,column=1,sticky=W)
        Label(Frame_c,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial[1][3,3]))).grid(row=2,column=2,sticky=W)
        Label(Frame_c,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][3])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial[1][3,3]))).grid(row=4,column=0,sticky=W)
        Label(Frame_c,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][4])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial[1][4,4]))).grid(row=3,column=2,sticky=W)
        Label(Frame_c,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][4])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial[1][4,4]))).grid(row=4,column=1,sticky=W)
        Label(Frame_c,text=u'\u03C3\u2083\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][5])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_triaxial[1][5,5]))).grid(row=4,column=2,sticky=W)

        Label(Frame_c,text=u'unstress peak 2\u03B8= '+str("%0.2f" % stress_calcul.peak_true)+'(°)').grid(row=1,column=1,sticky=W)
        
        fig=plt.figure(facecolor="0.94")
        theta=np.arange(0,math.radians(361),math.radians(5))
        ax = fig.add_subplot(111, polar=True)
        ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_triaxial))
        ax.set_yticks([max(np.negative(stress_calcul.all_sigma_phi_triaxial))])
        ax.set_yticklabels([str('%0.1f' % max(stress_calcul.all_sigma_phi_triaxial))+'MPa'])
        plt.title(u"Simulation \u03C3 vs \u03D5")
        plt.close(fig)                        
        canvas = FigureCanvasTkAgg(fig, master=Frame_d)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)

    main.root.mainloop()

def simulate_stress_phi(selection,Entry_phi,Frame_a,Frame_c,stress_calcul,main):
    try:
        phi_entry=float(Entry_phi.get())
    except ValueError:
        showinfo(title="Error",message="Please insert and verify that phi is a number\nPlease use '.' instead of ',' to insert a number")
    else:
        if selection in "Biaxial":
            if stress_calcul.sigma12_valid==True:
                    #sin2psimethod
                sigma_phi_1= (stress_calcul.tensor_biaxial_1[0][0]*(math.cos(math.radians(phi_entry)))**2+
                              stress_calcul.tensor_biaxial_1[0][1]*math.sin(math.radians(2*phi_entry))+
                              stress_calcul.tensor_biaxial_1[0][2]*(math.sin(math.radians(phi_entry)))**2)
                    #fundamental method
                sigma_phi= (stress_calcul.tensor_biaxial[0][0]*(math.cos(math.radians(phi_entry)))**2+
                            stress_calcul.tensor_biaxial[0][1]*math.sin(math.radians(2*phi_entry))+
                            stress_calcul.tensor_biaxial[0][2]*(math.sin(math.radians(phi_entry)))**2)
            if stress_calcul.sigma12_valid==False:
                    #sin2psimethod
                sigma_phi_1= (stress_calcul.tensor_biaxial_1[0][0]*(math.cos(math.radians(phi_entry)))**2+
                              stress_calcul.tensor_biaxial_1[0][1]*(math.sin(math.radians(phi_entry)))**2)
                    #fundamental method
                sigma_phi= (stress_calcul.tensor_biaxial[0][0]*(math.cos(math.radians(phi_entry)))**2+
                            stress_calcul.tensor_biaxial[0][1]*(math.sin(math.radians(phi_entry)))**2)
        if "shear" in selection:
            if stress_calcul.sigma12_valid==True:
                #sin2psimethod
                sigma_phi_1= (stress_calcul.tensor_biaxial_shear_1[0][0]*(math.cos(math.radians(phi_entry)))**2+
                              stress_calcul.tensor_biaxial_shear_1[0][1]*math.sin(math.radians(2*phi_entry))+
                              stress_calcul.tensor_biaxial_shear_1[0][2]*(math.sin(math.radians(phi_entry)))**2)
                    #fundamental method
                sigma_phi= (stress_calcul.tensor_biaxial_shear[0][0]*(math.cos(math.radians(phi_entry)))**2+
                            stress_calcul.tensor_biaxial_shear[0][1]*math.sin(math.radians(2*phi_entry))+
                            stress_calcul.tensor_biaxial_shear[0][2]*(math.sin(math.radians(phi_entry)))**2)
            if stress_calcul.sigma12_valid==False:
                #sin2psimethod
                sigma_phi_1= (stress_calcul.tensor_biaxial_shear_1[0][0]*(math.cos(math.radians(phi_entry)))**2+
                              stress_calcul.tensor_biaxial_shear_1[0][2]*(math.sin(math.radians(phi_entry)))**2)
                    #fundamental method
                sigma_phi= (stress_calcul.tensor_biaxial_shear[0][0]*(math.cos(math.radians(phi_entry)))**2+
                            stress_calcul.tensor_biaxial_shear[0][2]*(math.sin(math.radians(phi_entry)))**2)
        if selection in "Triaxial":
                #sin2psimethod
            sigma_phi_1= (stress_calcul.tensor_triaxial_1[0][0]*(math.cos(math.radians(phi_entry)))**2+
                          stress_calcul.tensor_triaxial_1[0][1]*math.sin(math.radians(2*phi_entry))+
                          stress_calcul.tensor_triaxial_1[0][2]*(math.sin(math.radians(phi_entry)))**2-
                          stress_calcul.tensor_triaxial_1[0][5])
                #fundamental method
            sigma_phi= (stress_calcul.tensor_triaxial[0][0]*(math.cos(math.radians(phi_entry)))**2+
                        stress_calcul.tensor_triaxial[0][1]*math.sin(math.radians(2*phi_entry))+
                        stress_calcul.tensor_triaxial[0][2]*(math.sin(math.radians(phi_entry)))**2-
                        stress_calcul.tensor_triaxial[0][5])

        Label(Frame_a,text=u'\u03C3\u03D5= '+str('%0.1f' % sigma_phi_1)).grid(row=6,column=2,sticky=W)
        Label(Frame_c,text=u'\u03C3\u03D5= '+str('%0.1f' % sigma_phi)).grid(row=6,column=0,sticky=W)    
    main.root.mainloop()

def show_other_info(event,main_calcul,stress_calcul,main):
    widget = event.widget
    selection=widget.curselection()
    selection = widget.get(selection)
    selection=selection.split(".")
    val=int(selection[0])

    for widget in main.Frame3_8_2.winfo_children():
        widget.destroy()
        
    if val==1:
        fig=plt.figure(facecolor="0.94")
        plt.plot(stress_calcul.phi_calib,stress_calcul.peak_shift,'ro')
        plt.xlabel(u"\u03D5(°)")
        plt.ylabel("peak shift(%)")
        plt.title("Variation of peak shift")
        plt.close(fig)
  
        canvas = FigureCanvasTkAgg(fig, main.Frame3_8_2)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)

    if val==2:
        fig=plt.figure(facecolor="0.94")
        plt.plot(stress_calcul.psi_calib,stress_calcul.peak_shift,'ro')
        plt.xlabel(u"\u03C8(°)")
        plt.ylabel("peak shift(%)")
        plt.title("Variation of peak shift")
        plt.close(fig)

        Entry_degree=Entry(main.Frame3_8_2,width=10)
        Entry_degree.pack(side=BOTTOM)
        Label(main.Frame3_8_2, text="Polynomial degree").pack(side=BOTTOM)
        Button(main.Frame3_8_2, text = 'Fit',bg="white", command = lambda:fit_peak_shift_correction(val,main_calcul.twotheta0,Entry_degree,stress_calcul.psi_calib,stress_calcul.peak_shift,main.Frame3_8_2,main)).pack(side=BOTTOM)
        
        canvas = FigureCanvasTkAgg(fig, main.Frame3_8_2)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)

    if val==3:
        fig=plt.figure(facecolor="0.94")
        plt.plot(stress_calcul.chi_calib,stress_calcul.peak_shift,'ro')
        plt.xlabel(u"\u03C7(°)")
        plt.ylabel("peak shift(%)")
        plt.title("Variation of peak shift")
        plt.close(fig)

        Entry_degree=Entry(main.Frame3_8_2,width=10)
        Entry_degree.pack(side=BOTTOM)
        Label(main.Frame3_8_2, text="Polynomial degree").pack(side=BOTTOM)
        Button(main.Frame3_8_2, text = 'Fit',bg="white", command = lambda:fit_peak_shift_correction(val,main_calcul.twotheta0,Entry_degree,stress_calcul.chi_calib,stress_calcul.peak_shift,main.Frame3_8_2,main)).pack(side=BOTTOM)
        
        canvas = FigureCanvasTkAgg(fig, main.Frame3_8_2)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)

    if val==4:
        fig=plt.figure(facecolor="0.94")
        plt.plot(stress_calcul.gamma_section,stress_calcul.psi_calib,'ro',label=u'\u03A8')
        plt.plot(stress_calcul.gamma_section,stress_calcul.phi_calib,'bo',label=u'\u03D5')
        plt.xlabel(r"$\gamma(°)$")
        plt.ylabel("(°)")
        plt.title(u"\u03D5 and \u03A8 in function of \u03B3")
        plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0.,fontsize='x-small')
        plt.subplots_adjust(bottom=0.3)
        plt.close(fig)
        
        canvas = FigureCanvasTkAgg(fig, master=main.Frame3_8_2)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)

    main.root.mainloop()
