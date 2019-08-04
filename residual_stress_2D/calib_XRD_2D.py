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
from tkinter import font
from tkinter.messagebox import *
from tkinter.ttk import Progressbar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
import numpy as np
import traceback

from residual_stress_2D.angles_modification_2D import angles_modif
from residual_stress_2D.main_calcul_2D import main_calcul
from residual_stress_2D.stress_calcul_2D import stress_calcul
from visualisation.show_XRD_2D import show_calib_image
from visualisation.preview_2D import limit_preview, fit_preview
from tools.calcul_parameters import export_calcul_parameters, import_calcul_parameters
from read_file.import_material import import_material
from tools.peak_shift_correction import import_peak_shift_correction
from tools.add_peak import add_peak, delete_peak
from visualisation.pack_Frame import pack_Frame_2D

def calib_pyFai(self,intensity_2D,nrow,ncol,center_row,center_col,twotheta_center):  
    try:
        #read PONI parameters
        calib=AzimuthalIntegrator()
        calib.pixel1=float(self.Entry_pixel_1.get())
        calib.pixel2=float(self.Entry_pixel_2.get())
        calib.dist = float(self.Entry_distance_calib.get())
        calib.poni1 = float(self.Entry_poni_1.get())
        calib.poni2 = float(self.Entry_poni_2.get())
        calib.rot1 = float(self.Entry_rot_1.get())
        calib.rot2 = float(self.Entry_rot_2.get())
        calib.rot3 = float(self.Entry_rot_3.get())
        calib.wavelength = float(self.Entry_wl_calib.get())
        theta_direction=self.direction_2theta.get()
    except Exception as e:
        showinfo(title="Error",message="Wrong PONI parameters:"+str(e))
        return
    else:
        if theta_direction==1:
            intensity_2D_calib, twotheta_x, gamma_y = calib.integrate2d( np.asarray(intensity_2D) , ncol, nrow, unit="2th_deg") #pyFAI calib
            
            gamma_y=np.asarray(gamma_y)-gamma_y[int(nrow/2)] #gamma direction
            if gamma_y[0]>gamma_y[len(gamma_y)-1]:
                gamma_y=np.flip(gamma_y,axis=0)
            #if np.isnan(twotheta_center)==False:
               #twotheta_x=np.asarray(twotheta_x)+twotheta_center-twotheta_x[int(center_col)] #2theta direction
            #else:
            twotheta_x=np.asarray(twotheta_x)

        else:
            intensity_2D_calib, twotheta_x, gamma_y = calib.integrate2d( np.asarray(intensity_2D) , nrow, ncol, unit="2th_deg") #pyFAI calib
            
            gamma_y=np.asarray(gamma_y)-gamma_y[int(ncol/2)] #gamma direction
            if gamma_y[0]>gamma_y[len(gamma_y)-1]:
                gamma_y=np.flip(gamma_y,axis=0)
            #if np.isnan(twotheta_center)==False:
                #twotheta_x=np.asarray(twotheta_x)+twotheta_center-twotheta_x[int(center_row)] #2theta direction
            #else:
            twotheta_x=np.asarray(twotheta_x)

            
        return(intensity_2D_calib,twotheta_x,gamma_y)
    
#-------------------------------------
class calib_2D:
    def __init__(self,import_XRD,main):
        try:
            self.process(import_XRD,main)
        except Exception as e:
            showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
            return
        main.root.mainloop()
        
    def process(self,import_XRD,main):
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Calibration").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress_indice=0
        progress_max=0
        progress["value"] = 0
        progress_max = 5
        progress["maximum"] = 5

        progress_indice=progress_indice+1
        progress["value"] = progress_indice
        progress.update()

        self.run_calib(import_XRD)
        if len(self.calib)>0:
            progress_indice=progress_indice+1
            progress["value"] = progress_indice
            progress.update()
            self.destroy_widget(main) #reset all Frame (see list in function)
            self.graphic_frame3_2(import_XRD,angles_modif,main_calcul,main) #Frame Calib XRD graphic
            #--------------------
            progress_indice=progress_indice+1
            progress["value"] = progress_indice
            progress.update()
            self.attribute_graphic_Frame3_3(import_XRD,angles_modif,main_calcul,main) #Frame Angles modif graphic
            #---------------------
            progress_indice=progress_indice+1
            progress["value"] = progress_indice
            progress.update()
            self.attribute_graphic_Frame3_4(import_XRD,angles_modif,main_calcul,main) #Frame STRESS PARAMETERS graphic
            #---------------------
            progress_indice=progress_indice+1
            progress["value"] = progress_indice
            progress.update()
            self.graphic_Frame3_5(import_XRD,angles_modif,main_calcul,main) #Frame FIT RESULTS graphic

        self.nimage=0

        for widget in main.Frame1_2.winfo_children():
            widget.destroy()

    def run_calib(self,import_XRD): #run calib fonction
        #take phi, chi, omega, twotheta value in calib class
        self.phi=import_XRD.phi*1
        self.chi=import_XRD.chi*1
        self.omega=import_XRD.omega*1
        self.twotheta_center=import_XRD.twotheta_center*1

        #check image rotation and flip
        twotheta_center=import_XRD.twotheta_center[0]
        rotate=import_XRD.rotate
        flip=import_XRD.flip
        
        if rotate==0:
            intensity_2D=import_XRD.intensity_2D
            nrow=import_XRD.nrow[0]
            ncol=import_XRD.ncol[0]
            center_row=import_XRD.center_row[0]
            center_col=import_XRD.center_col[0]
        
        if rotate==90:
            intensity_2D=np.rot90(import_XRD.intensity_2D,k=1,axes=(0, 1))
            nrow=import_XRD.ncol[0]
            ncol=import_XRD.nrow[0]
            center_row=import_XRD.center_col[0]
            center_col=import_XRD.center_row[0]
                            
        if rotate==180: 
            intensity_2D=np.rot90(import_XRD.intensity_2D,k=2,axes=(0, 1))
            nrow=import_XRD.nrow[0]
            ncol=import_XRD.ncol[0]
            center_row=import_XRD.center_row[0]
            center_col=import_XRD.center_col[0]
                                
        if rotate==270:
            intensity_2D=np.rot90(import_XRD.intensity_2D,k=3,axes=(0, 1))
            nrow=import_XRD.ncol[0]
            ncol=import_XRD.nrow[0]
            center_row=import_XRD.center_col[0]
            center_col=import_XRD.center_row[0]

        if flip==1:
            intensity_2D=np.flip(intensity_2D,axis=0)

        if flip==2:
            intensity_2D=np.flip(intensity_2D,axis=1)
            
        self.calib=calib_pyFai(import_XRD,intensity_2D,nrow,ncol,center_row,center_col,twotheta_center) #run calib pyFAI
        if len(self.calib)>0: #calib pyFAI valide => take results
            self.intensity_2D_calib=self.calib[0] #image data after pyFAI calib
            self.twotheta_x=self.calib[1] #2theta values
            self.gamma_y=self.calib[2] #gamma values
            self.nrow=len(self.gamma_y) #gamma points
            self.ncol=len(self.twotheta_x) #2theta points
            if np.isnan(self.twotheta_center[0])==True: #check if two theta center existe
                for i in range(len(self.twotheta_center)):
                    self.twotheta_center[i]=self.twotheta_x[int(len(self.twotheta_x)/2)]
                

    def destroy_widget(self,main):
        for widget in main.Frame3_2_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_2_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_2_4.winfo_children():
            widget.destroy()
        for widget in main.Frame3_3_1.winfo_children():
            widget.destroy()
        #for widget in main.Frame3_3_2_1.winfo_children():
            #widget.destroy()
        #for widget in main.Frame3_3_2_2.winfo_children():
            #widget.destroy()
        for widget in main.Frame3_3_3.winfo_children():
            widget.destroy()
        #for widget in main.Frame3_4_1.winfo_children():
            #widget.destroy()
        #for widget in main.Frame3_4_2.winfo_children():
            #widget.destroy()
        #for widget in main.Frame3_4_3.winfo_children():
            #widget.destroy()
        for widget in main.Frame3_4_4_1_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_4_4_1_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_4_4_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_3_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_3_2.winfo_children():
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

        
    def graphic_frame3_2(self,import_XRD,angles_modif,main_calcul,main): #Frame Calib XRD
        #image legend setting
        Label(main.Frame3_2_4, text="Image legend",bg="white").grid(row=0,column=0)
        Label(main.Frame3_2_4, text="from").grid(row=1,column=0)
        self.Entry_legend_from_3_2 = Entry(main.Frame3_2_4,width=6)
        self.Entry_legend_from_3_2.grid(row=2,column=0)
        self.Entry_legend_from_3_2.insert(0,0)
        
        Label(main.Frame3_2_4, text="to").grid(row=3,column=0)
        self.Entry_legend_to_3_2 = Entry(main.Frame3_2_4,width=6)
        self.Entry_legend_to_3_2.grid(row=4,column=0)
        self.Entry_legend_to_3_2.insert(0,max(map(max, self.intensity_2D_calib)))

        #color setting
        self.cmap_var_3_2=StringVar()
        Radiobutton(main.Frame3_2_4, text="hot", variable=self.cmap_var_3_2, value="hot").grid(row=5,column=0,sticky=W)
        Radiobutton(main.Frame3_2_4, text="cool", variable=self.cmap_var_3_2, value="GnBu").grid(row=6,column=0,sticky=W)
        Radiobutton(main.Frame3_2_4, text="gray", variable=self.cmap_var_3_2, value="gray").grid(row=7,column=0,sticky=W)
        Radiobutton(main.Frame3_2_4, text="nipy", variable=self.cmap_var_3_2, value="nipy_spectral").grid(row=8,column=0,sticky=W)
        self.cmap_var_3_2.set("hot")

        #images list
        scrollbar = Scrollbar(main.Frame3_2_2)
        scrollbar.pack(side = RIGHT, fill=Y) 
        mylist= Listbox(main.Frame3_2_2, yscrollcommand = scrollbar.set)
        mylist.pack(side = LEFT, fill = BOTH,expand=YES)
        for i in range(len(self.phi)):
            mylist.insert(END, str(i+1)+u'.\u03C6='+str(self.phi[i])+" ; "+u'\u03C7='+str(self.chi[i])+u"; \u03C9="+str(self.omega[i])+
                          ' (.'+str(import_XRD.nfile[i]+1)+'.'+str(import_XRD.nimage_i[i]+1)+'.)')
        mylist.bind("<ButtonRelease-1>", lambda event: show_calib_image(event,angles_modif,self,import_XRD,main_calcul,stress_calcul,main.Frame3_2_3,main))
        scrollbar.config(command = mylist.yview)
                 
        fig=plt.figure(1,facecolor="0.94")
        plt.imshow(self.intensity_2D_calib, cmap="hot",origin='lower')
        plt.title(u'\u03C6='+str(float(self.phi[0]))+
                  u'; \u03C7='+str(float(self.chi[0]))+
                  u'; \u03C9='+str(float(self.omega[0])))
        plt.yticks((1,self.nrow*0.25,self.nrow*0.5,self.nrow*0.75,self.nrow), (str("%0.1f" %self.gamma_y[0]),str("%0.1f" %self.gamma_y[int(self.nrow*0.25)]),str("%0.1f" %self.gamma_y[int(self.nrow*0.5)]),str("%0.1f" %self.gamma_y[int(self.nrow*0.75)]),str("%0.1f" %self.gamma_y[int(self.nrow-1)])))
        plt.xticks((1,self.ncol*0.25,self.ncol*0.5,self.ncol*0.75,self.ncol), (str("%0.1f" %self.twotheta_x[0]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.25)]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.5)]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.75)]),str("%0.1f" %self.twotheta_x[int(self.ncol-1)])))
        plt.xlabel(r"$2\theta(°)$")
        plt.ylabel(r"$\gamma(°)$")
        plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
        plt.close()

        canvas = FigureCanvasTkAgg(fig, main.Frame3_2_3)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES,ipadx=20)

    def graphic_Frame3_3(self,import_XRD,angles_modif,main_calcul,main): #Frame ANGLES MODIFICATION
        Label(main.Frame3_3_2_1, text="ANGLES MODIFICATION (optinal)", bg="white").grid(row=0,column=0,sticky=W)
        Label(main.Frame3_3_2_1, text=u"PHI \u03C6").grid(row=1,column=0,sticky=W)
        Label(main.Frame3_3_2_1, text="offset (°)").grid(row=1,column=1,sticky=W)

        Label(main.Frame3_3_2_1, text=u"CHI \u03C7").grid(row=2,column=0,sticky=W)
        Label(main.Frame3_3_2_1, text="offset (°)").grid(row=2,column=1,sticky=W)

        Label(main.Frame3_3_2_1, text=u"2 THETA 2\u03B8").grid(row=3,column=0,sticky=W)
        Label(main.Frame3_3_2_1, text="offset (°)").grid(row=3,column=1,sticky=W)

        Label(main.Frame3_3_2_1, text=u"OMEGA \u03C9").grid(row=4,column=0,sticky=W)
        Label(main.Frame3_3_2_1, text="offset (°)").grid(row=4,column=1,sticky=W) 

        Label(main.Frame3_3_2_1, text=u"GAMMA \u03B3").grid(row=5,column=0,sticky=W)
        Label(main.Frame3_3_2_1, text="offset (°)").grid(row=5,column=1,sticky=W)
           
        self.Entry_phi_offset= Entry(main.Frame3_3_2_1)
        self.Entry_phi_offset.grid(row=1, column=2,sticky=W)
            
        self.Entry_chi_offset= Entry(main.Frame3_3_2_1)
        self.Entry_chi_offset.grid(row=2, column=2,sticky=W)

        self.Entry_twotheta_offset=Entry(main.Frame3_3_2_1)
        self.Entry_twotheta_offset.grid(row=3, column=2,sticky=W)

        self.Entry_omega_offset=Entry(main.Frame3_3_2_1)
        self.Entry_omega_offset.grid(row=4, column=2,sticky=W)
                   
        self.Entry_gamma_offset= Entry(main.Frame3_3_2_1)
        self.Entry_gamma_offset.grid(row=5, column=2,sticky=W)
                  
        self.Check_phi_invert = IntVar()
        Checkbutton(main.Frame3_3_2_1, text="Invert", variable=self.Check_phi_invert).grid(row=1,column=3,sticky=W)

        self.Check_chi_invert = IntVar()
        Checkbutton(main.Frame3_3_2_1, text="Invert", variable=self.Check_chi_invert).grid(row=2,column=3,sticky=W)

        self.Check_twotheta_flip = IntVar()
        Checkbutton(main.Frame3_3_2_1, text="Flip", variable=self.Check_twotheta_flip).grid(row=3,column=3,sticky=W)

        self.Check_gamma_invert = IntVar()
        Checkbutton(main.Frame3_3_2_1, text="Invert", variable=self.Check_gamma_invert).grid(row=5,column=3,sticky=W)

        self.Check_gamma_flip = IntVar()
        Checkbutton(main.Frame3_3_2_1, text="Flip", variable=self.Check_gamma_flip).grid(row=5,column=4,sticky=W)   
            
        self.Entry_phi_offset.delete(0,END)
        self.Entry_chi_offset.delete(0,END)
        self.Entry_twotheta_offset.delete(0,END)
        self.Entry_omega_offset.delete(0,END)
        self.Entry_gamma_offset.delete(0,END)
        self.Entry_phi_offset.insert(0,"0")
        self.Entry_chi_offset.insert(0,"0")
        self.Entry_twotheta_offset.insert(0,"0")
        self.Entry_omega_offset.insert(0,"0")
        self.Entry_gamma_offset.insert(0,"0")
            
        self.angles_modif_valid=False

        #reset all button in Frame
        self.button_apply=Button(main.Frame3_3_2_1,compound=CENTER, text="Apply",bg="white",command=lambda:None)
        self.button_apply.grid(row=7, column=0,sticky=W)
        self.button_init=Button(main.Frame3_3_2_1,compound=CENTER, text="Initialize",bg="white",command=lambda:None) 
        self.button_init.grid(row=8, column=0,sticky=W)
        self.button_advance=Button(main.Frame3_3_2_1,compound=CENTER, text="Advance",bg="white",command=lambda:None)
        self.button_advance.grid(row=9,column=0,sticky=W)
        
        fig=plt.figure(1,facecolor="0.94")
        canvas = FigureCanvasTkAgg(fig, main.Frame3_3_3)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES,ipadx=50)

    def attribute_graphic_Frame3_3(self,import_XRD,angles_modif,main_calcul,main):
        scrollbar = Scrollbar(main.Frame3_3_1)
        scrollbar.pack( side = RIGHT, fill=Y) 
        mylist = Listbox(main.Frame3_3_1, yscrollcommand = scrollbar.set)
        mylist.pack(side = LEFT, fill = BOTH,expand=YES)
        for i in range(len(self.phi)):
            mylist.insert(END, str(i+1)+u'.\u03C6='+str(self.phi[i])+" ; "+u'\u03C7='+str(self.chi[i])+u"; \u03C9="+str(self.omega[i]))
        mylist.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command = mylist.yview )
            
        #self.angles_modif_valid=False

        #attribute function to buttons
        self.button_apply.config(command=lambda:angles_modif.apply(angles_modif,self,import_XRD,main_calcul,stress_calcul,main))
        self.button_init.config(command=lambda:angles_modif.init(angles_modif,self,import_XRD,main_calcul,stress_calcul,main))
        self.button_advance.config(command=lambda:angles_modif.advance(angles_modif,self,import_XRD,main_calcul,stress_calcul,main))
        
        fig=plt.figure(1,facecolor="0.94")
        plt.imshow(self.intensity_2D_calib, cmap="hot",origin='lower')
        plt.yticks((1,self.nrow*0.25,self.nrow*0.5,self.nrow*0.75,self.nrow), (str("%0.1f" %self.gamma_y[0]),str("%0.1f" %self.gamma_y[int(self.nrow*0.25)]),str("%0.1f" %self.gamma_y[int(self.nrow*0.5)]),str("%0.1f" %self.gamma_y[int(self.nrow*0.75)]),str("%0.1f" %self.gamma_y[int(self.nrow-1)])))
        plt.xticks((1,self.ncol*0.25,self.ncol*0.5,self.ncol*0.75,self.ncol), (str("%0.1f" %self.twotheta_x[0]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.25)]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.5)]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.75)]),str("%0.1f" %self.twotheta_x[int(self.ncol-1)])))
        plt.xlabel(r"$2\theta(°)$")
        plt.ylabel(r"$\gamma(°)$")
        plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
        plt.close()
            
        canvas = FigureCanvasTkAgg(fig, main.Frame3_3_3)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES,ipadx=50)

        try:
            angles_modif.Button_import_gma.config(command=lambda:angles_modif.import_goniometric_angles(angles_modif,self,import_XRD,main_calcul,stress_calcul,main))
            angles_modif.Button_next.config(command=lambda:angles_modif.next_step(angles_modif,self,import_XRD,main_calcul,stress_calcul,main))
            if angles_modif.gonio_config.get()==1:
                angles_modif.Button_apply_gma.config(command=lambda:angles_modif.apply_advance_1(angles_modif,self,import_XRD,main_calcul,stress_calcul,main))
            elif angles_modif.gonio_config.get()==2:
                angles_modif.Button_apply_gma.config(command=lambda:angles_modif.apply_advance_2(angles_modif,self,import_XRD,main_calcul,stress_calcul,main))
        except Exception:
            pass
        
        
    def graphic_Frame3_4(self,import_XRD,angles_modif,main_calcul,main):   #"STRESS PARAMETERS" frame
        f=font.Font(size=9,underline=1)
        
        i=0
        Label(main.Frame3_4_1, text="BACKGROUND",bg="white").grid(row=i,column=0,sticky=W)
        Label(main.Frame3_4_1, text=u"2\u03B8 from(°)").grid(row=i,column=1,sticky=W)
        Label(main.Frame3_4_1, text=u"2\u03B8 to(°)").grid(row=i,column=2,sticky=W)

        Label(main.Frame3_4_1, text="range 1,2,...").grid(row=i+1,column=0,sticky=W)
        self.Entry_background_from=Entry(main.Frame3_4_1,width=10)
        self.Entry_background_from.grid(row=i+1,column=1,sticky=W)
        #self.Entry_background_from.delete(0,END)
        #self.Entry_background_from.insert(0,str(int(self.twotheta_x[0])+1)+','+str(int(self.twotheta_x[len(self.twotheta_x)-1])-2))
        
        self.Entry_background_to=Entry(main.Frame3_4_1,width=10)
        self.Entry_background_to.grid(row=i+1,column=2,sticky=W)
        #self.Entry_background_to.delete(0,END)
        #self.Entry_background_to.insert(0,str(int(self.twotheta_x[0])+2)+','+str(int(self.twotheta_x[len(self.twotheta_x)-1])-1))
        
        Label(main.Frame3_4_1, text="Polynomial fit").grid(row=i+2,column=0,sticky=W)
        Label(main.Frame3_4_1, text="degrees").grid(row=i+2,column=2,sticky=W)
        self.Entry_background_polynominal_degrees=Entry(main.Frame3_4_1,width=10)
        self.Entry_background_polynominal_degrees.grid(row=i+2,column=1,sticky=W)
        #self.Entry_background_polynominal_degrees.delete(0,END)
        #self.Entry_background_polynominal_degrees.insert(0,str(1))

        #fitting range
        i=i+4
        Label(main.Frame3_4_1, text="--------------------").grid(row=i,column=0,sticky=W)
        Label(main.Frame3_4_1, text="FITTING RANGE",bg="white").grid(row=i+1,column=0,sticky=W)
        Label(main.Frame3_4_1, text=u"2\u03B8").grid(row=i+1,column=1)
        Label(main.Frame3_4_1, text=u"\u03B3").grid(row=i+1,column=2)
        Label(main.Frame3_4_1, text="from(°)").grid(row=i+2,column=0,sticky=W)
        Label(main.Frame3_4_1, text="to(°)").grid(row=i+3,column=0,sticky=W)
        Label(main.Frame3_4_1, text="number of sections").grid(row=i+4,column=0,sticky=W)

        self.Entry_twotheta_from = Entry(main.Frame3_4_1,width=10)
        self.Entry_twotheta_to = Entry(main.Frame3_4_1,width=10)
        self.Entry_twotheta_from.grid(row=i+2, column=1,sticky=W)
        self.Entry_twotheta_to.grid(row=i+3, column=1,sticky=W)
        #self.Entry_twotheta_from.delete(0,END)
        #self.Entry_twotheta_to.delete(0,END)
        #self.Entry_twotheta_from.insert(0,str('%0.2f' % self.twotheta_x[int(self.ncol*0.25)]))
        #self.Entry_twotheta_to.insert(0,str('%0.2f' % self.twotheta_x[int(self.ncol*0.75)]))
        
        self.Entry_gamma_from = Entry(main.Frame3_4_1,width=10)
        self.Entry_gamma_to = Entry(main.Frame3_4_1,width=10)
        self.Entry_gamma_number = Entry(main.Frame3_4_1,width=10)

        self.Entry_gamma_from.grid(row=i+2, column=2,sticky=W)
        self.Entry_gamma_to.grid(row=i+3, column=2,sticky=W)
        self.Entry_gamma_number.grid(row=i+4, column=2,sticky=W)     

        #self.Entry_gamma_from.delete(0,END)
        #self.Entry_gamma_to.delete(0,END)
        #self.Entry_gamma_number.delete(0,END)     
        #self.Entry_gamma_from.insert(0,str('%0.2f' % self.gamma_y[int(self.nrow*0.25)]))
        #self.Entry_gamma_to.insert(0,str('%0.2f' % self.gamma_y[int(self.nrow*0.75)]))
        #self.Entry_gamma_number.insert(0,"10")

        i=i+5
        Label(main.Frame3_4_1, text="--------------------").grid(row=i,column=0,sticky=W)
        Label(main.Frame3_4_1, text="PEAK FIT MODEL",bg="white").grid(row=i+1,column=0,sticky=W)
        Label(main.Frame3_4_1, text="Function",font=f).grid(row=i+2,column=0,sticky=W)
        self.function_fit = IntVar()
        Radiobutton(main.Frame3_4_1, text="Pearson_VII", variable=self.function_fit, value=1).grid(row=i+3,column=0,sticky=W)
        Radiobutton(main.Frame3_4_1, text="Pseudo-Voigt", variable=self.function_fit, value=2).grid(row=i+4,column=0,sticky=W)
        Radiobutton(main.Frame3_4_1, text="Voigt", variable=self.function_fit, value=3).grid(row=i+5,column=0,sticky=W)
        Radiobutton(main.Frame3_4_1, text="Gaussian", variable=self.function_fit, value=4).grid(row=i+6,column=0,sticky=W)
        Radiobutton(main.Frame3_4_1, text="Lorentzian", variable=self.function_fit, value=5).grid(row=i+7,column=0,sticky=W)
        self.function_fit.set(1)

        Label(main.Frame3_4_1, text="Peak shape",font=f).grid(row=i+2,column=1,sticky=W)
        self.peak_shape = IntVar()
        Radiobutton(main.Frame3_4_1, text="Symmetric", variable=self.peak_shape, value=1).grid(row=i+3,column=1,sticky=W)
        Radiobutton(main.Frame3_4_1, text="Asymmetric", variable=self.peak_shape, value=2).grid(row=i+4,column=1,sticky=W)
        self.peak_shape.set(1)

        Label(main.Frame3_4_1, text="Peak rejection",font=f).grid(row=i+5,column=1,sticky=W)
        Label(main.Frame3_4_1, text="Correlation r >").grid(row=i+6,column=1,sticky=W)
        self.Entry_r=Entry(main.Frame3_4_1,width=10)
        self.Entry_r.grid(row=i+6, column=2,sticky=W)
        #self.Entry_r.insert(0,0.5)
        
        i=i+8
        Label(main.Frame3_4_1, text="Initial guess",font=f).grid(row=i,column=0,sticky=W)
        self.init_guess = IntVar()
        Radiobutton(main.Frame3_4_1, text="Auto", variable=self.init_guess, value=1).grid(row=i,column=1,sticky=W)
        Radiobutton(main.Frame3_4_1, text="Fix", variable=self.init_guess, value=2).grid(row=i,column=2,sticky=W)
        self.init_guess.set(1)
        
        Label(main.Frame3_4_1, text=u"2\u03B8(°)").grid(row=i+1,column=1,sticky=W)
        Label(main.Frame3_4_1, text="FWHM(°)").grid(row=i+1,column=2,sticky=W)

        self.Entry_peak=[]
        self.Entry_limit_peak=[]
        self.Entry_peak_width=[]
        
        Label(main.Frame3_4_1, text="1 - stress").grid(row=i+2,column=0,sticky=W)
        Label(main.Frame3_4_1, text=u"\u00B1(°)").grid(row=i+3,column=0,sticky=W)
        
        self.Entry_peak.append(Entry(main.Frame3_4_1,width=10))
        self.Entry_limit_peak.append(Entry(main.Frame3_4_1,width=10))
        self.Entry_peak_width.append(Entry(main.Frame3_4_1,width=10))
        
        self.Entry_peak[0].grid(row=i+2, column=1,sticky=W)
        self.Entry_limit_peak[0].grid(row=i+3, column=1,sticky=W)
        self.Entry_peak_width[0].grid(row=i+2, column=2,sticky=W)

        #self.Entry_limit_peak[0].insert(0,2)

        self.row_i=i+4
        self.number_peak=1
        
        self.Label_1=[]
        self.Label_2=[]
        self.Label_3=[]
        self.add_peak=Button(main.Frame3_4_1,compound=CENTER, text="Add",bg="white",command=lambda:add_peak(self,main.Frame3_4_1))
        self.add_peak.grid(row=self.row_i,column=0,sticky=W)
        
        self.delete_peak=Button(main.Frame3_4_1,compound=CENTER, text="Delete",bg="white",command=lambda:delete_peak(self,main.Frame3_4_1))
          
        Label(main.Frame3_4_2, text="MATERIAL PROPERTIES",bg="white").grid(row=0,column=0,sticky=W)
        Label(main.Frame3_4_2, text="Material").grid(row=1,column=0,sticky=W)
        Label(main.Frame3_4_2, text=u"Source").grid(row=2,column=0,sticky=W)
        Label(main.Frame3_4_2, text=u"{hkl} 2\u03B8(°) ").grid(row=3,column=0,sticky=W)
        Label(main.Frame3_4_2, text=u"Unstressed 2\u03B8(°) ").grid(row=4,column=0,sticky=W)
        Label(main.Frame3_4_2, text=u"s\u2081(MPa\u207B\u00B9)").grid(row=5,column=0,sticky=W)
        Label(main.Frame3_4_2, text=u"s\u2082/2(MPa\u207B\u00B9)").grid(row=6,column=0,sticky=W)
        Label(main.Frame3_4_2, text="Young's modulus(MPa)").grid(row=7,column=0,sticky=W)
        Label(main.Frame3_4_2, text="Poisson's ratio").grid(row=8,column=0,sticky=W)

        self.Entry_twotheta0=Entry(main.Frame3_4_2,width=10)
        self.Entry_s1=Entry(main.Frame3_4_2,width=10)
        self.Entry_half_s2=Entry(main.Frame3_4_2,width=10)
        self.Entry_Young=Entry(main.Frame3_4_2,width=10)
        self.Entry_Poisson=Entry(main.Frame3_4_2,width=10)

        self.Entry_twotheta0.grid(row=4, column=1,sticky=W)        
        self.Entry_s1.grid(row=5, column=1,sticky=W)
        self.Entry_half_s2.grid(row=6, column=1,sticky=W)
        self.Entry_Young.grid(row=7, column=1,sticky=W)
        self.Entry_Poisson.grid(row=8, column=1,sticky=W)
                
        import_material(self,main.Frame3_4_2)

        i=9
        Label(main.Frame3_4_2, text="--------------------").grid(row=i,column=0,sticky=W)
        Label(main.Frame3_4_2, text="X-RAYS PROPETIES",bg="white").grid(row=i+1,column=0,sticky=W)
        Label(main.Frame3_4_2, text=u"\u03BB"+"("+u"\u212B"+")"+" k"+u"\u03B1"+"1").grid(row=i+2,column=0,sticky=W)
        Label(main.Frame3_4_2, text=u"\u03BB"+"("+u"\u212B"+")"+" k"+u"\u03B1"+"2").grid(row=i+3,column=0,sticky=W)
        Label(main.Frame3_4_2, text="k"+u"\u03B1"+" ratio").grid(row=i+4,column=0,sticky=W)

        self.Entry_kalpha=[]
        for j in range(3):
            self.Entry_kalpha.append(Entry(main.Frame3_4_2,width=10))
            self.Entry_kalpha[j].grid(row=i+2+j, column=1,sticky=W)

            self.Entry_kalpha[j].delete(0,END)
            #if len(import_XRD.k_alpha[0])>j:
                #self.Entry_kalpha[j].insert(0,str(import_XRD.k_alpha[0][j]))
        #if len(import_XRD.k_alpha[0])==1:
            #self.Entry_kalpha[1].insert(0,str(0))
            #self.Entry_kalpha[2].insert(0,str(0))
        #if len(import_XRD.k_alpha[0])==2:
            #if import_XRD.k_alpha[0][1]==0:
                #self.Entry_kalpha[2].insert(0,str(0))
            #else:
                #self.Entry_kalpha[2].insert(0,str(0.5))

        #for j in range(2):
            #self.Entry_kalpha[j].config(state='disabled')

        self.button_init_wavelength=Button(main.Frame3_4_2,compound=CENTER,text="Initialize",bg="white",command=lambda:None)
        self.button_init_wavelength.grid(row=i+5,column=1,sticky=W)
        Button(main.Frame3_4_2,compound=CENTER,text="Lock",bg="white",command=lambda:self.x_ray_lock(self)).grid(row=i+2,column=2,sticky=W)
        Button(main.Frame3_4_2,compound=CENTER,text="Unlock",bg="white",command=lambda:self.x_ray_unlock(self)).grid(row=i+3,column=2,sticky=W)
        
        i=i+6
        Label(main.Frame3_4_2, text="--------------------").grid(row=i,column=0,sticky=W)
        self.peak_shift_correction_coefficient=[]
        self.i=i
        self.Label_sc=Label(main.Frame3_4_2)
        self.Button_delete=Button(main.Frame3_4_2)
        self.button_psc=Button(main.Frame3_4_2,compound=CENTER,text="Peak shift correction",bg="white",command=lambda:None)
        self.button_psc.grid(row=i+1,column=0,sticky=W) 

        #tools
        Button(main.Frame3_4_3,compound=CENTER,text="Import template",bg="white",command=lambda:import_calcul_parameters(self,main)).grid(row=0,column=0)
        Button(main.Frame3_4_3,compound=CENTER,text="Export template",bg="white",command=lambda:export_calcul_parameters(self,main)).grid(row=1,column=0)
        Label(main.Frame3_4_3, text="--------------------").grid(row=2,column=0)
        
        Label(main.Frame3_4_3, text="Limit color",bg="white").grid(row=3,column=0)
        self.Entry_border_color=Entry(main.Frame3_4_3,width=10)
        self.Entry_border_color.grid(row=4,column=0)

        self.Button_limit_preview=Button(main.Frame3_4_3,compound=CENTER,text="Limits preview",bg="white",command=lambda:None)
        self.Button_limit_preview.grid(row=5,column=0)
        
        self.Button_fit_preview=Button(main.Frame3_4_3,compound=CENTER,text="Fit preview",bg="white",command=lambda:None)
        self.Button_fit_preview.grid(row=6,column=0)
        
        Label(main.Frame3_4_3, text="--------------------").grid(row=7,column=0)        
        self.Button_run_calcul=Button(main.Frame3_4_3,compound=CENTER, text="RUN CALCULATION",bg="white",command=lambda:None)
        self.Button_run_calcul.grid(row=8,column=0)       
        
        self.Entry_list_image_error=Entry(main.Frame3_4_2)
      
        fig=plt.figure(1,facecolor="0.94")
        plt.close(fig)
        
        canvas = FigureCanvasTkAgg(fig, main.Frame3_4_4_1_1)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES)


    def attribute_graphic_Frame3_4(self,import_XRD,angles_modif,main_calcul,main):

        if self.Entry_background_from.get() in ['', None,'\n']:
            self.Entry_background_from.insert(0,str(int(self.twotheta_x[0])+1)+','+str(int(self.twotheta_x[len(self.twotheta_x)-1])-2))
            
        if self.Entry_background_to.get() in ['', None,'\n']:
            self.Entry_background_to.insert(0,str(int(self.twotheta_x[0])+2)+','+str(int(self.twotheta_x[len(self.twotheta_x)-1])-1))
            
        if self.Entry_background_polynominal_degrees.get() in ['', None,'\n']:
            self.Entry_background_polynominal_degrees.insert(0,str(1))

        if self.Entry_twotheta_from.get() in ['', None,'\n']:
            self.Entry_twotheta_from.insert(0,str('%0.2f' % self.twotheta_x[int(self.ncol*0.25)]))

        if self.Entry_twotheta_to.get() in ['', None,'\n']:
            self.Entry_twotheta_to.insert(0,str('%0.2f' % self.twotheta_x[int(self.ncol*0.75)]))

        if self.Entry_gamma_from.get() in ['', None,'\n']:
            self.Entry_gamma_from.insert(0,str('%0.2f' % self.gamma_y[int(self.nrow*0.25)]))

        if self.Entry_gamma_to.get() in ['', None,'\n']:
            self.Entry_gamma_to.insert(0,str('%0.2f' % self.gamma_y[int(self.nrow*0.75)]))

        if self.Entry_gamma_number.get() in ['', None,'\n']:
            self.Entry_gamma_number.insert(0,"10")

        if self.Entry_r.get() in ['', None,'\n']:
            self.Entry_r.insert(0,0.5)

        if self.Entry_limit_peak[0].get() in ['', None,'\n']:
            self.Entry_limit_peak[0].insert(0,2)
        
        for j in range(3):
            if len(import_XRD.k_alpha[0])>j:
                if self.Entry_kalpha[j].get() in ['', None,'\n']:
                    self.Entry_kalpha[j].insert(0,str(import_XRD.k_alpha[0][j]))
        if len(import_XRD.k_alpha[0])==1:
            if self.Entry_kalpha[1].get() in ['', None,'\n']:
                self.Entry_kalpha[1].insert(0,str(0))
            if self.Entry_kalpha[2].get() in ['', None,'\n']:
                self.Entry_kalpha[2].insert(0,str(0))
        if len(import_XRD.k_alpha[0])==2:
            if self.Entry_kalpha[2].get() in ['', None,'\n']:
                if import_XRD.k_alpha[0][1]==0:
                    self.Entry_kalpha[2].insert(0,str(0))
                else:
                    self.Entry_kalpha[2].insert(0,str(0.5))

        for j in range(2):
            self.Entry_kalpha[j].config(state='disabled')

        self.button_init_wavelength.config(command=lambda:self.x_ray_initialize(import_XRD))
        
        self.button_psc.config(command=lambda:import_peak_shift_correction(self,self.i,main))

        #tools
        self.Button_limit_preview.config(command=lambda:limit_preview(self,angles_modif,main)) 
        self.Button_fit_preview.config(command=lambda:fit_preview(self,angles_modif,main))       
        self.Button_run_calcul.config(command=lambda:main_calcul(self,import_XRD,angles_modif,main))   
      
        fig=plt.figure(1,facecolor="0.94")
        plt.imshow(self.intensity_2D_calib, cmap="hot",origin='lower')
        plt.yticks((1,self.nrow*0.25,self.nrow*0.5,self.nrow*0.75,self.nrow), (str("%0.1f" %self.gamma_y[0]),str("%0.1f" %self.gamma_y[int(self.nrow*0.25)]),str("%0.1f" %self.gamma_y[int(self.nrow*0.5)]),str("%0.1f" %self.gamma_y[int(self.nrow*0.75)]),str("%0.1f" %self.gamma_y[int(self.nrow-1)])))
        plt.xticks((1,self.ncol*0.25,self.ncol*0.5,self.ncol*0.75,self.ncol), (str("%0.1f" %self.twotheta_x[0]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.25)]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.5)]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.75)]),str("%0.1f" %self.twotheta_x[int(self.ncol-1)])))
        plt.xlabel(r"$2\theta(°)$")
        plt.ylabel(r"$\gamma(°)$")
        plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
        plt.close(fig)
        
        canvas = FigureCanvasTkAgg(fig, main.Frame3_4_4_1_1)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

        Label(main.Frame3_4_4_1_2, text="Image legend",bg="white").grid(row=0,column=0)
        Label(main.Frame3_4_4_1_2, text="from").grid(row=1,column=0)
        self.Entry_legend_from_3_4 = Entry(main.Frame3_4_4_1_2,width=6)
        self.Entry_legend_from_3_4.grid(row=2,column=0)
        self.Entry_legend_from_3_4.insert(0,0)
        
        Label(main.Frame3_4_4_1_2, text="to").grid(row=3,column=0)
        self.Entry_legend_to_3_4 = Entry(main.Frame3_4_4_1_2,width=6)
        self.Entry_legend_to_3_4.grid(row=4,column=0)
        self.Entry_legend_to_3_4.insert(0,max(map(max, self.intensity_2D_calib)))

        self.cmap_var_3_4=StringVar()
        Radiobutton(main.Frame3_4_4_1_2, text="hot", variable=self.cmap_var_3_4, value="hot").grid(row=5,column=0,sticky=W)
        Radiobutton(main.Frame3_4_4_1_2, text="cool", variable=self.cmap_var_3_4, value="GnBu").grid(row=6,column=0,sticky=W)
        Radiobutton(main.Frame3_4_4_1_2, text="gray", variable=self.cmap_var_3_4, value="gray").grid(row=7,column=0,sticky=W)
        Radiobutton(main.Frame3_4_4_1_2, text="nipy", variable=self.cmap_var_3_4, value="nipy_spectral").grid(row=8,column=0,sticky=W)
        self.cmap_var_3_4.set("hot")

            
    def graphic_Frame3_5(self,import_XRD,angles_modif,main_calcul,main):      
        scrollbar = Scrollbar(main.Frame3_5_1)
        scrollbar.pack(side = RIGHT, fill=Y) 
        mylist= Listbox(main.Frame3_5_1, yscrollcommand = scrollbar.set)
        mylist.pack(side = LEFT, fill = BOTH,expand=YES)
        for i in range(len(self.phi)):
            mylist.insert(END, str(i+1)+u'.\u03C6='+str(self.phi[i])+" ; "+u'\u03C7='+str(self.chi[i])+u"; \u03C9="+str(self.omega[i])+
                          ' (.'+str(import_XRD.nfile[i]+1)+'.'+str(import_XRD.nimage_i[i]+1)+'.)')
        mylist.bind("<ButtonRelease-1>", lambda event: show_calib_image(event,angles_modif,self,import_XRD,main_calcul,stress_calcul,main.Frame3_5_2,main))
        scrollbar.config(command = mylist.yview)
            
        fig=plt.figure(1,facecolor="0.94")
        plt.imshow(self.intensity_2D_calib, cmap="hot",origin='lower')
        plt.title(u'\u03C6='+str(float(self.phi[0]))+" ; "+u'\u03C7='+str(float(self.chi[0]))+"")
        plt.yticks((1,self.nrow*0.25,self.nrow*0.5,self.nrow*0.75,self.nrow), (str("%0.1f" %self.gamma_y[0]),str("%0.1f" %self.gamma_y[int(self.nrow*0.25)]),str("%0.1f" %self.gamma_y[int(self.nrow*0.5)]),str("%0.1f" %self.gamma_y[int(self.nrow*0.75)]),str("%0.1f" %self.gamma_y[int(self.nrow-1)])))
        plt.xticks((1,self.ncol*0.25,self.ncol*0.5,self.ncol*0.75,self.ncol), (str("%0.1f" %self.twotheta_x[0]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.25)]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.5)]),str("%0.1f" %self.twotheta_x[int(self.ncol*0.75)]),str("%0.1f" %self.twotheta_x[int(self.ncol-1)])))
        plt.xlabel(r"$2\theta(°)$")
        plt.ylabel(r"$\gamma(°)$")
        plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
        plt.close()

        canvas = FigureCanvasTkAgg(fig, main.Frame3_5_2)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES,ipadx=20)

        Label(main.Frame3_5_3_2, text="Image legend",bg="white").grid(row=0,column=0)
        Label(main.Frame3_5_3_2, text="from").grid(row=1,column=0,)
        self.Entry_legend_from_3_5 = Entry(main.Frame3_5_3_2,width=6)
        self.Entry_legend_from_3_5.grid(row=2,column=0)
        self.Entry_legend_from_3_5.insert(0,0)
        
        Label(main.Frame3_5_3_2, text="to").grid(row=3,column=0)
        self.Entry_legend_to_3_5 = Entry(main.Frame3_5_3_2,width=6)
        self.Entry_legend_to_3_5.grid(row=4,column=0)
        self.Entry_legend_to_3_5.insert(0,max(map(max, self.intensity_2D_calib)))

        self.cmap_var_3_5=StringVar()
        Radiobutton(main.Frame3_5_3_2, text="hot", variable=self.cmap_var_3_5, value="hot").grid(row=5,column=0,sticky=W)
        Radiobutton(main.Frame3_5_3_2, text="cool", variable=self.cmap_var_3_5, value="GnBu").grid(row=6,column=0,sticky=W)
        Radiobutton(main.Frame3_5_3_2, text="gray", variable=self.cmap_var_3_5, value="gray").grid(row=7,column=0,sticky=W)
        Radiobutton(main.Frame3_5_3_2, text="nipy", variable=self.cmap_var_3_5, value="nipy_spectral").grid(row=8,column=0,sticky=W)
        self.cmap_var_3_5.set("hot")

    def x_ray_initialize(self,import_XRD):
        for j in range(3):
            self.Entry_kalpha[j].delete(0,END)
            if len(import_XRD.k_alpha)>j:
                self.Entry_kalpha[j].insert(0,str(import_XRD.k_alpha[j]))
        if len(import_XRD.k_alpha)==1:
            self.Entry_kalpha[1].insert(0,str(0))
            self.Entry_kalpha[2].insert(0,str(0))
        if len(import_XRD.k_alpha)==2:
            self.Entry_kalpha[2].insert(0,str(0.5))

    def x_ray_lock(self):
        for j in range(2):
            self.Entry_kalpha[j].config(state='disabled')

    def x_ray_unlock(self):
        for j in range(2):
            self.Entry_kalpha[j].config(state='normal')
