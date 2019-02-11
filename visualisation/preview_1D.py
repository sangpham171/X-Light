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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import traceback

from fit_function.initial_guess import initial_guess
from fit_function.peak_fit import peak_fit
    
def limit_preview(import_XRD,angles_modif,main):
    for widget in main.Frame3_3_4.winfo_children():
        widget.destroy()

    if import_XRD.angles_modif_valid==True:
        phi=angles_modif.phi*1
        chi=angles_modif.chi*1
        omega=angles_modif.omega*1
        twotheta=angles_modif.twotheta*1
        data_x=angles_modif.data_x*1
    else:
        phi=import_XRD.phi*1
        chi=import_XRD.chi*1
        omega=import_XRD.omega*1
        twotheta=import_XRD.twotheta*1
        data_x=import_XRD.data_x*1

    for i in range(len(phi)):
        f=plt.figure(1,facecolor="0.94")
        plt.plot(data_x[i],import_XRD.data_y[i])

    y1=[max(import_XRD.data_y[0]),max(import_XRD.data_y[0])]
    y2=[min(import_XRD.data_y[0]),min(import_XRD.data_y[0])]
    y3=[(min(import_XRD.data_y[0])+max(import_XRD.data_y[0]))/2,(min(import_XRD.data_y[0])+max(import_XRD.data_y[0]))/2]
    y4=[min(import_XRD.data_y[0]),max(import_XRD.data_y[0])]
  
    try:
        x=[float(import_XRD.Entry_twotheta_from.get()),float(import_XRD.Entry_twotheta_to.get())]
        plt.plot(x,y1,color='red',linewidth=4.0, label = "Fitting range")
    except Exception as e:
        showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
        return

    try:
        background_f=((import_XRD.Entry_background_from.get()).rstrip(',')).split(',')
        background_t=((import_XRD.Entry_background_to.get()).rstrip(',')).split(',')
        for i in range(len(background_f)):
            background_f[i]=float(background_f[i])
            background_t[i]=float(background_t[i])
                
        x=[background_f[0],background_t[0]]
        plt.plot(x,y2,color='black',linewidth=4.0, label = "Background range")
            
        for i in range(1,len(background_f)):
            x=[background_f[i],background_t[i]]
            plt.plot(x,y2,color='black',linewidth=4.0)
    except Exception as e:
        showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
        return

    try:
        twotheta0=float(import_XRD.Entry_twotheta0.get())
        x=[twotheta0,twotheta0]
        plt.plot(x,y4,color='grey',linewidth=2.0, label = "Unstressed peak")
    except Exception as e:
        showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
        return

    peaks_position_ref=[]
    peaks_limit=[]
    try:
        peaks_position_ref.append(float(import_XRD.Entry_peak[0].get()))
    except Exception:
        peaks_position_ref.append(twotheta0)

    try:
        peaks_limit.append(float(import_XRD.Entry_limit_peak[0].get()))
    except Exception:
        peaks_limit.append(1)

    if len(import_XRD.Entry_peak)==2:
        position_ref=((import_XRD.Entry_peak[1].get()).rstrip(',')).split(',')
        for i in range(len(position_ref)):
            try:
                peaks_position_ref.append(float(position_ref[i]))
            except Exception:
                pass
            
    for i in range(len(peaks_position_ref)):
        index=(np.abs(np.asarray(data_x[0])-peaks_position_ref[i])).argmin()
        if index==0 or index==len(data_x[0])-1:
            showinfo(title="Error",message="Peak out of limit")
            return
        
    if len(peaks_position_ref)>=2:
        limit_peak=((import_XRD.Entry_limit_peak[1].get()).rstrip(',')).split(',')
        for i in range(1,len(peaks_position_ref)):
            try:
                peaks_limit.append(float(limit_peak[i]))
            except Exception:
                peaks_limit.append(1)

    for i in range(len(peaks_position_ref)):                
        x=[peaks_position_ref[i]-peaks_limit[i],peaks_position_ref[i]+peaks_limit[i]]
        plt.plot(x,y3,linewidth=2.0, label = "init guess range "+str(i+1))
                               
    plt.xlabel(r"$2\theta$(°)")
    plt.ylabel("Intensity")
    plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0.,fontsize='x-small')
    plt.subplots_adjust(bottom=0.4)
    plt.close()
    
    canvas = FigureCanvasTkAgg(f, main.Frame3_3_4)
    canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
    
    main.root.mainloop()
#------------------------------------
def fit_preview(import_XRD,angles_modif,main):
    if import_XRD.angles_modif_valid==True:
        phi=angles_modif.phi*1
        chi=angles_modif.chi*1
        omega=angles_modif.omega*1
        twotheta=angles_modif.twotheta*1
        data_x=angles_modif.data_x*1
    else:
        phi=import_XRD.phi*1
        chi=import_XRD.chi*1
        omega=import_XRD.omega*1
        twotheta=import_XRD.twotheta*1
        data_x=import_XRD.data_x*1
        
    interval_valid=False
    try:
        twotheta_f=float(import_XRD.Entry_twotheta_from.get())
        twotheta_t=float(import_XRD.Entry_twotheta_to.get())
        background_f=(import_XRD.Entry_background_from.get().rstrip(',')).split(',')
        background_t=(import_XRD.Entry_background_to.get().rstrip(',')).split(',')
        for i in range(len(background_f)):
            background_f[i]=float(background_f[i])
            background_t[i]=float(background_t[i])
        background_polynominal_degrees=int(import_XRD.Entry_background_polynominal_degrees.get())
        kalpha_1=float(import_XRD.Entry_kalpha[0].get())
        kalpha_2=float(import_XRD.Entry_kalpha[1].get())
        kalpha_ratio=float(import_XRD.Entry_kalpha[2].get())
    except Exception as e:
        showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
        return
    else:
        twotheta_findex=(np.abs(np.asarray(data_x[0])-twotheta_f)).argmin()
        twotheta_tindex=(np.abs(np.asarray(data_x[0])-twotheta_t)).argmin()

        background_findex=[]
        background_tindex=[]
        for i in range(len(background_f)):
            background_findex.append((np.abs(np.asarray(data_x[0])-background_f[i])).argmin())
            background_tindex.append((np.abs(np.asarray(data_x[0])-background_t[i])).argmin())
            
        twotheta_f_index=min(twotheta_findex,twotheta_tindex)
        twotheta_t_index=max(twotheta_findex,twotheta_tindex)

        background_f_index=[]
        background_t_index=[]
        for i in range(len(background_findex)):
            background_f_index.append(min(background_findex[i],background_tindex[i]))
            background_t_index.append(max(background_findex[i],background_tindex[i]))
        
        data_x_limit=data_x[0][twotheta_f_index:twotheta_t_index]

        if len(data_x_limit)==0:
            showinfo(title="Error",message="Limits out of range")
            return
            
        peaks_position_ref=[]
        peaks_limit=[]
        peaks_width=[]
        try:
            peaks_position_ref.append(float(import_XRD.Entry_peak[0].get()))
        except Exception:
            try:
                peaks_position_ref.append(float(import_XRD.Entry_twotheta0.get()))
            except Exception:
                showinfo(title="Error",message=u"Please check the value of unstressed 2\u03B8")
                return

        try:
            peaks_limit.append(float(import_XRD.Entry_limit_peak[0].get()))
        except Exception:
            peaks_limit.append(1)

        try:
            peaks_width.append(float(import_XRD.Entry_peak_width[0].get()))
        except Exception:
            peaks_width.append(1)

        if len(import_XRD.Entry_peak)==2:
            position_ref=((import_XRD.Entry_peak[1].get()).rstrip(',')).split(',')
            for i in range(len(position_ref)):
                try:
                    peaks_position_ref.append(float(position_ref[i]))
                except Exception:
                    pass
                
        for i in range(len(peaks_position_ref)):
            index=(np.abs(np.asarray(data_x_limit)-peaks_position_ref[i])).argmin()
            if index==0 or index==len(data_x_limit)-1:
                showinfo(title="Error",message="Peak out of limit")
                return
            
        if len(import_XRD.Entry_peak)==2:
            limit_peak=((import_XRD.Entry_limit_peak[1].get()).rstrip(',')).split(',')
            peak_width=((import_XRD.Entry_peak_width[1].get()).rstrip(',')).split(',')
            for i in range(1,len(peaks_position_ref)):
                try:
                    peaks_limit.append(float(limit_peak[i]))
                except Exception:
                    peaks_limit.append(1)

                try:
                    peaks_width.append(float(peak_width[i]))
                except Exception:
                    peaks_width.append(1)

        interval_valid=True
        
    #------------------------------------
    if interval_valid==True:
        data_x_limit=data_x[0][twotheta_f_index:twotheta_t_index]
        data_y_limit=import_XRD.data_y[0][twotheta_f_index:twotheta_t_index]

        background_data_y_limit=[]
        background_data_x_limit=[]
        for i in range(len(background_f_index)):
            for j in range(background_f_index[i],background_t_index[i]):                      
                background_data_y_limit.append(import_XRD.data_y[0][j])
                background_data_x_limit.append(data_x[0][j])

        try:
            background_fit_coefficient=np.polyfit(background_data_x_limit,background_data_y_limit,background_polynominal_degrees)
        except Exception as e:
            showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
            return
        else:
            data_y_background_fit=[]
            for i in range(len(data_x_limit)):
                data_y_background_fit_i=0
                for j in range(background_polynominal_degrees+1):
                    data_y_background_fit_i=data_y_background_fit_i+background_fit_coefficient[j]*data_x_limit[i]**(background_polynominal_degrees-j)
                data_y_background_fit.append(data_y_background_fit_i)

            data_y_net=[]
            for i in range(len(data_x_limit)):
                data_y_net.append(data_y_limit[i]-data_y_background_fit[i])

            init_guess=float(import_XRD.init_guess.get())
            p0_guess=initial_guess(data_y_net,data_x_limit,peaks_position_ref,peaks_limit,peaks_width,init_guess)
            peak_shape=float(import_XRD.peak_shape.get())
            function_fit=import_XRD.function_fit.get()

            peak_fit_result=peak_fit(data_y_net,data_x_limit,kalpha_1,kalpha_2,kalpha_ratio,p0_guess,peak_shape,function_fit)
            
            if len(peak_fit_result)==0:
                return
            else:
                peaks_position=peak_fit_result[0][0]
                error_peaks_position=peak_fit_result[1][0]
                peak_intensity=peak_fit_result[2][0]
                error_peak_intensity=peak_fit_result[3][0]
                FWHM=peak_fit_result[4][0]
                error_FWHM=peak_fit_result[5][0]
                data_y_fit_total=peak_fit_result[6]
                data_y_k1_fit=peak_fit_result[7]
                data_y_k2_fit=peak_fit_result[8]
                data_y_fit=peak_fit_result[11]

                x1=[twotheta_f,twotheta_t]
                x2=[]
                for i in range(len(background_f)):
                    x2.append([background_f,background_t])
                y1=[min(import_XRD.data_y[0]),min(import_XRD.data_y[0])]
                y2=[max(import_XRD.data_y[0]),max(import_XRD.data_y[0])]
                x4=[peaks_position_ref,peaks_position_ref]
                y3=[min(import_XRD.data_y[0]),max(import_XRD.data_y[0])]
                
                fig=plt.figure(facecolor="0.94")
                plt.xlabel(r"$2\theta$")
                plt.ylabel("Intensity")
                plt.title(u"\u03C6="+str(float(phi[0]))+u"; \u03C7="+str(float(chi[0]))+"")

                plt.plot(data_x[0],import_XRD.data_y[0], label = "Original intensity")
                plt.plot(x1,y2,color='red',linewidth=4.0, label = "Fitting range")
                for i in range(2):
                    plt.plot(x2[0],y1,color='black',linewidth=4.0, label = "Background range")
                plt.plot(x4,y3,color='grey',linewidth=4.0, label = "Peak reference")
                plt.plot(data_x_limit,data_y_background_fit,label='Background')
                plt.plot(data_x_limit,data_y_net,label='Net intensity')
                x=[peaks_position,peaks_position]
                y=[min(data_y_net),max(data_y_limit)]        
                plt.plot(data_x_limit,data_y_k1_fit,label=r"I($\lambda_{1}$)")
                plt.plot(data_x_limit,data_y_k2_fit,label=r"I($\lambda_{2}$)")
                plt.plot(data_x_limit,data_y_fit_total,label=r"I($\lambda_{1}$)"+r" + I($\lambda_{2}$)")
                for i in range(len(data_y_fit)):
                    plt.plot(data_x_limit,data_y_fit[i],label='I(peak '+str(i+1)+')')
                plt.plot(x,y,label=r"peak $2\theta_{1}$ = "+str('%0.2f' % peaks_position)+"(°)")      
                plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0.,fontsize='x-small')
                plt.subplots_adjust(bottom=0.3)
                plt.close()

                for widget in main.Frame3_3_4.winfo_children():
                    widget.destroy()
                
                canvas = FigureCanvasTkAgg(fig, master=main.Frame3_3_4)
                canvas.get_tk_widget().pack(fill=BOTH,expand=YES)
    main.root.mainloop()
#---------------------------------
