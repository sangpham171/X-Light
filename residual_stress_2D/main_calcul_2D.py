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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import traceback

from visualisation.fig_style import fig_style
from visualisation.pack_Frame import pack_Frame_2D
from visualisation.show_XRD_2D import show_calib_image, show_fit_graph, show_stress_graph, show_stress_tensor, simulate_stress_phi,show_other_info
from fit_function.initial_guess import initial_guess
from fit_function.peak_fit import peak_fit
from residual_stress_2D.stress_calcul_2D import stress_calcul
from tools.export_image_2D import export_all_stress_graph
from tools.export_data_2D import export_all_stress_data
from read_file.image_2D.read_image_2D import read_data_2D

class main_calcul:
    def __init__(self,calib_2D,import_XRD,angles_modif,main):
        try:
            self.process(calib_2D,import_XRD,angles_modif,main)
        except Exception as e:
            showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
            return
        main.root.mainloop()

        
    def process(self,calib_2D,import_XRD,angles_modif,main):
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Caculation").pack(side=LEFT)
        self.progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        self.progress.pack(side=LEFT)
        self.progress["value"] = 0
        self.progress["maximum"] = len(import_XRD.nfile)+2

        self.progress["value"] = self.progress["value"]+1
        self.progress.update()
        self.check_angles_modif(angles_modif,calib_2D)
        self.check_peak_shift_correction(calib_2D)
        self.check_interval(angles_modif,calib_2D)
        self.check_material(calib_2D)
        self.check_x_ray(calib_2D)
        
        if self.interval_valid==True and self.material_valid==True and self.x_ray_valid==True:
            self.destroy_widget(main)
            self.peak_finder(calib_2D,import_XRD,main) 
            #-----------------------------
            self.show_fitting_frame(import_XRD,calib_2D,angles_modif,stress_calcul,main)
            #----------------------
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            stress_calcul.method_sin2psi(stress_calcul,self)
            stress_calcul.method_fundamental(stress_calcul,self)
            #------------------
            if stress_calcul.stress_valid>=1:
                self.show_stress_graph(import_XRD,stress_calcul,calib_2D,angles_modif,main)
                #-------------------
            if stress_calcul.stress_valid>=2:
                self.show_stress_tensor(stress_calcul,calib_2D,angles_modif,main)
                #------------------
            self.show_variation_peak(stress_calcul,main)

            for widget in main.Frame1_2.winfo_children():
                widget.destroy()

            if stress_calcul.stress_valid>=1:
                pack_Frame_2D(main,6)
            else:
                pack_Frame_2D(main,5)
        
 #-------------------------------------------------
    def check_angles_modif(self,angles_modif,calib_2D):
        if calib_2D.angles_modif_valid==True:
            self.twotheta_x=angles_modif.twotheta_x*1
            self.gamma_y=angles_modif.gamma_y*1
            self.phi=angles_modif.phi*1
            self.chi=angles_modif.chi*1
            self.omega=angles_modif.omega*1
            self.twotheta_center=angles_modif.twotheta_center*1
        else:
            self.twotheta_x=calib_2D.twotheta_x*1
            self.gamma_y=calib_2D.gamma_y*1
            self.phi=calib_2D.phi*1
            self.chi=calib_2D.chi*1
            self.omega=calib_2D.omega*1
            self.twotheta_center=calib_2D.twotheta_center*1

    def check_peak_shift_correction(self,calib_2D):
        self.peak_shift_correction_coefficient=calib_2D.peak_shift_correction_coefficient*1
            
    def check_interval(self,angles_modif,calib_2D):
        self.interval_valid=False
        #check_entry_number
        try:
            gamma_f=float(calib_2D.Entry_gamma_from.get())
            gamma_t=float(calib_2D.Entry_gamma_to.get())
            self.gamma_number=int(calib_2D.Entry_gamma_number.get())
            twotheta_f=float(calib_2D.Entry_twotheta_from.get())
            twotheta_t=float(calib_2D.Entry_twotheta_to.get())
            
            background_f=((calib_2D.Entry_background_from.get()).rstrip(',')).split(',')
            background_t=((calib_2D.Entry_background_to.get()).rstrip(',')).split(',')
            for i in range(len(background_f)):
                background_f[i]=float(background_f[i])
                background_t[i]=float(background_t[i])
                
            self.background_polynominal_degrees=int(calib_2D.Entry_background_polynominal_degrees.get())
        except ValueError:
            showinfo(title="Error",message="Please insert all the limit parameters and verify that they are number\nPlease use '.' instead of ',' to insert a number")
            return

        #find index limit
        twotheta_findex=(np.abs(np.asarray(self.twotheta_x)-twotheta_f)).argmin()
        twotheta_tindex=(np.abs(np.asarray(self.twotheta_x)-twotheta_t)).argmin()
        gamma_findex=(np.abs(np.asarray(self.gamma_y)-gamma_f)).argmin()
        gamma_tindex=(np.abs(np.asarray(self.gamma_y)-gamma_t)).argmin()
       
        background_findex=[]
        background_tindex=[]
        for i in range(len(background_f)):
            background_findex.append((np.abs(np.asarray(self.twotheta_x)-background_f[i])).argmin())
            background_tindex.append((np.abs(np.asarray(self.twotheta_x)-background_t[i])).argmin())

        #check limit
        self.twotheta_f_index=min(twotheta_findex,twotheta_tindex)
        self.twotheta_t_index=max(twotheta_findex,twotheta_tindex)
        self.gamma_f_index=min(gamma_findex,gamma_tindex)
        self.gamma_t_index=max(gamma_findex,gamma_tindex)
        
        self.background_f_index=[]
        self.background_t_index=[]
        for i in range(len(background_findex)):
            self.background_f_index.append(min(background_findex[i],background_tindex[i]))
            self.background_t_index.append(max(background_findex[i],background_tindex[i]))
     
        #append limit
        self.data_x_limit=self.twotheta_x[self.twotheta_f_index:self.twotheta_t_index]

        if len(self.data_x_limit)==0:
            showinfo(title="Error",message="Limits out of range")
            return

        self.gamma_step=(self.gamma_t_index-self.gamma_f_index)/self.gamma_number

        #check peaks reference
        self.peaks_position_ref=[]
        self.peaks_limit=[]
        self.peaks_width=[]
        try:
            self.peaks_position_ref.append(float(calib_2D.Entry_peak[0].get()))
        except Exception:
            try:
                peaks_position_ref.append(float(calib_2D.Entry_twotheta0.get()))
            except Exception:
                return

        try:
            self.peaks_limit.append(float(calib_2D.Entry_limit_peak[0].get()))
        except Exception:
            self.peaks_limit.append(1)

        try:
            self.peaks_width.append(float(calib_2D.Entry_peak_width[0].get()))
        except Exception:
            self.peaks_width.append(1)
        
        if len(calib_2D.Entry_peak)==2:
            position_ref=((calib_2D.Entry_peak[1].get()).rstrip(',')).split(',')
            for i in range(len(position_ref)):
                try:
                    self.peaks_position_ref.append(float(position_ref[i]))
                except Exception:
                    pass
            
        if len(calib_2D.Entry_peak)==2:
            limit_peak=((calib_2D.Entry_limit_peak[1].get()).rstrip(',')).split(',')
            peak_width=((calib_2D.Entry_peak_width[1].get()).rstrip(',')).split(',')
            for i in range(1,len(self.peaks_position_ref)):
                try:
                    self.peaks_limit.append(float(limit_peak[i]))
                except Exception:
                    self.peaks_limit.append(1)

                try:
                    self.peaks_width.append(float(peak_width[i]))
                except Exception:
                    self.peaks_width.append(1)

        for i in range(len(self.peaks_position_ref)):
            index=(np.abs(np.asarray(self.data_x_limit)-self.peaks_position_ref[i])).argmin()
            if index==0 or index==len(self.data_x_limit)-1:
                showinfo(title="Error",message="Peak out of limit")
                return

        self.interval_valid=True

    #----------------------------------------------
    def check_material(self,calib_2D):
        self.material_valid=False
        try:
            self.twotheta0=float(calib_2D.Entry_twotheta0.get())
        except ValueError:
            showinfo(title="Error",message="Please check the value of unstressed 2\u03B8")
            return
        else:
            try:
                self.s1=float(calib_2D.Entry_s1.get())
                self.s2_2=float(calib_2D.Entry_half_s2.get())
            except ValueError:
                try:
                    Young=float(calib_2D.Entry_Young.get())
                    Poisson=float(calib_2D.Entry_Poisson.get())
                except ValueError:
                    showinfo(title="Error",message="Please check the value of (s1,s2/2) or (E,v)")
                    return

                self.s1=-Poisson/Young
                self.s2_2=(Poisson+1)/Young
                self.material_valid=True

        self.material_valid=True
    #----------------------------------------------
    def check_x_ray(self,calib_2D):
        self.x_ray_valid=False
        try:
            self.kalpha_1=float(calib_2D.Entry_kalpha[0].get())
            self.kalpha_2=float(calib_2D.Entry_kalpha[1].get())
            self.kalpha_ratio=float(calib_2D.Entry_kalpha[2].get())
        except ValueError:
            showinfo(title="Error",message="Please check the value of X-ray propreties")
            return
        self.x_ray_valid=True
 #-------------------------------------------------              
    def read_data_i(self,nimage,import_XRD):
        data=read_data_2D(nimage,import_XRD)
        data_dim=len(data.shape)
        
        if data_dim==2: 
            pass
        elif data_dim==3:
            nimage_i=import_XRD.nimage_i[nimage]
            data=data[nimage_i]
        else:
            data=[]
        
        return(data)
#------------------------------------------------- 
    def calib_data_i(self,data,nimage,import_XRD,calib_2D):
        from residual_stress_2D.calib_XRD_2D import calib_pyFai

        rotate=import_XRD.rotate
        flip=import_XRD.flip
        twotheta_center=import_XRD.twotheta_center[nimage]

        if rotate==0:
            intensity_2D=data
            nrow=import_XRD.nrow[nimage]
            ncol=import_XRD.ncol[nimage]
            center_row=import_XRD.center_row[nimage]
            center_col=import_XRD.center_col[nimage]
        
        if rotate==90:
            intensity_2D=np.rot90(data,k=1,axes=(0, 1))
            nrow=import_XRD.ncol[nimage]
            ncol=import_XRD.nrow[nimage]
            center_row=import_XRD.center_col[nimage]
            center_col=import_XRD.center_row[nimage]
                            
        if rotate==180: 
            intensity_2D=np.rot90(data,k=2,axes=(0, 1))
            nrow=import_XRD.nrow[nimage]
            ncol=import_XRD.ncol[nimage]
            center_row=import_XRD.center_row[nimage]
            center_col=import_XRD.center_col[nimage]
                                
        if rotate==270:
            intensity_2D=np.rot90(data,k=3,axes=(0, 1))
            nrow=import_XRD.ncol[nimage]
            ncol=import_XRD.nrow[nimage]
            center_row=import_XRD.center_col[nimage]
            center_col=import_XRD.center_row[nimage]

        if flip==1:
            intensity_2D=np.flip(intensity_2D,axis=0)
            
        if flip==2:
            intensity_2D=np.flip(intensity_2D,axis=1)
        
        calib=calib_pyFai(import_XRD,intensity_2D,nrow,ncol,center_row,center_col,twotheta_center)

        intensity_2D_calib=calib[0]
        if float(calib_2D.Check_twotheta_flip.get())==1:
            intensity_2D_calib=np.flip(intensity_2D_calib,axis=0)
        else:
            intensity_2D_calib=intensity_2D_calib

        return(intensity_2D_calib)

#-------------------------------------------------
    def peak_finder(self,calib_2D,import_XRD,main):                          
        self.data_y_limit=[]                #list of experimental intensity in the selected range, 2 dimensional list; self.data_y_limit=[[list_intensity],[list_intensity],...]
        self.data_y_background_fit=[]       #list of intensity of the background fit, 2 dimensional list; [[],[],...]
        self.data_y_net=[]                  #list of net intensity, 2 dimensional list; [[],[],...]
        self.data_y_k1_fit=[]               #list of intensity of kalpha1 fit, 2 dimensional list; [[],[],...]
        self.data_y_k2_fit=[]               #list of intensity of kalpha2 fit, 2 dimensional list; [[],[],...]
        self.data_y_fit_total=[]            #list of intensity of kalpha1+kalpha2 fit, 2 dimensional list; [[],[],...]
        self.data_y_fit=[]                  #list of intensity of fit, 2 dimensional list; [[peak1],[peak2],...]
        self.peaks_position=[]              #list of peak position, 1 dimensional list
        self.error_peaks_position=[]        #list of uncertainty of peak position, 1 dimensional list
        self.peak_intensity=[]              #list of peak intensity, 1 dimensional list
        self.error_peak_intensity=[]        #list of uncertainty of peak intensity, 1 dimensional list
        self.FWHM=[]                        #list of Full Width at Haft Maximum, 1 dimensional list
        self.error_FWHM=[]                  #list of uncertainty of Full Width at Haft Maximum, 1 dimensional list
        self.r=[]                           #list of correlation coefficient, 1 dimensional list
        self.a=[]                           #list of symetry/astrimetry coefficient, 1 dimensional list
        self.peak_non_valide=[]             #list of peak non valide (can't not performe the peak finder process), 1 dimensional list
        self.peak_rejection=[]              #list of rejected peak by correlation coefficient, 1 dimensional list
        
        try:
            r=float(calib_2D.Entry_r.get())     #check correlation coefficient
        except ValueError:
            r=0

        for nimage in range(len(import_XRD.nfile)):
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()

            intensity_2D=self.read_data_i(nimage,import_XRD)   #read data
            
            try:
                calib_data=self.calib_data_i(intensity_2D,nimage,import_XRD,calib_2D)
            except Exception:
                for i_gamma in range(self.gamma_number):
                    self.data_y_background_fit.append([])
                    self.data_y_net.append([])
                    self.append_zero()
                    self.peak_non_valide.append(nimage*self.gamma_number+i_gamma)

                    calib_data=[]
            
            if len(calib_data)>0:
                calib_2D.nimage=nimage
                self.intensity_2D_calib=calib_data
                
                for i_gamma in range(self.gamma_number):
                    data_y_limit=[]
                    g_start=int(self.gamma_f_index+i_gamma*self.gamma_step)
                    g_end=int(self.gamma_f_index+(i_gamma+1)*self.gamma_step)
                    for i in range(self.twotheta_f_index,self.twotheta_t_index):                         
                        data_y_limit.append(sum(self.intensity_2D_calib[g_start:g_end,i]))
                    self.data_y_limit.append(data_y_limit)              #list of experimental intensity in the selected range, 2 dimensional list; self.data_y_limit=[[list_intensity],[list_intensity],...]

                    try:
                        background_data_y_limit=[]
                        background_data_x_limit=[]
                        for i in range(len(self.background_f_index)):
                            for j in range(self.background_f_index[i],self.background_t_index[i]):
                                background_data_y_limit.append(sum(self.intensity_2D_calib[g_start:g_end,j]))
                                background_data_x_limit.append(self.twotheta_x[j])       

                        background_fit_coefficient=np.polyfit(background_data_x_limit,background_data_y_limit,self.background_polynominal_degrees)                    
                    except (IndexError,ValueError, RuntimeError) as e:
                        self.data_y_background_fit.append([])
                        self.data_y_net.append([])
                        self.append_zero()
                        self.peak_non_valide.append(nimage*self.gamma_number+i_gamma)

                        showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))

                    else:
                        data_y_background_fit=[]
                        for i in range(len(self.data_x_limit)):
                            data_y_background_fit_i=0
                            for j in range(self.background_polynominal_degrees+1):
                                data_y_background_fit_i=data_y_background_fit_i+background_fit_coefficient[j]*self.data_x_limit[i]**(self.background_polynominal_degrees-j)
                            data_y_background_fit.append(data_y_background_fit_i)

                        data_y_net=[]
                        for i in range(len(self.data_x_limit)):
                            data_y_net.append(data_y_limit[i]-data_y_background_fit[i])

                        self.data_y_background_fit.append(data_y_background_fit)        #list of intensity of the background fit, 2 dimensional list; [[],[],...]
                        self.data_y_net.append(data_y_net)                              #list of net intensity, 2 dimensional list; [[],[],...]

                        init_guess=float(calib_2D.init_guess.get())
                        p0_guess=initial_guess(data_y_net,self.data_x_limit,self.peaks_position_ref,self.peaks_limit,self.peaks_width,init_guess)
                        peak_shape=float(calib_2D.peak_shape.get())
                        function_fit=calib_2D.function_fit.get()

                        peak_fit_result=peak_fit(data_y_net,self.data_x_limit,self.kalpha_1,self.kalpha_2,self.kalpha_ratio,p0_guess,peak_shape,function_fit)
                                
                        if len(peak_fit_result)==0:
                            self.append_zero()
                            self.peak_non_valide.append(nimage*self.gamma_number+i_gamma)
                        else:
                            #index_peak=(np.abs(np.asarray(sorted(self.peaks_position_ref))-self.peaks_position_ref[0])).argmin()
                            #peaks_position=(sorted(peak_fit_result[0]))[index_peak]
                            #index_peak=(np.abs(np.asarray(peak_fit_result[0])-peaks_position)).argmin()
                            index_peak=0
                                
                            self.peaks_position.append(peak_fit_result[0][index_peak])
                            self.error_peaks_position.append(peak_fit_result[1][index_peak])
                            self.peak_intensity.append(peak_fit_result[2][index_peak])
                            self.error_peak_intensity.append(peak_fit_result[3][index_peak])
                            self.FWHM.append(peak_fit_result[4][index_peak])
                            self.error_FWHM.append(peak_fit_result[5][index_peak])
                            self.data_y_fit_total.append(peak_fit_result[6])
                            self.data_y_k1_fit.append(peak_fit_result[7])
                            self.data_y_k2_fit.append(peak_fit_result[8])
                            self.r.append(peak_fit_result[9])
                            self.a.append(peak_fit_result[10][index_peak])
                            self.data_y_fit.append(peak_fit_result[11])
                            if self.r[nimage*self.gamma_number+i_gamma]<r:
                                self.peak_rejection.append(nimage*self.gamma_number+i_gamma)
                                
        self.Entry_peak_non_valide=Entry(main.Frame3_6_2_1,width=100)
        self.Entry_peak_rejection=Entry(main.Frame3_6_2_1,width=100)
        self.Entry_peak_remove=Entry(main.Frame3_6_2_1,width=100)
        self.Entry_image_remove=Entry(main.Frame3_6_2_1,width=100)
        for i in range(len(self.peak_non_valide)):
            nimage=int(self.peak_non_valide[i]/self.gamma_number)
            igraph=self.peak_non_valide[i]-nimage*self.gamma_number
            self.Entry_peak_non_valide.insert(END,str(nimage+1)+"."+str(igraph+1)+",")
        for i in range(len(self.peak_rejection)):
            nimage=int(self.peak_rejection[i]/self.gamma_number)
            igraph=self.peak_rejection[i]-nimage*self.gamma_number
            self.Entry_peak_non_valide.insert(END,str(nimage+1)+"."+str(igraph+1)+",")
    #-----------------------------------------
    def show_fitting_frame(self,import_XRD,calib_2D,angles_modif,stress_calcul,main):
        self.original = IntVar()
        Check_button=Checkbutton(main.Frame3_5_4_2, text="Original intensity", variable=self.original)
        Check_button.grid(row=0,column=0,sticky=W)
        Check_button.select()
        
        self.background = IntVar()
        Check_button=Checkbutton(main.Frame3_5_4_2, text="Background", variable=self.background)
        Check_button.grid(row=1,column=0,sticky=W)
        Check_button.select()
        
        self.net_intensity = IntVar()
        Check_button=Checkbutton(main.Frame3_5_4_2, text="Net intensity", variable=self.net_intensity)
        Check_button.grid(row=0,column=1,sticky=W)
        Check_button.select()

        self.I_total = IntVar()
        Check_button=Checkbutton(main.Frame3_5_4_2, text="I fit total", variable=self.I_total)
        Check_button.grid(row=1,column=1,sticky=W)
        Check_button.select()
        
        self.I_alpha1 = IntVar()
        Check_button=Checkbutton(main.Frame3_5_4_2, text=u"I (\u03BB\u2081)", variable=self.I_alpha1)
        Check_button.grid(row=0,column=2,sticky=W)
        Check_button.select()
        
        self.I_alpha2 = IntVar()
        Check_button=Checkbutton(main.Frame3_5_4_2, text=u"I (\u03BB\u2082)", variable=self.I_alpha2)
        Check_button.grid(row=1,column=2,sticky=W)
        Check_button.select()

        self.I=[]
        for i in range(len(self.data_y_fit[0])):
            self.I.append(IntVar())
            Check_button=Checkbutton(main.Frame3_5_4_2, text="I peak "+str(i+1), variable=self.I[i])
            if i%2==0:
                Check_button.grid(row=0,column=3+i,sticky=W)
                Check_button.select()
            else:
                Check_button.grid(row=1,column=2+i,sticky=W)
                Check_button.select()
               
        scrollbar = Scrollbar(main.Frame3_5_1)
        scrollbar.pack(side = RIGHT, fill=Y) 
        mylist= Listbox(main.Frame3_5_1, yscrollcommand = scrollbar.set)
        mylist.pack(side = LEFT, fill = BOTH,expand=YES)
        for i in range(len(self.phi)):
            mylist.insert(END, str(i+1)+u'.\u03C6='+str(self.phi[i])+" ; "+u'\u03C7='+str(self.chi[i])+u"; \u03C9="+str(self.omega[i])+
                          ' (.'+str(import_XRD.nfile[i]+1)+'.'+str(import_XRD.nimage_i[i]+1)+'.)')
        mylist.bind("<ButtonRelease-1>", lambda event: show_calib_image(event,angles_modif,calib_2D,import_XRD,self,stress_calcul,main.Frame3_5_2,main))
        scrollbar.config(command = mylist.yview) 

        scrollbar = Scrollbar(main.Frame3_5_3_1,width=10)
        scrollbar.pack( side = RIGHT, fill=Y)          
        mylist = Listbox(main.Frame3_5_3_1, yscrollcommand = scrollbar.set ,width=10)
        for i in range(self.gamma_number):
            mylist.insert(END, str(calib_2D.nimage+1)+".step "+str(i+1))
        mylist.pack( side = LEFT, fill = BOTH )
        mylist.bind("<ButtonRelease-1>", lambda event:show_fit_graph(event,self.intensity_2D_calib,self,calib_2D,stress_calcul,main))                   
        scrollbar.config( command = mylist.yview )

        i=calib_2D.nimage*self.gamma_number
        j_start=int(self.gamma_f_index)
        j_end=int(self.gamma_f_index+self.gamma_step)

        fig=plt.figure(facecolor="0.94")
        plt.xlabel(r"$2\theta(°)$")
        plt.ylabel("Intensity")
        plt.title(u"\u03C6= "+str(self.phi[calib_2D.nimage])+'°'+
                  u", \u03C7= "+str(self.chi[calib_2D.nimage])+'°'+
                  u", \u03C9= "+str(self.omega[calib_2D.nimage])+'°\n'+
                  r"$\gamma(°)$"+" integrate from "+str("%0.1f" %(self.gamma_y[j_start]))+
                  "° to "+str("%0.1f" %(self.gamma_y[j_end]))+"°")
        try:
            plt.plot(self.data_x_limit,self.data_y_limit[i],label='Original intensity')
        except (IndexError,ValueError): 
            pass
        else:
            try:
                plt.plot(self.data_x_limit,self.data_y_background_fit[i],label='Background')
                plt.plot(self.data_x_limit,self.data_y_net[i],label='Net intensity')
            except (IndexError,ValueError): 
                pass
            else:
                try:
                    x=[self.peaks_position[i],self.peaks_position[i]]
                    y=[min(self.data_y_net[i]),max(self.data_y_net[i])]    
                    plt.plot(self.data_x_limit,self.data_y_k1_fit[i],label=r"I($\lambda_{1}$)")
                    plt.plot(self.data_x_limit,self.data_y_k2_fit[i],label=r"I($\lambda_{2}$)")
                    plt.plot(self.data_x_limit,self.data_y_fit_total[i],label=r"I($\lambda_{1}$)"+r" + I($\lambda_{2}$)")
                    for j in range(len(self.data_y_fit[0])):
                        plt.plot(self.data_x_limit,self.data_y_fit[i][j],label='I(peak '+str(j+1)+')')
                    plt.plot(x,y,label=r"$2\theta_{1}$ = "+str(self.peaks_position[i])+"°")
                except (IndexError,ValueError): 
                    pass
        plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0.,fontsize='x-small')
        plt.subplots_adjust(bottom=0.3)
        plt.close()
        canvas = FigureCanvasTkAgg(fig, master=main.Frame3_5_4_1)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)

        fig_style(self,main.Frame3_5_3_3)
#----------------------------------------------------------
    def modification_stress(self,import_XRD,stress_calcul,calib_2D,angles_modif,main):
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()
        
        Label(main.Frame1_2,text="Caculation").pack(side=LEFT)
        self.progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        self.progress.pack(side=LEFT)
        self.progress["value"] = 0
        self.progress["maximum"] = 7

        self.check_angles_modif(angles_modif,calib_2D)
        self.check_peak_shift_correction(calib_2D)
        #--------------------------
        self.progress["value"] = self.progress["value"]+1
        self.progress.update()
        self.check_interval(angles_modif,calib_2D)
        #--------------------------
        self.progress["value"] = self.progress["value"]+1
        self.progress.update()
        self.check_material(calib_2D)
        #--------------------------
        self.progress["value"] = self.progress["value"]+1
        self.progress.update()
        self.check_x_ray(calib_2D)
        
        if self.interval_valid==True and self.material_valid==True and self.x_ray_valid==True:
            self.destroy_widget_2(main)
            #----------------------
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            stress_calcul.method_sin2psi(stress_calcul,self)
            #----------------------
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            stress_calcul.method_fundamental(stress_calcul,self)
            #------------------
            if stress_calcul.stress_valid>=1:
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.show_stress_graph(import_XRD,stress_calcul,calib_2D,angles_modif,main)
                #-------------------
            if stress_calcul.stress_valid>=2:
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.show_stress_tensor(stress_calcul,calib_2D,angles_modif,main)
                #------------------
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            self.show_variation_peak(stress_calcul,main)

            for widget in main.Frame1_2.winfo_children():
                widget.destroy()

            if stress_calcul.stress_valid>=1:
                pack_Frame_2D(main,6)
            else:
                pack_Frame_2D(main,5)
                
        main.root.mainloop()
            
#####################-----------------------------------###################################
    def show_stress_graph(self,import_XRD,stress_calcul,calib_2D,angles_modif,main):      
        self.experimental = IntVar()
        Check_button=Checkbutton(main.Frame3_6_3_2, text="Experimental", variable=self.experimental)
        Check_button.grid(row=0,column=0,sticky=W)
        Check_button.select()

        self.annotate = IntVar()
        Check_button=Checkbutton(main.Frame3_6_3_2, text="Annotate", variable=self.annotate)
        Check_button.grid(row=1,column=0,sticky=W)
        Check_button.select()

        if stress_calcul.stress_valid>=1:
            self.sin2khi_method = IntVar()
            Check_button=Checkbutton(main.Frame3_6_3_2, text=u'Sin\u00B2\u03A8 method', variable=self.sin2khi_method)
            Check_button.grid(row=2,column=0,sticky=W)
            Check_button.select()

            self.fundamental_method = IntVar()
            Check_button=Checkbutton(main.Frame3_6_3_2, text="Fundamental method", variable=self.fundamental_method)
            Check_button.grid(row=3,column=0,sticky=W)
            Check_button.select()
                
        #--Frame3_6-----------------------------------------------------    
        scrollbar = Scrollbar(main.Frame3_6_1)
        scrollbar.pack( side = RIGHT, fill=Y)                               
        mylist= Listbox(main.Frame3_6_1, yscrollcommand = scrollbar.set )
        for i in range(len(stress_calcul.liste_phi)):
            mylist.insert(END, str(i+1)+u".\u03D5="+str(float(stress_calcul.liste_phi[i])))
        mylist.pack( side = LEFT, fill = BOTH )
        mylist.bind("<ButtonRelease-1>", lambda event: show_stress_graph(event,self,stress_calcul,calib_2D,main))
        scrollbar.config( command = mylist.yview )

        Label(main.Frame3_6_2_1, text="(Frames number.Section number)(1.2,3.5,...)").grid(row=0,column=1,sticky=W)
        Label(main.Frame3_6_2_1, text="Graph non valide").grid(row=1,column=0,sticky=W)
        self.Entry_peak_non_valide.grid(row=1,column=1,sticky=W)
        self.Entry_peak_non_valide.config(state='disabled')
        Label(main.Frame3_6_2_1, text="Peak rejection").grid(row=2,column=0,sticky=W)
        self.Entry_peak_rejection.grid(row=2,column=1,sticky=W)
        self.Entry_peak_rejection.config(state='disabled')
        Label(main.Frame3_6_2_1, text="Remove peaks",bg="white").grid(row=3,column=0,sticky=W)
        self.Entry_peak_remove.grid(row=3,column=1,sticky=W)
        Label(main.Frame3_6_2_1, text="Remove image",bg="white").grid(row=4,column=0,sticky=W)
        self.Entry_image_remove.grid(row=4,column=1,sticky=W)
        Button(main.Frame3_6_2_1,compound=CENTER, text="APPLY MODIFICATION",bg="white",command=lambda:self.modification_stress(import_XRD,stress_calcul,calib_2D,angles_modif,main)).grid(row=5,column=1,sticky=W)

        Label(main.Frame3_6_2_2, text="Stress behaviour").grid(row=0,column=0,sticky=W)
        self.stress_behaviour = IntVar()
        Radiobutton(main.Frame3_6_2_2, text="No Shear", variable=self.stress_behaviour, value=1).grid(row=1,column=0,sticky=W)
        Radiobutton(main.Frame3_6_2_2, text="Shear", variable=self.stress_behaviour, value=2).grid(row=2,column=0,sticky=W)
        self.stress_behaviour.set(1)

        self.stress_dimension = IntVar()
        self.stress_dimension.set(2)
        if len(stress_calcul.liste_phi)>=3:
            Label(main.Frame3_6_2_2, text="Stress dimension").grid(row=0,column=1,sticky=W)
            Radiobutton(main.Frame3_6_2_2, text="Biaxial", variable=self.stress_dimension, value=2).grid(row=1,column=1,sticky=W)
            Radiobutton(main.Frame3_6_2_2, text="Triaxial", variable=self.stress_dimension, value=3).grid(row=2,column=1,sticky=W)
            
        Frame_a=Frame(main.Frame3_6_2_3)
        Frame_a.pack(fill=BOTH, expand=YES)
        Frame_b=Frame(main.Frame3_6_2_3)
        Frame_b.pack(fill=BOTH, expand=YES)

        if stress_calcul.stress_valid>=1:
            Label(Frame_a,text=u'STRESS AT \u03D5 = '+str(stress_calcul.liste_phi[0])).grid(row=0,column=0,sticky=W)
            Label(Frame_a,text="Unit: MPa").grid(row=0,column=1,sticky=W)
            Label(Frame_a,text=u'Sin\u00B2\u03A8 method').grid(row=1,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_linear[0])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_linear[0])).grid(row=2,column=0,sticky=W)
           
        if len(stress_calcul.liste_phi)>=1:
            Label(Frame_a,text=u'   Fundamental method').grid(row=1,column=2,sticky=W)
            if stress_calcul.length_strain>=3:
                Label(Frame_a,text=u'   \u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_biaxial[0])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_biaxial[0])).grid(row=2,column=2,sticky=W)
           
        fig=plt.figure(facecolor="0.94")
        ax = fig.add_subplot(111)
        i=-1
        for j in range(len(self.phi)):
            sinpsi_2=[]
            strain=[]
            for k in range(self.gamma_number):
                if (j*self.gamma_number+k) in stress_calcul.index_peak[0]:
                    i=i+1
                    plt.annotate(str(k+1),xy=(stress_calcul.sinpsi_2[0][i],stress_calcul.strain[0][i]))
                    sinpsi_2.append(stress_calcul.sinpsi_2[0][i])
                    strain.append(stress_calcul.strain[0][i])
            if len(strain)>0:
                plt.plot(sinpsi_2,strain,'o',label=str(j+1)+u".\u03C6= "+str(self.phi[j])+u", \u03C7= "+str(self.chi[j]))

        if stress_calcul.stress_valid>=1:
            plt.plot(stress_calcul.sinpsi_2_sorted[0],stress_calcul.strain_linear_fit[0],'b',label=u'Sin\u00B2\u03A8 method')     

        if len(stress_calcul.liste_phi)>=1:
            if stress_calcul.length_strain>=3:
                plt.plot(stress_calcul.sinpsi_2_sorted[0],stress_calcul.strain_biaxial[0],'m',label='Fundamental method')

        plt.xlabel(r"$sin^{2}\psi$")
        plt.ylabel('Elastic strain '+r"$\varepsilon$")
        plt.title(u"\u03D5 = "+str(stress_calcul.liste_phi[0])+"")
        plt.legend(loc='upper left', bbox_to_anchor=(0.0, -0.3, 1, 0),ncol=3,mode="expand",borderaxespad=0.,fontsize='x-small')
        plt.subplots_adjust(bottom=0.4)
        plt.subplots_adjust(left=0.2)
        plt.close(fig)
                             
        canvas = FigureCanvasTkAgg(fig, master=Frame_b)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

        Button(main.Frame3_6_3_1, text = 'Export all as image',bg="white", command = lambda: export_all_stress_graph(self,stress_calcul,main)).pack()
        Button(main.Frame3_6_3_1, text = 'Export all as text',bg="white", command = lambda:export_all_stress_data(calib_2D,self,stress_calcul,main)).pack()

        fig_style(stress_calcul,main.Frame3_6_3_3)

        #---Frame3_7----------------------------------------------
    def show_stress_tensor(self,stress_calcul,calib_2D,angles_modif,main):
        self.selection="Biaxial"
        scrollbar = Scrollbar(main.Frame3_7_1)
        scrollbar.pack( side = RIGHT, fill=Y)                               
        mylist = Listbox(main.Frame3_7_1, yscrollcommand = scrollbar.set )        
        mylist.insert(END, "Biaxial")
        mylist.insert(END, "Biaxial+shear")
        if len(stress_calcul.liste_phi)>=3:
            mylist.insert(END, "Triaxial")
        mylist.pack( side = LEFT, fill = BOTH )
        mylist.bind("<ButtonRelease-1>", lambda event: show_stress_tensor(event,self,stress_calcul,calib_2D,main))
        scrollbar.config( command = mylist.yview )
        
        Frame_a=Frame(main.Frame3_7_2)
        Frame_a.pack(fill=BOTH, expand=YES)
        Frame_b=Frame(main.Frame3_7_2)
        Frame_b.pack(fill=BOTH, expand=YES)

        Label(Frame_a,text="STRESS TENSOR - Biaxial").grid(row=0,column=0,sticky=W)
        Label(Frame_a,text="Unit: MPa").grid(row=0,column=2,sticky=W)
        
        Label(Frame_a,text=u'Sin\u00B2\u03A8 method').grid(row=1,column=0,sticky=W)
        if stress_calcul.stress_valid>=2:
            Label(Frame_a,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][0])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_1[1][0,0]**0.5)).grid(row=2,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_1[1][1,1]**0.5)).grid(row=2,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_1[1][1,1]**0.5)).grid(row=3,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][2])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial_1[1][2,2]**0.5)).grid(row=3,column=1,sticky=W)
       
            fig=plt.figure(facecolor="0.94")
            theta=np.arange(0,np.radians(361),np.radians(5))
            ax = fig.add_subplot(111, polar=True)
            ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial_1))
            ax.set_yticks([min(np.negative(stress_calcul.all_sigma_phi_biaxial_1)),max(np.negative(stress_calcul.all_sigma_phi_biaxial_1))])
            ax.set_yticklabels([str('%0.1f' % min(stress_calcul.all_sigma_phi_biaxial_1))+'MPa',str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial_1))+'MPa'])
            plt.title(u"Simulation \u03C3 vs \u03D5")
            plt.close(fig)               
            canvas = FigureCanvasTkAgg(fig, master=Frame_b)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)

        Frame_c=Frame(main.Frame3_7_3)
        Frame_c.pack(fill=BOTH, expand=YES)
        Frame_d=Frame(main.Frame3_7_3)
        Frame_d.pack(fill=BOTH, expand=YES)

        Label(Frame_c,text="").grid(row=0,column=0,sticky=W)
        Label(Frame_c,text="Fundamental method").grid(row=1,column=0,sticky=W)
        if len(stress_calcul.liste_phi)>=2:
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][0])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial[1][0,0]**0.5)).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial[1][1,1]**0.5)).grid(row=2,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][1])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial[1][1,1]**0.5)).grid(row=3,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][2])+u"\u00B1"+str('%0.1f' % stress_calcul.tensor_biaxial[1][2,2]**0.5)).grid(row=3,column=1,sticky=W)
            
            fig=plt.figure(facecolor="0.94")
            theta=np.arange(0,np.radians(361),np.radians(5))
            ax = fig.add_subplot(111, polar=True)
            ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial))
            ax.set_yticks([min(np.negative(stress_calcul.all_sigma_phi_biaxial)),max(np.negative(stress_calcul.all_sigma_phi_biaxial))])
            ax.set_yticklabels([str('%0.1f' % min(stress_calcul.all_sigma_phi_biaxial))+'MPa',str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial))+'MPa'])
            plt.title("Simulation stress-phi")
            plt.close(fig)                                     
            canvas = FigureCanvasTkAgg(fig, master=Frame_d)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)             

        #--FRame3_8--------------------------------
    def show_variation_peak(self,stress_calcul,main):
        scrollbar = Scrollbar(main.Frame3_8_1)
        scrollbar.pack( side = RIGHT, fill=Y)                               
        mylist = Listbox(main.Frame3_8_1, yscrollcommand = scrollbar.set )        
        mylist.insert(END, u"1.peak shift vs \u03D5")
        mylist.insert(END, u"2.peak shift vs \u03C8")
        mylist.insert(END, u"3.peak shift vs \u03C7")
        mylist.insert(END, u"4.\u03D5,\u03A8 vs \u03B3")
        mylist.pack( side = LEFT, fill = BOTH )
        mylist.bind("<ButtonRelease-1>", lambda event: show_other_info(event,self,stress_calcul,main))
        scrollbar.config( command = mylist.yview )
        
        fig=plt.figure(facecolor="0.94")
        plt.plot(stress_calcul.gamma_section,stress_calcul.psi_calib,'ro',label=u'\u03A8')
        plt.plot(stress_calcul.gamma_section,stress_calcul.phi_calib,'bo',label=u'\u03A6')
        plt.xlabel(r"$\gamma(°)$")
        plt.ylabel("(°)")
        plt.title(u"\u03A6 and \u03A8 in function of \u03B3")
        plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0.,fontsize='x-small')
        plt.subplots_adjust(bottom=0.3)
        plt.close(fig)
        
        canvas = FigureCanvasTkAgg(fig, master=main.Frame3_8_2)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)

    def destroy_widget(self,main):
        for widget in main.Frame3_5_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_3_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_4_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_4_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_4_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_2_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_2_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_2_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_8_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_8_2.winfo_children():
            widget.destroy()

    def destroy_widget_2(self,main):
        for widget in main.Frame3_6_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_2_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_2_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_8_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_8_2.winfo_children():
            widget.destroy()
    #-------------------------------------------------
    def append_zero(self):
        self.peaks_position.append(float('NaN'))
        self.error_peaks_position.append(float('NaN'))
        self.peak_intensity.append(float('NaN'))
        self.error_peak_intensity.append(float('NaN'))
        self.FWHM.append(float('NaN'))
        self.error_FWHM.append(float('NaN'))
        self.data_y_fit_total.append([])
        self.data_y_k1_fit.append([])
        self.data_y_k2_fit.append([])
        self.data_y_fit.append([])
        self.r.append(float('NaN'))
        self.a.append(float('NaN'))
