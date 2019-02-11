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

from fit_function.initial_guess import initial_guess
from fit_function.peak_fit import peak_fit
from residual_stress_1D.stress_calcul_1D import stress_calcul
from residual_stress_1D.angles_modification_1D import angles_modif
from tools.export_graph_1D import export_all_fit_graph, export_all_stress_graph
from tools.export_data_1D import export_all_fit_data, export_all_stress_data
from visualisation.show_XRD_1D import show_fit_graph, show_stress_graph, show_stress_tensor, simulate_stress_phi, show_other_info
from visualisation.pack_Frame import pack_Frame_1D
from visualisation.fig_style import fig_style

class main_calcul:
    def __init__(self,import_XRD,angles_modif,main):
        try:
            self.process(import_XRD,angles_modif,main)
        except Exception as e:
            showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
            return
                
        main.root.mainloop()

    def process(self,import_XRD,angles_modif,main):
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Caculation").pack(side=LEFT)
        self.progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        self.progress.pack(side=LEFT)
        self.progress["value"] = 0
        self.progress["maximum"] = len(import_XRD.phi)+7

        self.check_angles_modif(angles_modif,import_XRD)
        self.check_peak_shift_correction(import_XRD)
        #----------------------------------------
        self.progress["value"] = self.progress["value"]+1
        self.progress.update()
        self.test_interval(import_XRD)
        #----------------------------------------
        self.progress["value"] = self.progress["value"]+1
        self.progress.update()
        self.test_material(import_XRD)
        #----------------------------------------
        self.progress["value"] = self.progress["value"]+1
        self.progress.update()
        self.test_x_ray(import_XRD)
        #----------------------------------------
        if self.interval_valid==True and self.material_valid==True and self.x_ray_valid==True:
            self.destroy_widget(main)
            self.peak_finder(import_XRD,angles_modif,main)
            #-------------------------------------------
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            self.show_fitting_frame(import_XRD,stress_calcul,main)
            #-------------------------------------------
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            stress_calcul.method_sin2psi(stress_calcul,self)
            #-------------------------------------------
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            stress_calcul.method_fundamental(stress_calcul,self)
            #-------------------------------------------
            if stress_calcul.stress_valid>=1:
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.show_stress_graph(stress_calcul,import_XRD,main)
            if stress_calcul.stress_valid>=2:
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.show_stress_tensor(stress_calcul,main)
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            self.show_variation_peak(stress_calcul,main)

            for widget in main.Frame1_2.winfo_children():
                widget.destroy()

            if stress_calcul.stress_valid>=1:
                pack_Frame_1D(main,5)
            else:
                pack_Frame_1D(main,4)
    
    def check_angles_modif(self,angles_modif,import_XRD):
        if import_XRD.angles_modif_valid==True:
            self.phi=angles_modif.phi*1
            self.chi=angles_modif.chi*1
            self.omega=angles_modif.omega*1
            self.twotheta=angles_modif.twotheta*1
            self.data_x=angles_modif.data_x*1
        else:
            self.phi=import_XRD.phi*1
            self.chi=import_XRD.chi*1
            self.omega=import_XRD.omega*1
            self.twotheta=import_XRD.twotheta*1
            self.data_x=import_XRD.data_x*1

    def check_peak_shift_correction(self,import_XRD):
        self.peak_shift_correction_coefficient=import_XRD.peak_shift_correction_coefficient*1
#---------------------------------        
    def test_interval(self,import_XRD):
        self.interval_valid=False
        #test_entry_number
        try:
            twotheta_f=float(import_XRD.Entry_twotheta_from.get())
            twotheta_t=float(import_XRD.Entry_twotheta_to.get())

            background_f=((import_XRD.Entry_background_from.get()).rstrip(',')).split(',')
            background_t=((import_XRD.Entry_background_to.get()).rstrip(',')).split(',')
            for i in range(len(background_f)):
                background_f[i]=float(background_f[i])
                background_t[i]=float(background_t[i])
            self.background_polynominal_degrees=int(import_XRD.Entry_background_polynominal_degrees.get())
        except Exception:
            showinfo(title="Error",message="Please insert all the limit parameters and verify that they are number\nPlease use '.' instead of ',' to insert a number")
            return

        #find index limit           
        twotheta_f_index=(np.abs(np.asarray(self.data_x[0])-twotheta_f)).argmin()
        twotheta_t_index=(np.abs(np.asarray(self.data_x[0])-twotheta_t)).argmin()

        background_f_index=[]
        background_t_index=[]
        for i in range(len(background_f)):
            background_f_index.append((np.abs(np.asarray(self.data_x[0])-background_f[i])).argmin())
            background_t_index.append((np.abs(np.asarray(self.data_x[0])-background_t[i])).argmin())

        self.twotheta_f_index=min(twotheta_f_index,twotheta_t_index)
        self.twotheta_t_index=max(twotheta_f_index,twotheta_t_index)
        self.background_f_index=[]
        self.background_t_index=[]
        for i in range(len(background_f_index)):
            self.background_f_index.append(min(background_f_index[i],background_t_index[i]))
            self.background_t_index.append(max(background_f_index[i],background_t_index[i]))

        #append limit
        data_x_limit=self.data_x[0][self.twotheta_f_index:self.twotheta_t_index]
        if len(data_x_limit)==0:
            showinfo(title="Error",message="Limits out of range")
            return

        #check peaks reference
        self.peaks_position_ref=[]
        self.peaks_limit=[]
        self.peaks_width=[]
        
        try:
            self.peaks_position_ref.append(float(import_XRD.Entry_peak[0].get()))
        except Exception:
            try:
                self.peaks_position_ref.append(float(import_XRD.Entry_twotheta0.get()))
            except Exception:
                return

        try:
            self.peaks_limit.append(float(import_XRD.Entry_limit_peak[0].get()))
        except Exception:
            self.peaks_limit.append(1)

        try:
            self.peaks_width.append(float(import_XRD.Entry_peak_width[0].get()))
        except Exception:
            self.peaks_width.append(1)

        if len(import_XRD.Entry_peak)==2:
            position_ref=((import_XRD.Entry_peak[1].get()).rstrip(',')).split(',')
            for i in range(len(position_ref)):
                try:
                    self.peaks_position_ref.append(float(position_ref[i]))
                except Exception:
                    pass
                
        #find index peaks reference
        for i in range(len(self.peaks_position_ref)):
            index=(np.abs(np.asarray(data_x_limit)-self.peaks_position_ref[i])).argmin()
            if index==0 or index==len(data_x_limit)-1:
                showinfo(title="Error",message="Peak out of limit")
                return

        #find other informations
        if len(import_XRD.Entry_peak)==2:
            limit_peak=((import_XRD.Entry_limit_peak[1].get()).rstrip(',')).split(',')
            peak_width=((import_XRD.Entry_peak_width[1].get()).rstrip(',')).split(',')
            for i in range(1,len(self.peaks_position_ref)):
                try:
                    self.peaks_limit.append(float(limit_peak[i]))
                except Exception:
                    self.peaks_limit.append(1)

                try:
                    self.peaks_width.append(float(peak_width[i]))
                except Exception:
                    self.peaks_width.append(1)

        self.interval_valid=True
#----------------------------------------------------
    def test_material(self,import_XRD):
        #check material
        self.material_valid=False
        try:
            self.twotheta0=float(import_XRD.Entry_twotheta0.get())
        except Exception:
            showinfo(title="Error",message=u"Please check the value of unstressed 2\u03B8")
            return
        else:
            try:
                self.s1=float(import_XRD.Entry_s1.get())
                self.s2_2=float(import_XRD.Entry_half_s2.get())
            except Exception:
                try:
                    Young=float(import_XRD.Entry_Young.get())
                    Poisson=float(import_XRD.Entry_Poisson.get())
                except Exception:
                    showinfo(title="Error",message="Please check the value of (s1,s2/2) or (E,v)")
                    return

                self.s1=-Poisson/Young
                self.s2_2=(Poisson+1)/Young
                self.material_valid=True
            
        self.material_valid=True
#----------------------------------------------------
    def test_x_ray(self,import_XRD):
        self.x_ray_valid=False
        try:
            self.kalpha_1=float(import_XRD.Entry_kalpha[0].get())
            self.kalpha_2=float(import_XRD.Entry_kalpha[1].get())
            self.kalpha_ratio=float(import_XRD.Entry_kalpha[2].get())
        except Exception:
            showinfo(title="Error",message="Please check the value of X-ray propreties")
            return
        self.x_ray_valid=True
    
#--------------------------------------------------
    def destroy_widget(self,main):
        for widget in main.Frame3_4_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_4_2_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_4_2_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_4_3_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_4_3_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_2_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_2_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_2_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_3_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_3_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_2.winfo_children():
            widget.destroy()

    def destroy_widget_2(self,main):
        for widget in main.Frame3_5_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_2_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_2_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_3_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_3_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_2.winfo_children():
            widget.destroy()
#--------------------------------------------------    
    def peak_finder(self,import_XRD,angles_modif,main):
        self.data_y_background_fit=[]
        self.data_y_limit=[]
        self.data_x_limit=[]
        self.data_y_net=[]
        self.data_y_fit=[]
        self.data_y_k1_fit=[]
        self.data_y_k2_fit=[]
        self.data_y_fit_total=[]
        self.peaks_position=[]
        self.error_peaks_position=[]
        self.peak_intensity=[]
        self.error_peak_intensity=[]
        self.FWHM=[]
        self.error_FWHM=[]
        self.a=[]
        self.r=[]
        self.peak_non_valide=[]
        self.peak_rejection=[]

        try:
            r=float(import_XRD.Entry_r.get())
        except Exception:
            r=0

        for i in range(len(import_XRD.phi)):
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            #-------------------------------------------
            try:
                data_y_limit=import_XRD.data_y[i][self.twotheta_f_index:self.twotheta_t_index]
                data_x_limit=self.data_x[i][self.twotheta_f_index:self.twotheta_t_index]       
                self.data_y_limit.append(data_y_limit)
                self.data_x_limit.append(data_x_limit)


                background_data_y_limit=[]
                background_data_x_limit=[]
                for j in range(len(self.background_f_index)):
                    for k in range(self.background_f_index[j],self.background_t_index[j]):
                        background_data_y_limit.append(import_XRD.data_y[i][k])
                        background_data_x_limit.append(self.data_x[i][k])
                background_fit_coefficient=np.polyfit(background_data_x_limit,background_data_y_limit,self.background_polynominal_degrees)
            except Exception:
                self.data_y_background_fit.append([])
                self.data_y_net.append([])
                self.append_zero()
                self.peak_non_valide.append(i+1)
            else:
                data_y_background_fit=[]
                for j in range(len(data_x_limit)):
                    data_y_background_fit_i=0
                    for k in range(self.background_polynominal_degrees+1):
                        data_y_background_fit_i=data_y_background_fit_i+background_fit_coefficient[k]*data_x_limit[j]**(self.background_polynominal_degrees-k)
                    data_y_background_fit.append(data_y_background_fit_i)

                data_y_net=list(np.array(data_y_limit)-np.array(data_y_background_fit))

                self.data_y_background_fit.append(data_y_background_fit)
                self.data_y_net.append(data_y_net)

                init_guess=float(import_XRD.init_guess.get())
                p0_guess=initial_guess(data_y_net,data_x_limit,self.peaks_position_ref,self.peaks_limit,self.peaks_width,init_guess)
                peak_shape=float(import_XRD.peak_shape.get())
                function_fit=import_XRD.function_fit.get()

                peak_fit_result=peak_fit(data_y_net,data_x_limit,self.kalpha_1,self.kalpha_2,self.kalpha_ratio,p0_guess,peak_shape,function_fit)
                    
                if len(peak_fit_result)==0:
                    self.append_zero()
                    self.peak_non_valide.append(i+1)
                else:
                    self.peaks_position.append(peak_fit_result[0][0])
                    self.error_peaks_position.append(peak_fit_result[1][0])
                    self.peak_intensity.append(peak_fit_result[2][0])
                    self.error_peak_intensity.append(peak_fit_result[3][0])
                    self.FWHM.append(peak_fit_result[4][0])
                    self.error_FWHM.append(peak_fit_result[5][0])
                    self.data_y_fit_total.append(peak_fit_result[6])
                    self.data_y_k1_fit.append(peak_fit_result[7])
                    self.data_y_k2_fit.append(peak_fit_result[8])
                    self.r.append(peak_fit_result[9])
                    self.a.append(peak_fit_result[10][0])
                    self.data_y_fit.append(peak_fit_result[11])
                    if self.r[i]<r:
                        self.peak_rejection.append(i+1)

        self.data_x_limit_init=self.data_x_limit*1
        self.peaks_position_init=self.peaks_position*1
        
        self.Entry_peak_non_valide=Entry(main.Frame3_5_2_1,width=100)
        self.Entry_peak_rejection=Entry(main.Frame3_5_2_1,width=100)
        self.Entry_peak_remove=Entry(main.Frame3_5_2_1,width=100)
        for i in range(len(self.peak_non_valide)):
            self.Entry_peak_non_valide.insert(END,str(self.peak_non_valide[i])+",")
        for i in range(len(self.peak_rejection)):
            self.Entry_peak_rejection.insert(END,str(self.peak_rejection[i])+",")
 #--------------------------------------------------
    def show_fitting_frame(self,import_XRD,stress_calcul,main):       
        self.original = IntVar()
        Check_button=Checkbutton(main.Frame3_4_3_2, text="Original intensity", variable=self.original)
        Check_button.grid(row=0,column=0,sticky=W)
        Check_button.select()
        
        self.background = IntVar()
        Check_button=Checkbutton(main.Frame3_4_3_2, text="Background", variable=self.background)
        Check_button.grid(row=1,column=0,sticky=W)
        Check_button.select()
        
        self.net_intensity = IntVar()
        Check_button=Checkbutton(main.Frame3_4_3_2, text="Net intensity", variable=self.net_intensity)
        Check_button.grid(row=2,column=0,sticky=W)
        Check_button.select()
        
        self.I_alpha1 = IntVar()
        Check_button=Checkbutton(main.Frame3_4_3_2, text=u"I (\u03BB\u2081)", variable=self.I_alpha1)
        Check_button.grid(row=3,column=0,sticky=W)
        Check_button.select()
        
        self.I_alpha2 = IntVar()
        Check_button=Checkbutton(main.Frame3_4_3_2, text=u"I (\u03BB\u2082)", variable=self.I_alpha2)
        Check_button.grid(row=4,column=0,sticky=W)
        Check_button.select()
        
        self.I_total = IntVar()
        Check_button=Checkbutton(main.Frame3_4_3_2, text="I fit total", variable=self.I_total)
        Check_button.grid(row=5,column=0,sticky=W)
        Check_button.select()
       
        scrollbar = Scrollbar(main.Frame3_4_1)
        scrollbar.pack( side = RIGHT, fill=Y)
        mylist = Listbox(main.Frame3_4_1, yscrollcommand = scrollbar.set)
        for i in range(len(self.phi)):
            mylist.insert(END, str(i+1)+u".\u03C6="+str(float(self.phi[i]))+u"; \u03C7="+str(float(self.chi[i]))+u"; \u03C9="+str(float(self.omega[i])))
        mylist.pack( side = LEFT, fill = BOTH,expand=YES)
        mylist.bind("<ButtonRelease-1>", lambda event: show_fit_graph(event,self,stress_calcul,main))
        scrollbar.config( command = mylist.yview )

        for i in range(len(self.phi)):
            if str(i+1) in self.peak_non_valide or str(i+1) in self.peak_rejection:
                continue
            fig=plt.figure(facecolor="0.94")
            plt.xlabel(r"$2\theta$")
            plt.ylabel("Intensity")
            plt.title(u"\u03C6="+str(float(self.phi[i]))+u"; \u03C7="+str(float(self.chi[i])))
            plt.plot(self.data_x_limit[i],self.data_y_limit[i],'ro',markersize=2,label='Original intensity')
            plt.plot(self.data_x_limit[i],self.data_y_background_fit[i],'k',label='Background')
            plt.plot(self.data_x_limit[i],self.data_y_net[i],'go',markersize=2,label='Net intensity')
            x=[self.peaks_position[i],self.peaks_position[i]]
            y=[min(self.data_y_net[i]),max(self.data_y_limit[i])]        
            plt.plot(self.data_x_limit[i],self.data_y_k1_fit[i],'b',label=r"I($\lambda_{1}$)")
            plt.plot(self.data_x_limit[i],self.data_y_k2_fit[i],'c',label=r"I($\lambda_{2}$)")
            plt.plot(self.data_x_limit[i],self.data_y_fit_total[i],'m',label=r"I($\lambda_{1}$)"+r" + I($\lambda_{2}$)")
            plt.plot(x,y,'b--',label=r"peak 2$\theta_{1}$ = "+str('%0.2f' % self.peaks_position[i])+"°")      
            plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0.)
            plt.subplots_adjust(bottom=0.3)
            plt.close()
            
            canvas = FigureCanvasTkAgg(fig, master=main.Frame3_4_2_1)
            canvas.get_tk_widget().pack(fill=BOTH,expand=YES)
            break

        Button(main.Frame3_4_3_1, text = 'Export all as image',bg="white", command = lambda: export_all_fit_graph(self,main)).pack(side=TOP,padx=10, pady=10)
        Button(main.Frame3_4_3_1, text = 'Export all as text',bg="white", command = lambda: export_all_fit_data(self,main)).pack(side=TOP,padx=10, pady=10)

        fig_style(self,main.Frame3_4_3_3)

    #---------------------------------
    def modification_stress(self,import_XRD,angles_modif,main):
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()
 
        Label(main.Frame1_2,text="Caculation").pack(side=LEFT)
        self.progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        self.progress.pack(side=LEFT)
        self.progress["value"] = 0
        self.progress["maximum"] = len(import_XRD.phi)+7

        self.check_angles_modif(angles_modif,import_XRD)
        self.check_peak_shift_correction(import_XRD)
        #----------------------------------------
        self.progress["value"] = self.progress["value"]+1
        self.progress.update()
        self.test_interval(import_XRD)
        #----------------------------------------
        self.progress["value"] = self.progress["value"]+1
        self.progress.update()
        self.test_material(import_XRD)
        #----------------------------------------
        self.progress["value"] = self.progress["value"]+1
        self.progress.update()
        self.test_x_ray(import_XRD)
        #----------------------------------------
        if self.interval_valid==True and self.material_valid==True and self.x_ray_valid==True:
            self.destroy_widget_2(main)
            #-------------------------------------------
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            stress_calcul.method_sin2psi(stress_calcul,self)
            #-------------------------------------------
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            stress_calcul.method_fundamental(stress_calcul,self)
            #-------------------------------------------
            if stress_calcul.stress_valid>=1:
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.show_stress_graph(stress_calcul,import_XRD,main)
            if stress_calcul.stress_valid>=2:
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.show_stress_tensor(stress_calcul,main)
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()
            self.show_variation_peak(stress_calcul,main)

            for widget in main.Frame1_2.winfo_children():
                widget.destroy()

            if stress_calcul.stress_valid>=1:
                pack_Frame_1D(main,5)
            else:
                pack_Frame_1D(main,4)

        main.root.mainloop()
    #-----------------------------------------------------
    def show_stress_graph(self,stress_calcul,import_XRD,main):      
        self.experimental = IntVar()
        Check_button=Checkbutton(main.Frame3_5_3_2, text="Experimental", variable=self.experimental)
        Check_button.grid(row=0,column=0,sticky=W)
        Check_button.select()

        self.annotate = IntVar()
        Check_button=Checkbutton(main.Frame3_5_3_2, text="Annotate", variable=self.annotate)
        Check_button.grid(row=1,column=0,sticky=W)
        Check_button.select()

        if stress_calcul.stress_valid>=1:
            self.sin2khi_method = IntVar()
            Check_button=Checkbutton(main.Frame3_5_3_2, text=u'Sin\u00B2\u03A8 method', variable=self.sin2khi_method)
            Check_button.grid(row=2,column=0,sticky=W)
            Check_button.select()

            self.fundamental_method = IntVar()
            Check_button=Checkbutton(main.Frame3_5_3_2, text="Fundamental method", variable=self.fundamental_method)
            Check_button.grid(row=3,column=0,sticky=W)
            Check_button.select()
        
        #--Frame3_5-----------------------------------------------------    
        scrollbar = Scrollbar(main.Frame3_5_1)
        scrollbar.pack( side = RIGHT, fill=Y)                               
        mylist = Listbox(main.Frame3_5_1, yscrollcommand = scrollbar.set )
        for i in range(len(stress_calcul.liste_phi)):
            mylist.insert(END, str(i+1)+u".\u03D5="+str(float(stress_calcul.liste_phi[i])))
        mylist.pack( side = LEFT, fill = BOTH )
        mylist.bind("<ButtonRelease-1>", lambda event: show_stress_graph(event,self,stress_calcul,main))
        scrollbar.config( command = mylist.yview )

        Label(main.Frame3_5_2_1, text="(Peak number)(1,2,3,...)").grid(row=0,column=1,sticky=W)
        Label(main.Frame3_5_2_1, text="Graph non valide").grid(row=1,column=0,sticky=W)
        self.Entry_peak_non_valide.grid(row=1,column=1,sticky=W)
        self.Entry_peak_non_valide.config(state='disabled')
        Label(main.Frame3_5_2_1, text="Peak rejection").grid(row=2,column=0,sticky=W)
        self.Entry_peak_rejection.grid(row=2,column=1,sticky=W)
        self.Entry_peak_rejection.config(state='disabled')
        Label(main.Frame3_5_2_1, text="Remove peaks",bg="white").grid(row=3,column=0,sticky=W)
        self.Entry_peak_remove.grid(row=3,column=1,sticky=W)
        Button(main.Frame3_5_2_1,compound=CENTER, text="APPLY MODIFICATION",bg="white",command=lambda:self.modification_stress(import_XRD,angles_modif,main)).grid(row=4,column=1,sticky=W)

        Label(main.Frame3_5_2_2, text="Stress behaviour").grid(row=0,column=0,sticky=W)
        self.stress_behaviour = IntVar()
        Radiobutton(main.Frame3_5_2_2, text="No Shear", variable=self.stress_behaviour, value=1).grid(row=1,column=0,sticky=W)
        Radiobutton(main.Frame3_5_2_2, text="Shear", variable=self.stress_behaviour, value=2).grid(row=2,column=0,sticky=W)
        self.stress_behaviour.set(1)

        self.stress_dimension = IntVar()
        self.stress_dimension.set(2)
        if len(stress_calcul.liste_phi)>=3:
            Label(main.Frame3_5_2_2, text="Stress dimension").grid(row=0,column=1,sticky=W)
            Radiobutton(main.Frame3_5_2_2, text="Biaxial", variable=self.stress_dimension, value=2).grid(row=1,column=1,sticky=W)
            Radiobutton(main.Frame3_5_2_2, text="Triaxial", variable=self.stress_dimension, value=3).grid(row=2,column=1,sticky=W)
        
        Frame_a=Frame(main.Frame3_5_2_3)
        Frame_a.pack(fill=BOTH, expand=YES)
        Frame_b=Frame(main.Frame3_5_2_3)
        Frame_b.pack(fill=BOTH, expand=YES)

        if stress_calcul.stress_valid>=1:
            Label(Frame_a,text=u'STRESS AT \u03D5='+str(stress_calcul.liste_phi[0])).grid(row=0,column=0,sticky=W)
            Label(Frame_a,text="Unit: MPa").grid(row=0,column=1,sticky=W)
            Label(Frame_a,text=u'Sin\u00B2\u03A8 method').grid(row=1,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_linear[0])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_linear[0])).grid(row=2,column=0,sticky=W)
               
        if len(stress_calcul.liste_phi)>=1:
            Label(Frame_a,text=u'   Fundamental method').grid(row=1,column=2,sticky=W)
            if stress_calcul.length_strain>=3:
                Label(Frame_a,text=u'   \u03C3\u03D5= '+str('%0.1f' % stress_calcul.sigma_phi_biaxial[0])+u"\u00B1"+str('%0.1f' % stress_calcul.error_sigma_phi_biaxial[0])).grid(row=2,column=2,sticky=W)
            
        fig=plt.figure(facecolor="0.94")
        ax = fig.add_subplot(111)  
        plt.plot(stress_calcul.sinpsi_2[0],stress_calcul.strain[0],'ro',label='Experimental')
        for j in range(len(stress_calcul.psi[0])):
            plt.annotate(str(stress_calcul.index_psi[0][j]),xy=(stress_calcul.sinpsi_2[0][j],stress_calcul.strain[0][j]))

        if stress_calcul.stress_valid>=1:
            plt.plot(stress_calcul.sinpsi_2_sorted[0],stress_calcul.strain_linear_fit[0],'b',label=u'Sin\u00B2\u03A8 method')
                
        if len(stress_calcul.liste_phi)>=1:
            if stress_calcul.length_strain>=3:
                plt.plot(stress_calcul.sinpsi_2_sorted[0],stress_calcul.strain_biaxial[0],'m',label='Fundamental method')
                
        plt.xlabel(r"$sin^{2}\psi$")
        plt.ylabel('Elastic strain '+r"$\varepsilon$")
        plt.title(u"\u03D5="+str(stress_calcul.liste_phi[0]))
        plt.legend(loc='upper left', bbox_to_anchor=(0.0, -0.3, 1, 0),ncol=3,mode="expand",borderaxespad=0.)
        plt.subplots_adjust(bottom=0.4)
        plt.subplots_adjust(left=0.2)
        plt.close()
                             
        canvas = FigureCanvasTkAgg(fig, master=Frame_b)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        fig_style(stress_calcul,main.Frame3_5_3_3)

        Button(main.Frame3_5_3_1, text = 'Export all as image',bg="white", command = lambda: export_all_stress_graph(self,stress_calcul,main)).pack(side=TOP,padx=10, pady=10)
        Button(main.Frame3_5_3_1, text = 'Export all as text',bg="white", command = lambda:export_all_stress_data(self,stress_calcul,main)).pack(side=TOP,padx=10, pady=10)      

    def show_stress_tensor(self,stress_calcul,main):
        self.selection="Biaxial"
        scrollbar = Scrollbar(main.Frame3_6_1)
        scrollbar.pack( side = RIGHT, fill=Y)                               
        mylist = Listbox(main.Frame3_6_1, yscrollcommand = scrollbar.set )
        if stress_calcul.length_strain>=3:
            mylist.insert(END, "Biaxial")
        if stress_calcul.length_strain>=5:
            mylist.insert(END, "Biaxial+shear")
        if stress_calcul.length_strain>=6:
            mylist.insert(END, "Triaxial")
        mylist.pack( side = LEFT, fill = BOTH )
        mylist.bind("<ButtonRelease-1>", lambda event: show_stress_tensor(event,stress_calcul,main))
        scrollbar.config( command = mylist.yview )
        #------------------------------------
        Frame_a=Frame(main.Frame3_6_2)
        Frame_a.pack(fill=BOTH, expand=YES)
        Frame_b=Frame(main.Frame3_6_2)
        Frame_b.pack(fill=BOTH, expand=YES)
        
        Label(Frame_a,text="STRESS TENSOR - Biaxial").grid(row=0,column=0,sticky=W)
        Label(Frame_a,text="Unit: MPa").grid(row=0,column=2,sticky=W)
        Label(Frame_a,text=u'Sin\u00B2\u03A8 method').grid(row=1,column=0,sticky=W)
        if stress_calcul.stress_valid>=2:
            Label(Frame_a,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_1[1][0,0]))).grid(row=2,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_1[1][1,1]))).grid(row=2,column=1,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_1[1][1,1]))).grid(row=3,column=0,sticky=W)
            Label(Frame_a,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial_1[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial_1[1][2,2]))).grid(row=3,column=1,sticky=W)

            fig=plt.figure(facecolor="0.94")
            theta=np.arange(0,np.radians(361),np.radians(5))
            ax = fig.add_subplot(111, polar=True)
            plt.title("Simulation stress-phi")
            ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial_1))
            ax.set_yticks([min(np.negative(stress_calcul.all_sigma_phi_biaxial_1)),max(np.negative(stress_calcul.all_sigma_phi_biaxial_1))])
            ax.set_yticklabels([str('%0.1f' % min(stress_calcul.all_sigma_phi_biaxial_1))+'MPa',str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial_1))+'MPa'])
            plt.close(fig)
                                     
            canvas = FigureCanvasTkAgg(fig, master=Frame_b)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)
        #------------------------------------------------------
        if len(stress_calcul.liste_phi)>=2:
            Frame_c=Frame(main.Frame3_6_3)
            Frame_c.pack(fill=BOTH, expand=YES)
            Frame_d=Frame(main.Frame3_6_3)
            Frame_d.pack(fill=BOTH, expand=YES)
            
            Label(Frame_c,text="").grid(row=0,column=0,sticky=W)
            Label(Frame_c,text="Fundamental method").grid(row=1,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][0])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][0,0]))).grid(row=2,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2081\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][1,1]))).grid(row=2,column=1,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2081= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][1])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][1,1]))).grid(row=3,column=0,sticky=W)
            Label(Frame_c,text=u'\u03C3\u2082\u2082= '+str('%0.1f' % stress_calcul.tensor_biaxial[0][2])+u"\u00B1"+str('%0.1f' % np.sqrt(stress_calcul.tensor_biaxial[1][2,2]))).grid(row=3,column=1,sticky=W)
            
            fig=plt.figure(facecolor="0.94")
            plt.title("Simulation stress-phi")
            theta=np.arange(0,np.radians(361),np.radians(5))
            ax = fig.add_subplot(111, polar=True)
            ax.plot(theta,np.negative(stress_calcul.all_sigma_phi_biaxial))
            ax.set_yticks([min(np.negative(stress_calcul.all_sigma_phi_biaxial)),max(np.negative(stress_calcul.all_sigma_phi_biaxial))])
            ax.set_yticklabels([str('%0.1f' % min(stress_calcul.all_sigma_phi_biaxial))+'MPa',str('%0.1f' % max(stress_calcul.all_sigma_phi_biaxial))+'MPa'])
            plt.close(fig)
                                     
            canvas = FigureCanvasTkAgg(fig, master=Frame_d)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)

    def show_variation_peak(self,stress_calcul,main):
        scrollbar = Scrollbar(main.Frame3_7_1)
        scrollbar.pack( side = RIGHT, fill=Y)                               
        mylist = Listbox(main.Frame3_7_1, yscrollcommand = scrollbar.set )
        mylist.insert(END, u"1.peak shift - \u03D5")
        mylist.insert(END, u"2.peak shift - \u03C8")
        mylist.pack( side = LEFT, fill = BOTH )
        mylist.bind("<ButtonRelease-1>", lambda event: show_other_info(event,self,stress_calcul,main))
        scrollbar.config( command = mylist.yview )
        
        fig=plt.figure(facecolor="0.94")
        plt.plot(stress_calcul.psi_calib,stress_calcul.peak_shift,'ro',label='peak shift')
        plt.xlabel(u"\u03C8(°)")
        plt.ylabel("peak shift(%)")
        plt.title("Variation of peak shift")
        plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0.,fontsize='x-small')
        plt.subplots_adjust(bottom=0.3)
        plt.close(fig)
        
        canvas = FigureCanvasTkAgg(fig, master=main.Frame3_7_2)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)

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
