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
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import markers
from matplotlib import lines
import numpy as np
import math as math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tools.export_graph_1D import export_original_graph, export_all_original_graph, export_fit_graph, export_all_fit_graph, export_stress_graph, export_all_stress_graph
from tools.export_data_1D import export_original_data, export_all_original_data,export_all_original_data_2,export_fit_data, export_all_fit_data, export_all_stress_data, export_strain_sin2psi_data
from tools.peak_shift_correction import fit_peak_shift_correction
#-------------------------------------------------------------------------------------
def show_original_graph(event,import_XRD,main):
    for widget in main.Frame3_1_2.winfo_children():
        widget.destroy()
    for widget in main.Frame3_1_4.winfo_children():
        widget.destroy()
    
    widget = event.widget
    selection=widget.curselection()
    selection = widget.get(selection)
    selection=selection.split(".")
    index=int(selection[0])-1

    graph_valid=True
    if index==-1:
        try:
            for j in range(len(import_XRD.phi)):
                f = plt.figure(1,facecolor="0.94")
                plt.plot(import_XRD.data_x[j],import_XRD.data_y[j],label=str(j+1))
            plt.xlabel(r"$2\theta$")
            plt.ylabel("Intensity")
            plt.title("All original graphs")
            plt.legend(loc='upper left' , bbox_to_anchor=(0, -0.2, 1, 0), ncol=10,mode="expand",borderaxespad=0.,fontsize='x-small')
            plt.subplots_adjust(bottom=0.4)
            plt.close()
        except (ValueError, IndexError):
            showinfo(title="Warning",message="Some graphs don't exist")
            pass

    else:
        f=plt.figure(facecolor="0.94")
        xlabel=plt.xlabel(r"$2\theta(°)$",fontsize=20)
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
                pass
                
        plt.close()

    if graph_valid==True:
        canvas = FigureCanvasTkAgg(f, main.Frame3_1_2)
        canvas.get_tk_widget().pack(expand=YES,fill=BOTH)

        Frame_a=Frame(main.Frame3_1_4)
        Frame_a.pack(side=TOP,fill=BOTH, expand=YES)
        Frame_b=Frame(main.Frame3_1_4)
        Frame_b.pack(side=BOTTOM,fill=BOTH, expand=YES)
    
        Button(Frame_a, text = 'Export as image',bg="white", command = lambda: export_original_graph(index,import_XRD,main)).grid(row=0,column=0,sticky=W) 
        Button(Frame_a, text = 'Export all as image',bg="white", command = lambda: export_all_original_graph(import_XRD,main)).grid(row=1,column=0,sticky=W)
        Button(Frame_a, text = 'Export as text',bg="white", command = lambda: export_original_data(index,import_XRD,main)).grid(row=2,column=0,sticky=W) 
        Button(Frame_a, text = 'Export all as text',bg="white", command = lambda: export_all_original_data_2(import_XRD,main)).grid(row=3,column=0,sticky=W)


        scrollbar = Scrollbar(Frame_b)
        scrollbar.pack(side = RIGHT, fill=BOTH) 
        mylist = Listbox(Frame_b, yscrollcommand = scrollbar.set)

        for i in range(len(import_XRD.file_info[0])):
            mylist.insert(END,str(import_XRD.file_info[0][i]))

        if index>-1:
            for i in range(len(import_XRD.range_info[index])):
                mylist.insert(END,str(import_XRD.range_info[index][i]))

        mylist.pack(side = LEFT, fill=BOTH,expand=YES)
        scrollbar.config( command = mylist.yview ) 
                
    main.root.mainloop()
#-------------------------------------------------------------------------------------------------------

def show_fit_graph(event,main_calcul,stress_calcul,main):
    for widget in main.Frame3_4_2_1.winfo_children():
        widget.destroy()
    for widget in main.Frame3_4_2_2.winfo_children():
        widget.destroy()
    for widget in main.Frame3_4_3_1.winfo_children():
        widget.destroy()

    widget = event.widget
    selection=widget.curselection()
    selection = widget.get(selection)
    selection=selection.split(".")
    index=int(selection[0])-1

    graph_valid=True
    try:
        residual= list(np.array(main_calcul.data_y_net[index])-np.array(main_calcul.data_y_fit_total[index]))
    except ValueError:
        graph_valid=False
        showinfo(title="Warning",message="This graph doesn't exist")
    
    fig=plt.figure(facecolor="0.94")
    
    if graph_valid==True:
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
                pass
            
        else:
            x=[main_calcul.peaks_position[index],main_calcul.peaks_position[index]]
            y=[min(main_calcul.data_y_net[index]),max(main_calcul.data_y_net[index])] 
   
        try:
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
                    pass
                
        except (IndexError,ValueError):
            showinfo(title="Warning",message="Can not do fitting Pearson VII on this graph")
        else:
            try:  
                if float(main_calcul.I_alpha1.get())==1:
                    plt.plot(main_calcul.data_x_limit[index],main_calcul.data_y_k1_fit[index],'b',label=r"I($\lambda_{1}$)")
                if float(main_calcul.I_alpha2.get())==1:
                    plt.plot(main_calcul.data_x_limit[index],main_calcul.data_y_k2_fit[index],'c',label=r"I($\lambda_{2}$)")
                if float(main_calcul.I_total.get())==1:
                    plt.plot(main_calcul.data_x_limit[index],main_calcul.data_y_fit_total[index],'m',label=r"I($\lambda_{1}$)"+r" + I($\lambda_{2}$)"+' (r='+str("%0.3f" %main_calcul.r[index])+")")
                plt.plot(x,y,'b--',label=r"peak 2$\theta_{1}$ = "+str('%0.2f' % main_calcul.peaks_position[index])+"°"+"\n"+
                         r"I$_{0}$="+str('%0.1f' % main_calcul.peak_intensity[index])+
                         "; FWHM="+str('%0.1f' % main_calcul.FWHM[index])+"°"+
                         "; a="+str('%0.1f' % main_calcul.a[index]))
            except (IndexError,ValueError):
                showinfo(title="Warning",message="Can not do fitting Pearson VII on this graph")
            else:
                Button(main.Frame3_4_3_1, text = 'Export as image',bg="white", command = lambda: export_fit_graph(index,main_calcul,stress_calcul,main)).pack(side=TOP,padx=10, pady=10)
                Button(main.Frame3_4_3_1, text = 'Export all as image',bg="white", command = lambda: export_all_fit_graph(main_calcul,stress_calcul,main)).pack(side=TOP,padx=10, pady=10)
                Button(main.Frame3_4_3_1, text = 'Export as text',bg="white", command = lambda: export_fit_data(index,main_calcul,main)).pack(side=TOP,padx=10, pady=10)
                Button(main.Frame3_4_3_1, text = 'Export all as text',bg="white", command = lambda: export_all_fit_data(main_calcul,main)).pack(side=TOP,padx=10, pady=10)

        xlabel=plt.xlabel(r"$2\theta(°)$")
        ylabel=plt.ylabel("Intensity")
        plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0)
        if str(index+1) in stress_calcul.list_graph_error:
            title=plt.title("This result is not used in stress calculation\n"+
                            u"\u03C6="+str(main_calcul.phi[index])+'°'+
                            u"; \u03C7="+str(main_calcul.chi[index])+'°'+
                            u"; \u03C9="+str(main_calcul.omega[index])+'°')
        else:
            title=plt.title(u"\u03C6="+str(main_calcul.phi[index])+'°'+
                            u"; \u03C7="+str(main_calcul.chi[index])+'°'+
                            u"; \u03C9="+str(main_calcul.omega[index])+'°')

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
    plt.close()
    canvas = FigureCanvasTkAgg(fig, master=main.Frame3_4_2_1)
    canvas.get_tk_widget().pack(fill=BOTH, expand=YES)


    fig=plt.figure(facecolor="0.94")
    plt.plot(main_calcul.data_x_limit[index],residual,'bo',markersize=1)
    plt.xlabel(r"$2\theta(°)$")
    plt.ylabel("Residual")
    plt.close()
    canvas = FigureCanvasTkAgg(fig, master=main.Frame3_4_2_2)
    canvas.get_tk_widget().pack(fill=X, expand=YES)

    
    main.root.mainloop()
#--------------------------------------------------------------------------------
def show_stress_graph(event,main_calcul,stress_calcul,main):
    for widget in main.Frame3_5_2_3.winfo_children():
        widget.destroy()
    for widget in main.Frame3_5_3_1.winfo_children():
        widget.destroy()

    widget = event.widget
    selection=widget.curselection()
    selection = widget.get(selection)
    selection=selection.split(".")
    i_stress=int(selection[0])-1

    Frame_a=Frame(main.Frame3_5_2_3)
    Frame_a.pack(fill=BOTH, expand=YES)
    Frame_b=Frame(main.Frame3_5_2_3)
    Frame_b.pack(fill=BOTH, expand=YES)
    Frame_b.pack_propagate(1)

    fig=plt.figure(facecolor="0.94")
    
    ax = fig.add_subplot(111)
    if float(main_calcul.experimental.get())==1:
        curve=plt.errorbar(stress_calcul.sinpsi_2[i_stress],stress_calcul.strain[i_stress],yerr=stress_calcul.error_strain[i_stress],fmt='ro',capsize=4,elinewidth=1,label='Experimental')

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
            pass
        
        if float(main_calcul.annotate.get())==1:
            for j in range(len(stress_calcul.psi[i_stress])):
                plt.annotate(str(stress_calcul.index_psi[i_stress][j]),xy=(stress_calcul.sinpsi_2[i_stress][j],stress_calcul.strain[i_stress][j]))
    if stress_calcul.stress_valid>=1:
        if float(main_calcul.stress_behaviour.get())==1 and float(main_calcul.sin2khi_method.get())==1 and len(stress_calcul.strain_linear_fit[i_stress])>0:            
            plt.plot(stress_calcul.sinpsi_2_sorted[i_stress],stress_calcul.strain_linear_fit[i_stress],'b',linestyle="-",label=u'Sin\u00B2\u03A8 method')
            
        if float(main_calcul.stress_behaviour.get())==2 and float(main_calcul.sin2khi_method.get())==1 and len(stress_calcul.strain_elliptical_fit[i_stress])>0:
            plt.plot(stress_calcul.sinpsi_2_sorted[i_stress],stress_calcul.strain_elliptical_fit[i_stress],'b',linestyle="-",label=u'Sin\u00B2\u03A8 method')

    if len(stress_calcul.liste_phi)>=1:
        if float(main_calcul.stress_dimension.get())==2:
            if stress_calcul.length_strain>=3 and float(main_calcul.stress_behaviour.get())==1 and float(main_calcul.fundamental_method.get())==1 and len(stress_calcul.strain_biaxial[i_stress])>0:
                plt.plot(stress_calcul.sinpsi_2_sorted[i_stress],stress_calcul.strain_biaxial[i_stress],'m',linestyle="--",label='Fundamental_method')

            if stress_calcul.length_strain>=5 and float(main_calcul.stress_behaviour.get())==2 and float(main_calcul.fundamental_method.get())==1 and len(stress_calcul.strain_biaxial_shear[i_stress])>0:
                plt.plot(stress_calcul.sinpsi_2_sorted[i_stress],stress_calcul.strain_biaxial_shear[i_stress],'m',linestyle="--",label='Fundamental_method')

        if float(main_calcul.stress_dimension.get())==3 and len(stress_calcul.strain_triaxial[i_stress])>0:
            if stress_calcul.length_strain>=6 and float(main_calcul.fundamental_method.get())==1:
                plt.plot(stress_calcul.sinpsi_2_sorted[i_stress],stress_calcul.strain_triaxial[i_stress],'m',linestyle="--",label='Fundamental_method')

    title=plt.title(u"\u03D5 = "+str(stress_calcul.liste_phi[i_stress])+"°")
    xlabel=plt.xlabel(r"$sin^{2}\psi$")
    ylabel=plt.ylabel('Lattice strain '+r"$\varepsilon$")
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
    plt.close()

    if stress_calcul.stress_valid>=1:
        Label(Frame_a,text=u'STRESS AT \u03D5 = '+str(stress_calcul.liste_phi[i_stress])).grid(row=0,column=0,sticky=W)
        Label(Frame_a,text="Unit: MPa").grid(row=0,column=1,sticky=W)
        Label(Frame_a,text=u'Sin\u00B2\u03A8 method').grid(row=1,column=0,sticky=W)
        if float(main_calcul.stress_behaviour.get())==1 and stress_calcul.sigma_phi_linear[i_stress] is not None:
            Label(Frame_a,text=u'\u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_linear[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_linear[i_stress])).grid(row=2,column=0,sticky=W)
        if float(main_calcul.stress_behaviour.get())==2 and stress_calcul.sigma_phi_elliptic[i_stress] is not None:
            Label(Frame_a,text=u'\u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_elliptic[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_elliptic[i_stress])).grid(row=2,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C4\u03D5= '+str('%0.1f' % stress_calcul.shear_phi_elliptic[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_shear_phi_elliptic[i_stress])).grid(row=3,column=0,sticky=W)
            
    if len(stress_calcul.liste_phi)>=1:
        Label(Frame_a,text=u'   Fundamental method').grid(row=1,column=2,sticky=W)
        if float(main_calcul.stress_dimension.get())==2:
            if float(main_calcul.stress_behaviour.get())==1 and stress_calcul.sigma_phi_biaxial[i_stress] is not None:
                Label(Frame_a,text=u'   \u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_biaxial[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_biaxial[i_stress])).grid(row=2,column=2,sticky=W)
            if float(main_calcul.stress_behaviour.get())==2 and stress_calcul.sigma_phi_biaxial_shear[i_stress] is not None:
                Label(Frame_a,text=u'   \u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_biaxial_shear[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_biaxial_shear[i_stress])).grid(row=2,column=2,sticky=W)
                Label(Frame_a,text=u'   \u03C4\u03D5= '+str('%0.1f' % stress_calcul.shear_phi_biaxial_shear[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_shear_phi_biaxial_shear[i_stress])).grid(row=3,column=2,sticky=W)         

        if float(main_calcul.stress_dimension.get())==3 and stress_calcul.sigma_phi_triaxial[i_stress] is not None:
            if stress_calcul.length_strain>=6:
                Label(Frame_a,text=u'   \u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_triaxial[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_triaxial[i_stress])).grid(row=2,column=2,sticky=W)
                Label(Frame_a,text=u'   \u03C4\u03D5= '+str('%0.1f' % stress_calcul.shear_phi_triaxial[i_stress])+u"\u00B1"+str('%0.1f' % stress_calcul.error_shear_phi_triaxial[i_stress])).grid(row=3,column=2,sticky=W)

    canvas = FigureCanvasTkAgg(fig, master=Frame_b)
    canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

    Button(main.Frame3_5_3_1, text = 'Export as image',bg="white", command = lambda: export_stress_graph(i_stress,main_calcul,stress_calcul,main)).pack(side=TOP,padx=10, pady=10)
    Button(main.Frame3_5_3_1, text = 'Export all as image',bg="white", command = lambda: export_all_stress_graph(main_calcul,stress_calcul,main)).pack(side=TOP,padx=10, pady=10)
    Button(main.Frame3_5_3_1, text = 'Export all as text',bg="white", command = lambda:export_all_stress_data(main_calcul,stress_calcul,main)).pack(side=TOP,padx=10, pady=10)
    Button(main.Frame3_5_3_1, text = 'Export strain',bg="white", command = lambda: export_strain_sin2psi_data(i_stress,stress_calcul,main)).pack()
    main.root.mainloop()

def show_stress_tensor(event,stress_calcul,main):
    widget = event.widget
    selection=widget.curselection()
    selection = widget.get(selection)

    for widget in main.Frame3_6_2.winfo_children():
        widget.destroy()
    Frame_a=Frame(main.Frame3_6_2)
    Frame_a.pack(fill=BOTH, expand=YES)
    Frame_b=Frame(main.Frame3_6_2)
    Frame_b.pack(fill=BOTH, expand=YES)
    
    for widget in main.Frame3_6_3.winfo_children():
        widget.destroy()
    Frame_c=Frame(main.Frame3_6_3)
    Frame_c.pack(fill=BOTH, expand=YES)
    Frame_d=Frame(main.Frame3_6_3)
    Frame_d.pack(fill=BOTH, expand=YES)
    
    Label(Frame_a,text="Stress at \u03D5(°)= ").grid(row=6,column=0,sticky=W)
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
        if stress_calcul.stress_valid>=2:
            Label(Frame_a,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][0])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_1[1][0,0]**0.5)).grid(row=2,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_1[1][1,1]**0.5)).grid(row=2,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_1[1][1,1]**0.5)).grid(row=3,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][2])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_1[1][2,2]**0.5)).grid(row=3,column=1,sticky=W)

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

        if len(stress_calcul.liste_phi)>=2 and stress_calcul.length_strain==3:
            Label(Frame_c,text="").grid(row=0,column=0,sticky=W)
            Label(Frame_c,text="Fundamental method").grid(row=1,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][0])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial[1][0,0]**0.5)).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial[1][1,1]**0.5)).grid(row=3,column=1,sticky=W)
            
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
            
        if len(stress_calcul.liste_phi)>=2 and stress_calcul.length_strain>=4:
            Label(Frame_c,text="").grid(row=0,column=0,sticky=W)
            Label(Frame_c,text="Fundamental method").grid(row=1,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][0])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial[1][0,0]**0.5)).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial[1][1,1]**0.5)).grid(row=2,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial[1][1,1]**0.5)).grid(row=3,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][2])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial[1][2,2]**0.5)).grid(row=3,column=1,sticky=W)
            
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
                
    if "shear" in selection:
        Label(Frame_a,text="STRESS TENSOR - Biaxial+shear").grid(row=0,column=0,sticky=W)
        Label(Frame_a,text="Unit: MPa").grid(row=0,column=2,sticky=W)
        Label(Frame_a,text=u'Sin\u00B2\u03A8 method').grid(row=1,column=0,sticky=W)
        if stress_calcul.stress_valid>=2:
            Label(Frame_a,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][0])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[1][0,0]**0.5)).grid(row=2,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[1][1,1]**0.5)).grid(row=2,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[1][1,1]**0.5)).grid(row=3,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][2])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[1][2,2]**0.5)).grid(row=3,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][3])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[1][3,3]**0.5)).grid(row=2,column=2,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][3])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[1][3,3]**0.5)).grid(row=4,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][4])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[1][4,4]**0.5)).grid(row=3,column=2,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[0][4])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear_1[1][4,4]**0.5)).grid(row=4,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2083= '+str(0)+u"\u00B1"+str(0)).grid(row=4,column=2,sticky=W) 
            
            fig=plt.figure(facecolor="0.94")
            theta=np.arange(0,math.radians(361),math.radians(5))
            ax = fig.add_subplot(111, polar=True)
            ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial_shear_1))
            ax.set_yticks([max(np.negative(stress_calcul.all_sigma_phi_biaxial_shear_1))])
            ax.set_yticklabels([str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial_shear_1))+'MPa'])
            plt.title(u"Simulation \u03C3 vs \u03D5")
            plt.close(fig)
                                 
            canvas = FigureCanvasTkAgg(fig, master=Frame_b)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)

        if len(stress_calcul.liste_phi)>=2 and stress_calcul.length_strain==5:
            Label(Frame_c,text="").grid(row=0,column=0,sticky=W)
            Label(Frame_c,text="Fundamental method").grid(row=1,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][0])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][0,0]**0.5)).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][2])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][2,2]**0.5)).grid(row=3,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][3])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][3,3]**0.5)).grid(row=2,column=2,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][3])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][3,3]**0.5)).grid(row=4,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][4])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][4,4]**0.5)).grid(row=3,column=2,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][4])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][4,4]**0.5)).grid(row=4,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2083= '+str(0)+u"\u00B1"+str(0)).grid(row=4,column=2,sticky=W) 
            #Label(Frame_a,text=u'true peak 2\u03B8\u2080= '+str("%0.2f" % stress_calcul.twotheta0_biaxial)+'(°)').grid(row=5,column=0,sticky=W)
            
            fig=plt.figure(facecolor="0.94")
            theta=np.arange(0,math.radians(361),math.radians(5))
            ax = fig.add_subplot(111, polar=True)
            ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial_shear))
            ax.set_yticks([max(np.negative(stress_calcul.all_sigma_phi_biaxial_shear))])
            ax.set_yticklabels([str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial_shear))+'MPa'])
            plt.title(u"Simulation \u03C3 vs \u03D5")
            plt.close(fig)                    
            canvas = FigureCanvasTkAgg(fig, master=Frame_d)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)
            
        if len(stress_calcul.liste_phi)>=2 and stress_calcul.length_strain>=6:
            Label(Frame_c,text="").grid(row=0,column=0,sticky=W)
            Label(Frame_c,text="Fundamental method").grid(row=1,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][0])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][0,0]**0.5)).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][1,1]**0.5)).grid(row=2,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][1,1]**0.5)).grid(row=3,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][2])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][2,2]**0.5)).grid(row=3,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][3])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][3,3]**0.5)).grid(row=2,column=2,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][3])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][3,3]**0.5)).grid(row=4,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][4])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][4,4]**0.5)).grid(row=3,column=2,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_shear[0][4])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_shear[1][4,4]**0.5)).grid(row=4,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2083= '+str(0)+u"\u00B1"+str(0)).grid(row=4,column=2,sticky=W)
            
            fig=plt.figure(facecolor="0.94")
            theta=np.arange(0,math.radians(361),math.radians(5))
            ax = fig.add_subplot(111, polar=True)
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
        if stress_calcul.stress_valid>=3:
            Label(Frame_a,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][0])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial_1[1][0,0]**0.5)).grid(row=2,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial_1[1][1,1]**0.5)).grid(row=2,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial_1[1][1,1]**0.5)).grid(row=3,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][2])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial_1[1][2,2]**0.5)).grid(row=3,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][3])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial_1[1][3,3]**0.5)).grid(row=2,column=2,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][3])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial_1[1][3,3]**0.5)).grid(row=4,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][4])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial_1[1][4,4]**0.5)).grid(row=3,column=2,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][4])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial_1[1][4,4]**0.5)).grid(row=4,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2083\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial_1[0][5])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial_1[1][5,5]**0.5)).grid(row=4,column=2,sticky=W)

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

        if len(stress_calcul.liste_phi)>=3 and stress_calcul.length_strain>=6:
            Label(Frame_c,text="").grid(row=0,column=0,sticky=W)
            Label(Frame_c,text="Fundamental method").grid(row=1,column=0,sticky=W) 
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][0])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial[1][0,0]**0.5)).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial[1][1,1]**0.5)).grid(row=2,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial[1][1,1]**0.5)).grid(row=3,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][2])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial[1][2,2]**0.5)).grid(row=3,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][3])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial[1][3,3]**0.5)).grid(row=2,column=2,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2081= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][3])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial[1][3,3]**0.5)).grid(row=4,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][4])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial[1][4,4]**0.5)).grid(row=3,column=2,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2082= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][4])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial[1][4,4]**0.5)).grid(row=4,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2083\u2083= '+str('%0.1f' % stress_calcul.tensor_triaxial[0][5])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_triaxial[1][5,5]**0.5)).grid(row=4,column=2,sticky=W)

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
                #sin2psimethod
            sigma_phi_1= (stress_calcul.tensor_biaxial_1[0][0]*(math.cos(math.radians(phi_entry)))**2+
                          stress_calcul.tensor_biaxial_1[0][1]*math.sin(math.radians(2*phi_entry))+
                          stress_calcul.tensor_biaxial_1[0][2]*(math.sin(math.radians(phi_entry)))**2)
                #fundamental method
            sigma_phi= (stress_calcul.tensor_biaxial[0][0]*(math.cos(math.radians(phi_entry)))**2+
                        stress_calcul.tensor_biaxial[0][1]*math.sin(math.radians(2*phi_entry))+
                        stress_calcul.tensor_biaxial[0][2]*(math.sin(math.radians(phi_entry)))**2)
        if "shear" in selection:
                #sin2psimethod
            sigma_phi_1= (stress_calcul.tensor_biaxial_shear_1[0][0]*(math.cos(math.radians(phi_entry)))**2+
                          stress_calcul.tensor_biaxial_shear_1[0][1]*math.sin(math.radians(2*phi_entry))+
                          stress_calcul.tensor_biaxial_shear_1[0][2]*(math.sin(math.radians(phi_entry)))**2)
                #fundamental method
            sigma_phi= (stress_calcul.tensor_biaxial_shear[0][0]*(math.cos(math.radians(phi_entry)))**2+
                        stress_calcul.tensor_biaxial_shear[0][1]*math.sin(math.radians(2*phi_entry))+
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

        Label(Frame_a,text=u'\u03C3\u03D5= '+str('%0.1f' % sigma_phi)).grid(row=6,column=2,sticky=W)
        Label(Frame_c,text=u'\u03C3\u03D5= '+str('%0.1f' % sigma_phi_1)).grid(row=6,column=0,sticky=W)       
    main.root.mainloop()

def show_other_info(event,main_calcul,stress_calcul,main):
    widget = event.widget
    selection=widget.curselection()
    selection = widget.get(selection)
    selection=selection.split(".")
    val=int(selection[0])

    for widget in main.Frame3_7_2.winfo_children():
        widget.destroy()

    if val==1:
        fig=plt.figure(facecolor="0.94")
        plt.plot(stress_calcul.phi_calib,stress_calcul.peak_shift,'ro',label='peak shift')
        plt.xlabel(u"\u03D5(°)")
        plt.ylabel("peak shift(%)")
        plt.title("Variation of peak shift")
        plt.close(fig)

        canvas = FigureCanvasTkAgg(fig, master=main.Frame3_7_2)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)

    if val==2:
        fig=plt.figure(facecolor="0.94")
        plt.plot(stress_calcul.psi_calib,stress_calcul.peak_shift,'ro',label='peak shift')
        plt.xlabel(u"\u03C8(°)")
        plt.ylabel("peak shift(%)")
        plt.title("Variation of peak shift")
        plt.close(fig)

        Entry_degree=Entry(main.Frame3_7_2,width=10)
        Entry_degree.pack(side=BOTTOM)
        Label(main.Frame3_7_2, text="Polynomial degree").pack(side=BOTTOM)
        Button(main.Frame3_7_2, text = 'Fit',bg="white", command = lambda:fit_peak_shift_correction(val,main_calcul.twotheta0,Entry_degree,stress_calcul.psi_calib,stress_calcul.peak_shift,main.Frame3_7_2,main)).pack(side=BOTTOM)
        
        canvas = FigureCanvasTkAgg(fig, master=main.Frame3_7_2)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)
    
    main.root.mainloop()
