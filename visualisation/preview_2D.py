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
from tkinter.filedialog import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import traceback

from fit_function.initial_guess import initial_guess
from fit_function.peak_fit import peak_fit

def limit_preview(calib_2D,angles_modif,main):
    
    limit_valid=False
    try:
        gamma_f=float(calib_2D.Entry_gamma_from.get())
        gamma_t=float(calib_2D.Entry_gamma_to.get())
        gamma_number=int(calib_2D.Entry_gamma_number.get())
        twotheta_f=float(calib_2D.Entry_twotheta_from.get())
        twotheta_t=float(calib_2D.Entry_twotheta_to.get())
        
        background_f=((calib_2D.Entry_background_from.get()).rstrip(',')).split(',')
        background_t=((calib_2D.Entry_background_to.get()).rstrip(',')).split(',')
        for i in range(len(background_f)):
            background_f[i]=float(background_f[i])
            background_t[i]=float(background_t[i])
    except Exception as e:
        showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
        return

    if calib_2D.angles_modif_valid==True:
        twotheta_x=angles_modif.twotheta_x*1
        gamma_y=angles_modif.gamma_y*1
        phi=angles_modif.phi*1
        chi=angles_modif.chi*1
        omega=angles_modif.omega*1
    else:
        twotheta_x=calib_2D.twotheta_x*1
        gamma_y=calib_2D.gamma_y*1
        phi=calib_2D.phi*1
        chi=calib_2D.chi*1
        omega=calib_2D.omega*1

    nrow=calib_2D.nrow
    ncol=calib_2D.ncol

    twotheta_findex=(np.abs(np.asarray(twotheta_x)-twotheta_f)).argmin()
    twotheta_tindex=(np.abs(np.asarray(twotheta_x)-twotheta_t)).argmin()
    gamma_findex=(np.abs(np.asarray(gamma_y)-gamma_f)).argmin()
    gamma_tindex=(np.abs(np.asarray(gamma_y)-gamma_t)).argmin()
    
    background_findex=[]
    background_tindex=[]
    for i in range(len(background_f)):
        background_findex.append((np.abs(np.asarray(twotheta_x)-background_f[i])).argmin())
        background_tindex.append((np.abs(np.asarray(twotheta_x)-background_t[i])).argmin())
            
    twotheta_f_index=min(twotheta_findex,twotheta_tindex)
    twotheta_t_index=max(twotheta_findex,twotheta_tindex)
    gamma_f_index=min(gamma_findex,gamma_tindex)
    gamma_t_index=max(gamma_findex,gamma_tindex)

    background_f_index=[]
    background_t_index=[]
    for i in range(len(background_findex)):
        background_f_index.append(min(background_findex[i],background_tindex[i]))
        background_t_index.append(max(background_findex[i],background_tindex[i]))

    intensity_2D=calib_2D.intensity_2D_calib*1
    
    gamma_step=(gamma_t_index-gamma_f_index)/gamma_number
    gamma_start_1=int(gamma_f_index)
    gamma_end_1=int(gamma_f_index+gamma_step)

    min_twotheta=min(twotheta_f_index,min(background_f_index))
    max_twotheta=max(twotheta_t_index,max(background_t_index))
  
    intensity=[]
    for i in range(min_twotheta,max_twotheta):
        intensity.append(sum(intensity_2D[gamma_start_1:gamma_end_1,i]))

    if len(intensity)==0:
        showinfo(title="Error",message="Limits out of range")
        return
        
    #---zone mesure limit----
    try:
        float(calib_2D.Entry_border_color.get())
    except ValueError:
        border_color=max(map(max, intensity_2D))
    else:
        border_color=float(calib_2D.Entry_border_color.get())
        if border_color<5:
            border_color=5
    #---background limit----
    for i in range(len(background_f_index)):
        intensity_2D[gamma_f_index:gamma_t_index,background_f_index[i]:background_t_index[i]]=0

    #line vertical left and right
    intensity_2D[gamma_f_index:gamma_t_index,twotheta_f_index-5:twotheta_f_index+6]=border_color*0.75
    intensity_2D[gamma_f_index:gamma_t_index,twotheta_t_index-5:twotheta_t_index+6]=border_color*0.75
    
    #line center of each zone
    for i in range(gamma_number):
        gamma_start_index=int(gamma_f_index+i*gamma_step)
        gamma_end_index=int(gamma_f_index+(i+1)*gamma_step)
        gamma_center_index=int(gamma_f_index+i*gamma_step+gamma_step/2)
        
        intensity_2D[gamma_center_index-5:gamma_center_index+6,twotheta_f_index:twotheta_t_index]=border_color

        a=0
        for i in range(len(background_f_index)):
            a=a+background_t_index[i]-background_f_index[i]
        average_line=int(abs(a)/(2*len(background_f_index)))

        #limits zone
        intensity_2D[gamma_start_index-5:gamma_start_index+6,twotheta_f_index:twotheta_f_index+average_line]=border_color*0.75
        intensity_2D[gamma_end_index-5:gamma_end_index+6,twotheta_f_index:twotheta_f_index+average_line]=border_color*0.75

        intensity_2D[gamma_start_index-5:gamma_start_index+6,twotheta_t_index-average_line:twotheta_t_index]=border_color*0.75
        intensity_2D[gamma_end_index-5:gamma_end_index+6,twotheta_t_index-average_line:twotheta_t_index]=border_color*0.75

    fig=plt.figure(1,facecolor="0.94")
    try:
        legend_from= float(calib_2D.Entry_legend_from_3_4.get())
        legend_to= float(calib_2D.Entry_legend_to_3_4.get())
    except ValueError:
        plt.imshow(intensity_2D, cmap="hot",origin='lower')
    else:
        plt.imshow(intensity_2D,clim=(legend_from, legend_to),cmap="hot",origin='lower')

    plt.title(u"Calib image of \u03C6="+str(float(phi[0]))+'°'+
              u"; \u03C7="+str(float(chi[0]))+'°'+
              u"; \u03C9="+str(float(omega[0]))+'°')
    plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %gamma_y[0]),str("%0.1f" %gamma_y[int(nrow*0.25)]),str("%0.1f" %gamma_y[int(nrow*0.5)]),str("%0.1f" %gamma_y[int(nrow*0.75)]),str("%0.1f" %gamma_y[int(nrow-1)])))
    plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %twotheta_x[0]),str("%0.1f" %twotheta_x[int(ncol*0.25)]),str("%0.1f" %twotheta_x[int(ncol*0.5)]),str("%0.1f" %twotheta_x[int(ncol*0.75)]),str("%0.1f" %twotheta_x[int(ncol-1)])))
    plt.xlabel(r"$2\theta(°)$")
    plt.ylabel(r"$\gamma(°)$")
    plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
    plt.close()

    for widget in main.Frame3_4_4_1_1.winfo_children():
        widget.destroy()

    Button(main.Frame3_4_4_1_1,compound=CENTER, text="Export",bg="white",command=lambda:export_limit(intensity_2D,calib_2D.Entry_legend_from_3_4,calib_2D.Entry_legend_to_3_4,nrow,ncol,twotheta_x,gamma_y,phi[0],chi[0],omega[0])).pack(side=BOTTOM)
        
    canvas = FigureCanvasTkAgg(fig, main.Frame3_4_4_1_1)
    canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    #---------------------------------
    fig=plt.figure(1,facecolor="0.94",figsize=(10,10))
    plt.plot(twotheta_x[min_twotheta:max_twotheta],intensity)

    y1=[max(intensity)*1.05, max(intensity)*1.05]
    y2=[min(intensity), min(intensity)]
    y3=[max(intensity), max(intensity)]
    y4=[min(intensity),max(intensity)]

    x=[twotheta_f,twotheta_t]
    plt.plot(x,y1,color='red',linewidth=4.0, label = "Fitting range")

    x=[background_f[0],background_t[0]]
    plt.plot(x,y2,color='black',linewidth=4.0, label = "Background range")
    
    for i in range(1,len(background_f)):
        x=[background_f[i],background_t[i]]
        plt.plot(x,y2,color='black',linewidth=4.0)

    try:
        twotheta0=float(calib_2D.Entry_twotheta0.get())
        x=[twotheta0,twotheta0]
        plt.plot(x,y4,color='grey',linewidth=2.0, label = "Unstressed peak")
    except Exception as e:
        showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
        return

    peaks_position_ref=[]
    peaks_limit=[]

    try:
        peaks_position_ref.append(float(calib_2D.Entry_peak[0].get()))
    except Exception:
        peaks_position_ref.append(twotheta0)

    try:
        peaks_limit.append(float(calib_2D.Entry_limit_peak[0].get()))
    except Exception:
        peaks_limit.append(1)

    if len(calib_2D.Entry_peak)==2:
        position_ref=((calib_2D.Entry_peak[1].get()).rstrip(',')).split(',')
        for i in range(len(position_ref)):
            try:
                peaks_position_ref.append(float(position_ref[i]))
            except Exception:
                pass

    data_x=twotheta_x[min_twotheta:max_twotheta]
    for i in range(len(peaks_position_ref)):
        index=(np.abs(np.asarray(data_x)-peaks_position_ref[i])).argmin()
        if index==0 or index==len(data_x)-1:
            showinfo(title="Error",message="Peak out of limit")
            return
        
    if len(peaks_position_ref)>=2:
        limit_peak=((calib_2D.Entry_limit_peak[1].get()).rstrip(',')).split(',')
        for i in range(1,len(peaks_position_ref)):
            try:
                peaks_limit.append(float(limit_peak[i]))
            except Exception:
                peaks_limit.append(1)

    for i in range(len(peaks_position_ref)):                
        x=[peaks_position_ref[i]-peaks_limit[i],peaks_position_ref[i]+peaks_limit[i]]
        plt.plot(x,y3,linewidth=2.0, label = "init guess range "+str(i+1))
        
    plt.xlabel(r"$2\theta(°)$")
    plt.ylabel("Intensity")
    plt.title("1D integration in azimuthal direction "+r"$\gamma$"+" from "+str("%0.1f" %gamma_y[gamma_start_1])+"° to "+str("%0.1f" %gamma_y[gamma_end_1])+"°")
    plt.legend(loc='best',fontsize='large')
    plt.close(fig)

    for widget in main.Frame3_4_4_2.winfo_children():
        widget.destroy()

    Button(main.Frame3_4_4_2,compound=CENTER, text="Export",bg="white",command=lambda:export_1D_intergration(twotheta_x,min_twotheta,max_twotheta,intensity,twotheta_f,twotheta_t,background_f,background_t,calib_2D,gamma_y,gamma_start_1,gamma_end_1)).pack(side=BOTTOM)
    
    canvas = FigureCanvasTkAgg(fig, main.Frame3_4_4_2)
    canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

def fit_preview(calib_2D,angles_modif,main):
    from fit_function.Pearson_vii_fit import Pearson_vii_fit
    
    limit_valid=False
    try:
        gamma_f=float(calib_2D.Entry_gamma_from.get())
        gamma_t=float(calib_2D.Entry_gamma_to.get())
        gamma_number=int(calib_2D.Entry_gamma_number.get())
        twotheta_f=float(calib_2D.Entry_twotheta_from.get())
        twotheta_t=float(calib_2D.Entry_twotheta_to.get())

        background_f=((calib_2D.Entry_background_from.get()).rstrip(',')).split(',')
        background_t=((calib_2D.Entry_background_to.get()).rstrip(',')).split(',')
        for i in range(len(background_f)):
            background_f[i]=float(background_f[i])
            background_t[i]=float(background_t[i])
        background_polynominal_degrees=int(calib_2D.Entry_background_polynominal_degrees.get())
        kalpha_1=float(calib_2D.Entry_kalpha[0].get())
        kalpha_2=float(calib_2D.Entry_kalpha[1].get())
        kalpha_ratio=float(calib_2D.Entry_kalpha[2].get())
    except Exception as e:
        showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
        return

    if calib_2D.angles_modif_valid==True:
        twotheta_x=angles_modif.twotheta_x*1
        gamma_y=angles_modif.gamma_y*1
        phi=angles_modif.phi*1
        chi=angles_modif.chi*1
        omega=angles_modif.omega*1
    else:
        twotheta_x=calib_2D.twotheta_x*1
        gamma_y=calib_2D.gamma_y*1
        phi=calib_2D.phi*1
        chi=calib_2D.chi*1
        omega=calib_2D.omega*1

    nrow=calib_2D.nrow
    ncol=calib_2D.ncol

    twotheta_findex=(np.abs(np.asarray(twotheta_x)-twotheta_f)).argmin()
    twotheta_tindex=(np.abs(np.asarray(twotheta_x)-twotheta_t)).argmin()
    gamma_findex=(np.abs(np.asarray(gamma_y)-gamma_f)).argmin()
    gamma_tindex=(np.abs(np.asarray(gamma_y)-gamma_t)).argmin()
    background_findex=[]
    background_tindex=[]
    for i in range(len(background_f)):
        background_findex.append((np.abs(np.asarray(twotheta_x)-background_f[i])).argmin())
        background_tindex.append((np.abs(np.asarray(twotheta_x)-background_t[i])).argmin())
            
    twotheta_f_index=min(twotheta_findex,twotheta_tindex)
    twotheta_t_index=max(twotheta_findex,twotheta_tindex)
    gamma_f_index=min(gamma_findex,gamma_tindex)
    gamma_t_index=max(gamma_findex,gamma_tindex)
    
    background_f_index=[]
    background_t_index=[]
    for i in range(len(background_findex)):
        background_f_index.append(min(background_findex[i],background_tindex[i]))
        background_t_index.append(max(background_findex[i],background_tindex[i]))

    peaks_position_ref=[]
    peaks_limit=[]
    peaks_width=[]
    try:
        peaks_position_ref.append(float(calib_2D.Entry_peak[0].get()))
    except Exception:
        try:
            peaks_position_ref.append(float(calib_2D.Entry_twotheta0.get()))
        except Exception:
            showinfo(title="Error",message=u"Please check the value of unstressed 2\u03B8")
            return

    try:
        peaks_limit.append(float(calib_2D.Entry_limit_peak[0].get()))
    except Exception:
        peaks_limit.append(1)

    try:
        peaks_width.append(float(calib_2D.Entry_peak_width[0].get()))
    except Exception:
        peaks_width.append(1)
    
    if len(calib_2D.Entry_peak)==2:
        position_ref=((calib_2D.Entry_peak[1].get()).rstrip(',')).split(',')
        for i in range(len(position_ref)):
            try:
                peaks_position_ref.append(float(position_ref[i]))
            except Exception:
                pass
        
    if len(calib_2D.Entry_peak)==2:
        limit_peak=((calib_2D.Entry_limit_peak[1].get()).rstrip(',')).split(',')
        peak_width=((calib_2D.Entry_peak_width[1].get()).rstrip(',')).split(',')
        for i in range(1,len(peaks_position_ref)):
            try:
                peaks_limit.append(float(limit_peak[i]))
            except Exception:
                peaks_limit.append(1)

            try:
                peaks_width.append(float(peak_width[i]))
            except Exception:
                peaks_width.append(1)
                    
    intensity_2D=calib_2D.intensity_2D_calib*1
    
    gamma_step=(gamma_t_index-gamma_f_index)/gamma_number

    gamma_start_index=int(gamma_f_index)
    gamma_end_index=int(gamma_f_index+gamma_step)
    gamma_center_index=int(gamma_f_index+gamma_step/2)

    data_y_limit=[]
    data_x_limit=[]
    for i in range(twotheta_f_index,twotheta_t_index):                         
        data_y_limit.append(sum(intensity_2D[gamma_start_index:gamma_end_index,i]))
        data_x_limit.append(twotheta_x[i])

    if len(data_y_limit)==0:
        showinfo(title="Error",message="Limits out of range")
        return

    for i in range(len(peaks_position_ref)):
        index=(np.abs(np.asarray(data_x_limit)-peaks_position_ref[i])).argmin()
        if index==0 or index==len(data_x_limit)-1:
            showinfo(title="Error",message="Peak out of limit")
            return

    background_data_y_limit=[]
    background_data_x_limit=[]
    for i in range(len(background_f_index)):
        for j in range(background_f_index[i],background_t_index[i]):
            background_data_y_limit.append(sum(intensity_2D[gamma_start_index:gamma_end_index,j]))
            background_data_x_limit.append(twotheta_x[j])
                                    
    try:
        background_fit_coefficient=np.polyfit(background_data_x_limit,background_data_y_limit,background_polynominal_degrees)
    except Exception as e:
        showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
        return

    data_y_background_fit=[]
    for i in range(len(data_x_limit)):
        data_y_background_fit_i=0
        for j in range(background_polynominal_degrees+1):
            data_y_background_fit_i=data_y_background_fit_i+background_fit_coefficient[j]*data_x_limit[i]**(background_polynominal_degrees-j)
        data_y_background_fit.append(data_y_background_fit_i)

    data_y_net=[]
    for i in range(len(data_x_limit)):
        data_y_net.append(data_y_limit[i]-data_y_background_fit[i])

    init_guess=float(calib_2D.init_guess.get())
    p0_guess=initial_guess(data_y_net,data_x_limit,peaks_position_ref,peaks_limit,peaks_width,init_guess)
    peak_shape=float(calib_2D.peak_shape.get())
    function_fit=calib_2D.function_fit.get()

    peak_fit_result=peak_fit(data_y_net,data_x_limit,kalpha_1,kalpha_2,kalpha_ratio,p0_guess,peak_shape,function_fit)
        
    if len(peak_fit_result)==0:
        return
    else:
        #index_peak=(np.abs(np.asarray(sorted(peaks_position_ref))-peaks_position_ref[0])).argmin()
        #peaks_position=(sorted(peak_fit_result[0]))[index_peak]
        #index_peak=(np.abs(np.asarray(peak_fit_result[0])-peaks_position)).argmin()
        index_peak=0
        
        peaks_position=peak_fit_result[0][index_peak]
        data_y_fit_total=peak_fit_result[6]
        data_y_k1_fit=peak_fit_result[7]
        data_y_k2_fit=peak_fit_result[8]
        data_y_fit=peak_fit_result[11]

        fig=plt.figure(facecolor="0.94")
        plt.xlabel(r"$2\theta(°)$")
        plt.ylabel("Intensity")
        plt.title(u"\u03C6= "+str(calib_2D.phi[0])+u", \u03C7= "+str(calib_2D.chi[0])+"\n"+
            r"$\gamma(°)$"+" integrate from "+str("%0.1f" %(gamma_y[gamma_start_index]))
                  +"° to "+str("%0.1f" %(gamma_y[gamma_end_index]))+"°")
        try:
            plt.plot(data_x_limit,data_y_limit,label='Original intensity')
        except (IndexError,ValueError): 
            pass
        else:
            try:
                plt.plot(data_x_limit,data_y_background_fit,label='Background')
                plt.plot(data_x_limit,data_y_net,label='Net intensity')
            except (IndexError,ValueError): 
                pass
            else:
                try:
                    x=[peaks_position,peaks_position]
                    y=[min(data_y_net),max(data_y_net)]    
                    plt.plot(data_x_limit,data_y_k1_fit,label=r"I($\lambda_{1}$)")
                    plt.plot(data_x_limit,data_y_k2_fit,label=r"I($\lambda_{2}$)")
                    plt.plot(data_x_limit,data_y_fit_total,label=r"I($\lambda_{1}$)"+r" + I($\lambda_{2}$)")
                    for i in range(len(data_y_fit)):
                        plt.plot(data_x_limit,data_y_fit[i],label='I(peak '+str(i+1)+')')
                    plt.plot(x,y,label=r"$2\theta_{1}$ = "+str(peaks_position))
                except (IndexError,ValueError): 
                    pass
        plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0.,fontsize='x-small')
        plt.subplots_adjust(bottom=0.3)
        plt.close()

        for widget in main.Frame3_4_4_2.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=main.Frame3_4_4_2)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)

        #---zone mesure limit----
        try:
            float(calib_2D.Entry_border_color.get())
        except ValueError:
            border_color=max(map(max, intensity_2D))
        else:
            border_color=float(calib_2D.Entry_border_color.get())
            if border_color<5:
                border_color=5
        #---background limit----

        for i in range(len(background_f_index)):
            intensity_2D[gamma_start_index:gamma_end_index,background_f_index[i]:background_t_index[i]]=0

        #line vertical left and right
        intensity_2D[gamma_start_index:gamma_end_index,twotheta_f_index-5:twotheta_f_index+6]=border_color*0.75
        intensity_2D[gamma_start_index:gamma_end_index,twotheta_t_index-5:twotheta_t_index+6]=border_color*0.75
        
        #line center of zone    
        intensity_2D[gamma_center_index-5:gamma_center_index+6,twotheta_f_index:twotheta_t_index]=border_color

        a=0
        for i in range(len(background_f_index)):
            a=a+background_t_index[i]-background_f_index[i]
        average_line=int(abs(a)/(2*len(background_f_index)))
        
        intensity_2D[gamma_start_index-5:gamma_start_index+6,twotheta_f_index:twotheta_f_index+average_line]=border_color*0.75
        intensity_2D[gamma_end_index-5:gamma_end_index+6,twotheta_f_index:twotheta_f_index+average_line]=border_color*0.75

        intensity_2D[gamma_start_index-5:gamma_start_index+6,twotheta_t_index-average_line:twotheta_t_index]=border_color*0.75
        intensity_2D[gamma_end_index-5:gamma_end_index+6,twotheta_t_index-average_line:twotheta_t_index]=border_color*0.75

        fig=plt.figure(1,facecolor="0.94")
        cmap_var=calib_2D.cmap_var_3_4.get()
        try:
            legend_from= float(calib_2D.Entry_legend_from_3_4.get())
            legend_to= float(calib_2D.Entry_legend_to_3_4.get())
        except ValueError:
            plt.imshow(intensity_2D, cmap=cmap_var,origin='lower')
        else:
            plt.imshow(intensity_2D,clim=(legend_from, legend_to),cmap=cmap_var,origin='lower')

        plt.title(u"Calib image of \u03C6="+str(float(phi[0]))+"°"+
                  u"; \u03C7="+str(float(chi[0]))+"°"+
                  u"; \u03C9="+str(float(omega[0]))+"°")
        plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %gamma_y[0]),str("%0.1f" %gamma_y[int(nrow*0.25)]),str("%0.1f" %gamma_y[int(nrow*0.5)]),str("%0.1f" %gamma_y[int(nrow*0.75)]),str("%0.1f" %gamma_y[int(nrow-1)])))
        plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %twotheta_x[0]),str("%0.1f" %twotheta_x[int(ncol*0.25)]),str("%0.1f" %twotheta_x[int(ncol*0.5)]),str("%0.1f" %twotheta_x[int(ncol*0.75)]),str("%0.1f" %twotheta_x[int(ncol-1)])))
        plt.xlabel(r"$2\theta(°)$")
        plt.ylabel(r"$\gamma(°)$")
        plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
        plt.close()

        for widget in main.Frame3_4_4_1_1.winfo_children():
            widget.destroy()
            
        canvas = FigureCanvasTkAgg(fig, main.Frame3_4_4_1_1)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES)
        
    main.root.mainloop() 

def export_limit(intensity_2D,Entry_legend_from,Entry_legend_to,nrow,ncol,twotheta_x,gamma_y,phi,chi,omega):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),('all files','.*')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)
        
        fig=plt.figure(figsize=(10,10),dpi=100)
        try:
            legend_from= float(Entry_legend_from.get())
            legend_to= float(Entry_legend_to.get())
        except ValueError:
            plt.imshow(intensity_2D, cmap="hot",origin='lower')
        else:
            plt.imshow(intensity_2D,clim=(legend_from, legend_to),cmap="hot",origin='lower')

        plt.title(u'\u03C6='+str(float(phi))+"°"+
                  u'; \u03C7='+str(float(chi))+"°"+
                  u'; \u03C9='+str(float(omega))+"°",fontsize=30)
        plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %gamma_y[0]),str("%0.1f" %gamma_y[int(nrow*0.25)]),str("%0.1f" %gamma_y[int(nrow*0.5)]),str("%0.1f" %gamma_y[int(nrow*0.75)]),str("%0.1f" %gamma_y[int(nrow-1)])))
        plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %twotheta_x[0]),str("%0.1f" %twotheta_x[int(ncol*0.25)]),str("%0.1f" %twotheta_x[int(ncol*0.5)]),str("%0.1f" %twotheta_x[int(ncol*0.75)]),str("%0.1f" %twotheta_x[int(ncol-1)])))
        plt.xlabel(r"$2\theta(°)$",fontsize=30)
        plt.ylabel(r"$\gamma(°)$",fontsize=30)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.savefig(str(name), bbox_inches="tight")
        plt.close()
        
def export_1D_intergration(twotheta_x,min_twotheta,max_twotheta,intensity,twotheta_f,twotheta_t,background_f,background_t,calib_2D,gamma_y,gamma_start_1,gamma_end_1):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),('all files','.*')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)

        fig=plt.figure(1,figsize=(10,8))
        plt.plot(twotheta_x[min_twotheta:max_twotheta],intensity)

        y1=[max(intensity)*1.01, max(intensity)*1.01]
        y2=[min(intensity), min(intensity)]
        y3=[max(intensity), max(intensity)]
        y4=[min(intensity),max(intensity)]

        x=[twotheta_f,twotheta_t]
        plt.plot(x,y1,color='red',linewidth=4.0, label = "Fitting range")

        x=[background_f[0],background_t[0]]
        plt.plot(x,y2,color='black',linewidth=4.0, label = "Background range")
        
        for i in range(1,len(background_f)):
            x=[background_f[i],background_t[i]]
            plt.plot(x,y2,color='black',linewidth=4.0)

        try:
            twotheta0=float(calib_2D.Entry_twotheta0.get())
            x=[twotheta0,twotheta0]
            #plt.plot(x,y4,color='grey',linewidth=2.0, label = "Unstressed peak")
        except ValueError:
            showinfo(title="Error",message="Please verify unstressed peak")
            pass

        for i in range(len(calib_2D.Entry_peak)):
            try:
                peaks_position_ref=float(calib_2D.Entry_peak[i].get())
                limit_peak=float(calib_2D.Entry_limit_peak[i].get())
                x=[peaks_position_ref-limit_peak,peaks_position_ref+limit_peak]
                #plt.plot(x,y3,color='blue',linewidth=4.0, label = "Init-range "+str(i+1))
            except ValueError:
                pass
             
        plt.xlabel(r"$2\theta(°)$",fontsize=30)
        plt.ylabel("Intensity",fontsize=30)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.title("1D integration in azimuthal direction\n"+r"$\gamma$"+" from "+str("%0.1f" %gamma_y[gamma_start_1])+"° to "+str("%0.1f" %gamma_y[gamma_end_1])+"°",fontsize=30)
        plt.legend(loc='center left',bbox_to_anchor=(0, -0.4, 0, 0),ncol=1,fontsize=30)
        plt.savefig(str(name),bbox_inches="tight")
        plt.close(fig)
