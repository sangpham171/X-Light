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
import os.path
import sys
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import markers
from matplotlib import lines
from tkinter.ttk import Progressbar

def export_original_graph(index,import_XRD,main):            
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

        if index==-1:
            try:
                for j in range(len(import_XRD.phi)):
                    f = plt.figure(1,figsize=(10,10),dpi=100)
                    plt.plot(import_XRD.data_x[j],import_XRD.data_y[j],label=str(j+1))
                plt.xlabel(r"$2\theta(°)$",fontsize=20)
                plt.ylabel("Intensity",fontsize=20)
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                plt.title("All original graph",fontsize=20)
                plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.,fontsize=20)
                plt.subplots_adjust(bottom=0.4)
                plt.savefig(str(name), bbox_inches="tight")
                plt.close()
            except (ValueError, IndexError):
                showinfo(title="Warning",message="Some graphs don't exist")
        #-------------------------------
        else:
            f=plt.figure()
            try:
                fsize=(import_XRD.Entry_fig[0].get()).split(',')
                float(fsize[0])
                float(fsize[1])
            except ValueError:
                showinfo(title="Warning",message="Figsize format: number,number") 
                pass
            else:
                f.set_size_inches(float(fsize[0]),float(fsize[1]))

            try:
                float(import_XRD.Entry_fig[6].get())
            except ValueError:
                showinfo(title="Warning",message="dpi must be a number") 
                pass
            else:
                f.set_dpi(float(import_XRD.Entry_fig[6].get()))
                
            xlabel=plt.xlabel(r"$2\theta(°)$")
            ylabel=plt.ylabel("Intensity")
            title=plt.title(u"\u03C6="+str(float(import_XRD.phi[index]))+'°'+
                            u"; \u03C7="+str(float(import_XRD.chi[index]))+'°'+
                            u"; \u03C9="+str(float(import_XRD.omega[index]))+'°')
            try:
                fs=float(import_XRD.Entry_fig[1].get())
            except ValueError:
                pass
            else:   
                xlabel.set_fontsize(fs)
                ylabel.set_fontsize(fs)
                plt.xticks(fontsize=fs)
                plt.yticks(fontsize=fs)
                title.set_fontsize(fs)

            try:
                curve=plt.plot(import_XRD.data_x[index],import_XRD.data_y[index])
            except (IndexError, ValueError):
                showinfo(title="Warning",message="Graph does not exist") 
                graph_valid=False
            else:
                line=curve[0]
                if import_XRD.Entry_fig[4].get() in dict(colors.BASE_COLORS, **colors.CSS4_COLORS):
                    line.set_color(import_XRD.Entry_fig[4].get())
                else:
                    showinfo(title="Warning",message=str(import_XRD.Entry_fig[4].get())+" is not a color keyword"+
                             "\n Matplotlib https://matplotlib.org/examples/color/named_colors.html")
                    pass

                if import_XRD.Entry_fig[2].get() in dict(markers.MarkerStyle.markers):
                    line.set_marker(import_XRD.Entry_fig[2].get())
                    try:
                        ms=float(import_XRD.Entry_fig[3].get())
                    except ValueError:
                        showinfo(title="Warning",message="Markersize muse be a number")
                    else:
                        line.set_markersize(ms)
                else:
                    showinfo(title="Warning",message=str(import_XRD.Entry_fig[2].get())+" is not a marker keyword"+
                             "\n Matplotlib https://matplotlib.org/api/markers_api.html")
                    pass

                if import_XRD.Entry_fig[5].get() in dict(lines.Line2D.lineStyles):
                    line.set_linestyle(import_XRD.Entry_fig[5].get())
                else:
                    showinfo(title="Warning",message=str(import_XRD.Entry_fig[5].get())+" is not a line style keyword"+
                             "\n Matplotlib https://matplotlib.org/gallery/lines_bars_and_markers/line_styles_reference.html")

            plt.savefig(str(name), bbox_inches="tight")
            plt.close()

    main.root.mainloop()

#-------------------------------------------
def export_all_original_graph(import_XRD,main):
    location=askdirectory(title="Please choose a directory")
    if location is not None and location is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(import_XRD.phi)
  
        for i in range(len(import_XRD.phi)):
            progress["value"] = progress["value"]+1
            progress.update()
            f=plt.figure()
            
            try:
                fsize=(import_XRD.Entry_fig[0].get()).split(',')
                float(fsize[0])
                float(fsize[1])
            except ValueError:
                showinfo(title="Warning",message="Figsize format: number,number") 
                pass
            else:
                f.set_size_inches(float(fsize[0]),float(fsize[1]))

            try:
                float(import_XRD.Entry_fig[6].get())
            except ValueError:
                showinfo(title="Warning",message="dpi must be a number") 
                pass
            else:
                f.set_dpi(float(import_XRD.Entry_fig[6].get()))

            xlabel=plt.xlabel(r"$2\theta(°)$")
            ylabel=plt.ylabel("Intensity")
            title=plt.title(u"\u03C6="+str(float(import_XRD.phi[i]))+'°'+
                            u"; \u03C7="+str(float(import_XRD.chi[i]))+'°'+
                            u"; \u03C9="+str(float(import_XRD.omega[i]))+'°')

            try:
                fs=float(import_XRD.Entry_fig[1].get())
            except ValueError:
                pass
            else:   
                xlabel.set_fontsize(fs)
                ylabel.set_fontsize(fs)
                plt.xticks(fontsize=fs)
                plt.yticks(fontsize=fs)
                title.set_fontsize(fs)

            try:
                curve=plt.plot(import_XRD.data_x[i],import_XRD.data_y[i],'ro',markersize=2)
            except (IndexError, ValueError):
                showinfo(title="Warning",message="Graph does not exist") 
                graph_valid=False
            else:
                line=curve[0]
                if import_XRD.Entry_fig[4].get() in dict(colors.BASE_COLORS, **colors.CSS4_COLORS):
                    line.set_color(import_XRD.Entry_fig[4].get())
                else:
                    showinfo(title="Warning",message=str(import_XRD.Entry_fig[4].get())+" is not a color keyword"+
                             "\n Matplotlib https://matplotlib.org/examples/color/named_colors.html")
                    pass

                if import_XRD.Entry_fig[2].get() in dict(markers.MarkerStyle.markers):
                    line.set_marker(import_XRD.Entry_fig[2].get())
                    try:
                        ms=float(import_XRD.Entry_fig[3].get())
                    except ValueError:
                        showinfo(title="Warning",message="Markersize muse be a number")
                    else:
                        line.set_markersize(ms)
                else:
                    showinfo(title="Warning",message=str(import_XRD.Entry_fig[2].get())+" is not a marker keyword"+
                             "\n Matplotlib https://matplotlib.org/api/markers_api.html")
                    pass

                if import_XRD.Entry_fig[5].get() in dict(lines.Line2D.lineStyles):
                    line.set_linestyle(import_XRD.Entry_fig[5].get())
                else:
                    showinfo(title="Warning",message=str(import_XRD.Entry_fig[5].get())+" is not a line style keyword"+
                             "\n Matplotlib https://matplotlib.org/gallery/lines_bars_and_markers/line_styles_reference.html")
            
                plt.savefig(str(location)+"/original_phi="+str(float(import_XRD.phi[i]))+"; chi="+str(float(import_XRD.chi[i]))+".png", bbox_inches="tight")
            plt.close()
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()
    main.root.mainloop()
#---------------------------------------
def export_fit_graph(index,main_calcul,stress_calcul,main):   
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
    
        try:
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
                x=[main_calcul.peaks_position[index],main_calcul.peaks_position[index]]
                y=[min(main_calcul.data_y_net[index]),max(main_calcul.data_y_limit[index])]
                curve=plt.plot(main_calcul.data_x_limit[index],main_calcul.data_y_limit[index],'ro',markersize=2,label='Original intensity')

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
                x=[main_calcul.peaks_position[index],main_calcul.peaks_position[index]]
                y=[min(main_calcul.data_y_net[index]),max(main_calcul.data_y_net[index])] 
            if float(main_calcul.background.get())==1:    
                plt.plot(main_calcul.data_x_limit[index],main_calcul.data_y_background_fit[index],'k',label='Background')
            if float(main_calcul.net_intensity.get())==1:
                curve=plt.plot(main_calcul.data_x_limit[index],main_calcul.data_y_net[index],'go',markersize=2,label='Net intensity')

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
                    
            if float(main_calcul.I_alpha1.get())==1:
                plt.plot(main_calcul.data_x_limit[index],main_calcul.data_y_k1_fit[index],'b',label="I($\lambda_{1}$)")
            if float(main_calcul.I_alpha2.get())==1:
                plt.plot(main_calcul.data_x_limit[index],main_calcul.data_y_k2_fit[index],'c',label=r"I($\lambda_{2}$)")
            if float(main_calcul.I_total.get())==1:
                plt.plot(main_calcul.data_x_limit[index],main_calcul.data_y_fit_total[index],'m',label=r"I($\lambda_{1}$)"+r" + I($\lambda_{2}$)"+' (r='+str("%0.3f" %main_calcul.r[index])+")")
            plt.plot(x,y,'b--',label=r"peak 2$\theta_{1}$ = "+str('%0.2f' % main_calcul.peaks_position[index])+"°"+"\n"+
                         r"I$_{0}$="+str('%0.1f' % main_calcul.peak_intensity[index])+
                         "; FWHM="+str('%0.1f' % main_calcul.FWHM[index])+"°"+
                         "; a="+str('%0.1f' % main_calcul.a[index]))

            xlabel=plt.xlabel(r"$2\theta(°)$")
            ylabel=plt.ylabel("Intensity")
            if str(index+1) in stress_calcul.list_graph_error:
                title=plt.title("This result is not used in stress calculation\n"+
                                u"\u03C6="+str(main_calcul.phi[index])+'°'+
                                u"; \u03C7="+str(main_calcul.chi[index])+'°'+
                                u"; \u03C9="+str(main_calcul.omega[index])+'°')
            else:
                title=plt.title(u"\u03C6="+str(main_calcul.phi[index])+'°'+
                                u"; \u03C7="+str(main_calcul.chi[index])+'°'+
                                u"; \u03C9="+str(main_calcul.omega[index])+'°')
            
            plt.legend(loc='upper left', bbox_to_anchor=(-0.2, -0.2, 1.2, 0),ncol=2,mode="expand",borderaxespad=0.)

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
        except (IndexError,ValueError):
            plt.close()
            showinfo(title="Warning",message="Can not export this graph")
        else:
            plt.savefig(str(name), bbox_inches="tight")
            plt.close()
    main.root.mainloop()
    
#-------------------------------------------
def export_all_fit_graph(main_calcul,stress_calcul,main):
    location=askdirectory(title="Please choose a directory")
    if location is not None and location is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(main_calcul.phi)
        for i in range(len(main_calcul.phi)):
            progress["value"] = progress["value"]+1
            progress.update()
            try:
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
                
                if float(main_calcul.original.get())==1:
                    x=[main_calcul.peaks_position[i],main_calcul.peaks_position[i]]
                    y=[min(main_calcul.data_y_net[i]),max(main_calcul.data_y_limit[i])]
                    curve=plt.plot(main_calcul.data_x_limit[i],main_calcul.data_y_limit[i],'ro',markersize=2,label='Original intensity')

                    line=curve[0]
                    if main_calcul.Entry_fig[2].get() in dict(markers.MarkerStyle.markers):
                        line.set_marker(main_calcul.Entry_fig[2].get())
                        try:
                            ms=float(main_calcul.Entry_fig[3].get())
                        except ValueError:
                            showinfo(title="Warning",message="Markersize muse be a number")
                        else:
                            line.set_markersize(ms)

                    if main_calcul.Entry_fig[5].get() in dict(lines.Line2D.lineStyles):
                        line.set_linestyle(main_calcul.Entry_fig[5].get())
        
                else:
                    x=[main_calcul.peaks_position[index],main_calcul.peaks_position[index]]
                    y=[min(main_calcul.data_y_net[index]),max(main_calcul.data_y_net[index])]
                if float(main_calcul.background.get())==1:    
                    plt.plot(main_calcul.data_x_limit[i],main_calcul.data_y_background_fit[i],'k',label='Background')
                if float(main_calcul.net_intensity.get())==1:
                    curve=plt.plot(main_calcul.data_x_limit[i],main_calcul.data_y_net[i],'go',markersize=2,label='Net intensity')

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
                    
                if float(main_calcul.I_alpha1.get())==1:
                    plt.plot(main_calcul.data_x_limit[i],main_calcul.data_y_k1_fit[i],'b',label=r"I($\lambda_{1}$)")
                if float(main_calcul.I_alpha2.get())==1:
                    plt.plot(main_calcul.data_x_limit[i],main_calcul.data_y_k2_fit[i],'c',label=r"I($\lambda_{2}$)")
                if float(main_calcul.I_total.get())==1:
                    plt.plot(main_calcul.data_x_limit[i],main_calcul.data_y_fit_total[i],'m',label=r"I($\lambda_{1}$)"+r" + I($\lambda_{2}$)"+' (r='+str("%0.3f" %main_calcul.r[i])+")")
                plt.plot(x,y,'b--',label=r"peak 2$\theta_{1}$ = "+str('%0.2f' % main_calcul.peaks_position[i])+"°"+"\n"+
                         r"I$_{0}$="+str('%0.1f' % main_calcul.peak_intensity[i])+
                         "; FWHM="+str('%0.3f' % main_calcul.FWHM[i])+"°"+
                         "; a="+str('%0.1f' % main_calcul.a[i]))

                xlabel=plt.xlabel(r"$2\theta(°)$")
                ylabel=plt.ylabel("Intensity")
                if str(i+1) in stress_calcul.list_graph_error:
                    title=plt.title("This result is not used in stress calculation\n"+
                                    u"\u03C6="+str(main_calcul.phi[i])+'°'+
                                    u"; \u03C7="+str(main_calcul.chi[i])+'°'+
                                    u"; \u03C9="+str(main_calcul.omega[i])+'°')
                else:
                    title=plt.title(u"\u03C6="+str(main_calcul.phi[i])+'°'+
                                    u"; \u03C7="+str(main_calcul.chi[i])+'°'+
                                    u"; \u03C9="+str(main_calcul.omega[i])+'°')
                    
                plt.legend(loc='upper left', bbox_to_anchor=(-0.2, -0.2, 1.2, 0),ncol=2,mode="expand",borderaxespad=0.)
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
            except (IndexError,ValueError):
                plt.close()
            else:
                plt.savefig(str(location)+"/fitting_phi="+str(float(main_calcul.phi[i]))+"_chi="+str(float(main_calcul.chi[i]))+".png", bbox_inches="tight")
                plt.close()
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()
    main.root.mainloop()

#----------------------------------
def export_stress_graph(index,main_calcul,stress_calcul,main):  
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
     
        if float(main_calcul.experimental.get())==1:
            curve=plt.errorbar(stress_calcul.sinpsi_2[index],stress_calcul.strain[index],yerr=stress_calcul.error_strain[index],fmt='ro',capsize=4,elinewidth=1,label='Experimental')

            line=curve[0]
            if stress_calcul.Entry_fig[4].get() in dict(colors.BASE_COLORS, **colors.CSS4_COLORS):
                line.set_color(stress_calcul.Entry_fig[4].get())
            else:
                showinfo(title="Warning",message=str(stress_calcul.Entry_fig[4].get())+" is not a color keyword"+
                         "\n Matplotlib https://matplotlib.org/examples/color/named_colors.html")
                pass

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
            
            if float(main_calcul.annotate.get())==1:
                for j in range(len(stress_calcul.psi[index])):
                    plt.annotate(str(stress_calcul.index_psi[index][j]),xy=(stress_calcul.sinpsi_2[index][j],stress_calcul.strain[index][j]))
        if stress_calcul.stress_valid>=1:
            if float(main_calcul.stress_behaviour.get())==1 and float(main_calcul.sin2khi_method.get())==1:
                plt.plot(stress_calcul.sinpsi_2_sorted[index],stress_calcul.strain_linear_fit[index],'b',linestyle="-",label=u'Sin\u00B2\u03A8 method')
            if float(main_calcul.stress_behaviour.get())==2 and float(main_calcul.sin2khi_method.get())==1:
                plt.plot(stress_calcul.sinpsi_2_sorted[index],stress_calcul.strain_elliptical_fit[index],'b',linestyle="-",label=u'Sin\u00B2\u03A8 method')    

        if len(stress_calcul.liste_phi)>=1:
            if float(main_calcul.stress_dimension.get())==2:
                if stress_calcul.length_strain>=3 and float(main_calcul.stress_behaviour.get())==1 and float(main_calcul.fundamental_method.get())==1:  
                    plt.plot(stress_calcul.sinpsi_2_sorted[index],stress_calcul.strain_biaxial[index],'m',linestyle="--",label='Fundamental_method')
                if stress_calcul.length_strain>=5 and float(main_calcul.stress_behaviour.get())==2 and float(main_calcul.fundamental_method.get())==1:
                    plt.plot(stress_calcul.sinpsi_2_sorted[index],stress_calcul.strain_biaxial_shear[index],'m',linestyle="--",label='Fundamental_method')

            if float(main_calcul.stress_dimension.get())==3:
                if stress_calcul.length_strain>=6 and float(main_calcul.fundamental_method.get())==1:
                    plt.plot(stress_calcul.sinpsi_2_sorted[index],stress_calcul.strain_triaxial[index],'m',linestyle="--",label='Fundamental_method')
        
        xlabel=plt.xlabel(r"$sin^{2}\psi$")
        ylabel=plt.ylabel('Lattice strain '+r"$\varepsilon$")
        title=plt.title(u"\u03D5="+str(stress_calcul.liste_phi[index])+"°")
        plt.legend(loc='upper left', bbox_to_anchor=(-0.2, -0.3, 1.2, 0),ncol=2,mode="expand",borderaxespad=0.)

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
            plt.legend(loc='upper left', bbox_to_anchor=(-0.2, -0.3, 1.2, 0),ncol=2,mode="expand",borderaxespad=0.,fontsize=fs)
            
        plt.subplots_adjust(bottom=0.4)
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
        for i in range(len(stress_calcul.liste_phi)):
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
            
            if float(main_calcul.experimental.get())==1:
                curve=plt.errorbar(stress_calcul.sinpsi_2[i],stress_calcul.strain[i],yerr=stress_calcul.error_strain[i],fmt='ro',capsize=4,elinewidth=1,label='Experimental')

                line=curve[0]
                if stress_calcul.Entry_fig[4].get() in dict(colors.BASE_COLORS, **colors.CSS4_COLORS):
                    line.set_color(stress_calcul.Entry_fig[4].get())

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
                           
                if float(main_calcul.annotate.get())==1:
                    for j in range(len(stress_calcul.psi[i])):
                        plt.annotate(str(stress_calcul.index_psi[i][j]),xy=(stress_calcul.sinpsi_2[i][j],stress_calcul.strain[i][j]))
            if stress_calcul.stress_valid>=1:
                if float(main_calcul.stress_behaviour.get())==1 and float(main_calcul.sin2khi_method.get())==1:
                    plt.plot(stress_calcul.sinpsi_2_sorted[i],stress_calcul.strain_linear_fit[i],'b',linestyle="-",label=u'Sin\u00B2\u03A8 method')
                if float(main_calcul.stress_behaviour.get())==2 and float(main_calcul.sin2khi_method.get())==1:
                    plt.plot(stress_calcul.sinpsi_2_sorted[i],stress_calcul.strain_elliptical_fit[i],'b',linestyle="-",label=u'Sin\u00B2\u03A8 method')    

            if len(stress_calcul.liste_phi)>=1:
                if float(main_calcul.stress_dimension.get())==2:
                    if stress_calcul.length_strain>=3 and float(main_calcul.stress_behaviour.get())==1 and float(main_calcul.fundamental_method.get())==1:  
                        plt.plot(stress_calcul.sinpsi_2_sorted[i],stress_calcul.strain_biaxial[i],'m',linestyle="--",label='Fundamental_method')
                    if stress_calcul.length_strain>=5 and float(main_calcul.stress_behaviour.get())==2 and float(main_calcul.fundamental_method.get())==1:
                        plt.plot(stress_calcul.sinpsi_2_sorted[i],stress_calcul.strain_biaxial_shear[i],'m',linestyle="--",label='Fundamental_method')

                if float(main_calcul.stress_dimension.get())==3:
                    if stress_calcul.length_strain>=6 and float(main_calcul.fundamental_method.get())==1:
                        plt.plot(stress_calcul.sinpsi_2_sorted[i],stress_calcul.strain_triaxial[i],'m',linestyle="--",label='Fundamental_method')

            xlabel=plt.xlabel(r"$sin^{2}\psi$")
            ylabel=plt.ylabel('Lattice strain '+r"$\varepsilon$")
            title=plt.title(u"\u03D5="+str(stress_calcul.liste_phi[i])+"°")
            plt.legend(loc='upper left', bbox_to_anchor=(-0.2, -0.3, 1.2, 0),ncol=2,mode="expand",borderaxespad=0.)

            try:
                fs=float(stress_calcul.Entry_fig[1].get())
            except ValueError:
                pass
            else:   
                xlabel.set_fontsize(fs)
                ylabel.set_fontsize(fs)
                title.set_fontsize(fs)
                plt.xticks(fontsize=fs)
                plt.yticks(fontsize=fs)
                plt.legend(loc='upper left', bbox_to_anchor=(-0.2, -0.3, 1.2, 0),ncol=2,mode="expand",borderaxespad=0.,fontsize=fs)
            
            plt.subplots_adjust(bottom=0.4)
            plt.savefig(str(location)+"/stress_phi="+str(float(stress_calcul.liste_phi[i]))+".png", bbox_inches="tight")
            plt.close()
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()
    main.root.mainloop()
