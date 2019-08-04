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
from tkinter.filedialog import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class angles_modif:
    def __init__(self,main):
        main.Frame3_3_2_2_1=Frame(main.Frame3_3_2_2)
        main.Frame3_3_2_2_2=Frame(main.Frame3_3_2_2)
        self.Button_import_gma=Button(main.Frame3_3_2_2_1)
        self.Button_next=Button(main.Frame3_3_2_2_1)
        self.Button_apply_gma=Button(main.Frame3_3_2_2_2)
        
    def init(self,calib_2D,import_XRD,main_calcul,stress_calcul,main):
        calib_2D.angles_modif_valid=False

        calib_2D.Entry_phi_offset.delete(0,END)
        calib_2D.Entry_chi_offset.delete(0,END)
        calib_2D.Entry_twotheta_offset.delete(0,END)
        calib_2D.Entry_omega_offset.delete(0,END)
        calib_2D.Entry_gamma_offset.delete(0,END)   
        calib_2D.Entry_phi_offset.insert(0,"0")
        calib_2D.Entry_chi_offset.insert(0,"0")
        calib_2D.Entry_twotheta_offset.insert(0,"0")
        calib_2D.Entry_omega_offset.insert(0,"0")
        calib_2D.Entry_gamma_offset.insert(0,"0")

        self.phi=import_XRD.phi
        self.chi=import_XRD.chi
        self.omega=import_XRD.omega
        self.twotheta_center=import_XRD.twotheta_center

        self.twotheta_x=calib_2D.twotheta_x
        self.gamma_y=calib_2D.gamma_y
            
        nrow=calib_2D.nrow
        ncol=calib_2D.ncol

    #Frame3_3
        for widget in main.Frame3_3_1.winfo_children():
            widget.destroy()
        scrollbar = Scrollbar(main.Frame3_3_1)
        scrollbar.pack( side = RIGHT, fill=Y) 
        mylist= Listbox(main.Frame3_3_1, yscrollcommand = scrollbar.set,width=50)
        for i in range(len(calib_2D.phi)):
            mylist.insert(END, str(i+1)+u".\u03C6="+str(self.phi[i])+u"; \u03C7="+str(self.chi[i])+u"; \u03C9="+str(self.omega[i])+
                          ' (.'+str(import_XRD.nfile[i]+1)+'.'+str(import_XRD.nimage_i[i]+1)+'.)')
        mylist.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command = mylist.yview )

        fig=plt.figure(1,facecolor="0.94")
        cmap_var=calib_2D.cmap_var_3_2.get()
        try:
            legend_from= float(calib_2D.Entry_legend_from_3_2.get())
            legend_to= float(calib_2D.Entry_legend_to_3_2.get())
        except ValueError:
            plt.imshow(calib_2D.intensity_2D_calib, cmap=cmap_var,origin='lower')
        else:
            plt.imshow(calib_2D.intensity_2D_calib,clim=(legend_from, legend_to),cmap=cmap_var,origin='lower')
        
        plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %self.gamma_y[0]),str("%0.1f" %self.gamma_y[int(nrow*0.25)]),str("%0.1f" %self.gamma_y[int(nrow*0.5)]),str("%0.1f" %self.gamma_y[int(nrow*0.75)]),str("%0.1f" %self.gamma_y[int(nrow-1)])))
        plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %self.twotheta_x[0]),str("%0.1f" %self.twotheta_x[int(ncol*0.25)]),str("%0.1f" %self.twotheta_x[int(ncol*0.5)]),str("%0.1f" %self.twotheta_x[int(ncol*0.75)]),str("%0.1f" %self.twotheta_x[int(ncol-1)])))
        plt.xlabel(r"$2\theta(°)$")
        plt.ylabel(r"$\gamma(°)$")
        plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
        plt.close()
        
        for widget in main.Frame3_3_3.winfo_children():
            widget.destroy()  
        canvas = FigureCanvasTkAgg(fig, main.Frame3_3_3)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    #Frame3_4
        for widget in main.Frame3_4_4_1_1.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, main.Frame3_4_4_1_1)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

        main.root.mainloop()

    #---------------------------------------------------------------
    def apply(self,calib_2D,import_XRD,main_calcul,stress_calcul,main):
        try:
            phi_offset=float(calib_2D.Entry_phi_offset.get())
            chi_offset=float(calib_2D.Entry_chi_offset.get())
            twotheta_offset=float(calib_2D.Entry_twotheta_offset.get())
            omega_offset=float(calib_2D.Entry_omega_offset.get())
            gamma_offset=float(calib_2D.Entry_gamma_offset.get())
        except ValueError:
            showinfo(title="Error",message="Please verify all the value is a number\nUse '.' instead of ',' to insert a number")
        else:
            calib_2D.angles_modif_valid=True
 
            nrow=calib_2D.nrow
            ncol=calib_2D.ncol
            
            if float(calib_2D.Check_phi_invert.get())==1:
                phi_invert=-1
            else:
                phi_invert=1
                
            if float(calib_2D.Check_chi_invert.get())==1:
                chi_invert=-1
            else:
                chi_invert=1
                
            if float(calib_2D.Check_gamma_invert.get())==1:
                gamma_invert=-1
            else:
                gamma_invert=1
           
            self.phi=list((np.asarray(import_XRD.phi)-phi_offset)*phi_invert)
            self.chi=list((np.asarray(import_XRD.chi)-chi_offset)*chi_invert)
            self.omega=list(np.asarray(import_XRD.omega)-omega_offset)
            self.twotheta_center=list(np.asarray(import_XRD.twotheta_center)-twotheta_offset)

            self.twotheta_x=np.asarray(calib_2D.twotheta_x)-twotheta_offset

            if float(calib_2D.Check_twotheta_flip.get())==1:
                intensity_2D_calib=np.flip(calib_2D.intensity_2D_calib,axis=1)
            else:
                intensity_2D_calib=calib_2D.intensity_2D_calib

            gamma_y=(np.asarray(calib_2D.gamma_y)-gamma_offset)*gamma_invert

            if float(calib_2D.Check_gamma_flip.get())==1:
                self.gamma_y=np.flip(gamma_y,axis=0)
            else:
                self.gamma_y=gamma_y

            #Frame3_3
            for widget in main.Frame3_3_1.winfo_children():
                widget.destroy()
            scrollbar = Scrollbar(main.Frame3_3_1)
            scrollbar.pack( side = RIGHT, fill=Y) 
            mylist= Listbox(main.Frame3_3_1, yscrollcommand = scrollbar.set,width=50)
            for i in range(len(calib_2D.phi)):
                mylist.insert(END, str(i+1)+u".\u03C6="+str(self.phi[i])+u"; \u03C7="+str(self.chi[i])+u"; \u03C9="+str(self.omega[i])+
                              ' (.'+str(import_XRD.nfile[i]+1)+'.'+str(import_XRD.nimage_i[i]+1)+'.)')
            mylist.pack( side = LEFT, fill = BOTH )
            scrollbar.config( command = mylist.yview )

            fig=plt.figure(1,facecolor="0.94")
            
            cmap_var=calib_2D.cmap_var_3_2.get()
            try:
                legend_from= float(calib_2D.Entry_legend_from_3_2.get())
                legend_to= float(calib_2D.Entry_legend_to_3_2.get())
            except ValueError:
                plt.imshow(intensity_2D_calib, cmap=cmap_var,origin='lower')
            else:
                plt.imshow(intensity_2D_calib,clim=(legend_from, legend_to),cmap=cmap_var,origin='lower')
                
            plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %self.gamma_y[0]),str("%0.1f" %self.gamma_y[int(nrow*0.25)]),str("%0.1f" %self.gamma_y[int(nrow*0.5)]),str("%0.1f" %self.gamma_y[int(nrow*0.75)]),str("%0.1f" %self.gamma_y[int(nrow-1)])))
            plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %self.twotheta_x[0]),str("%0.1f" %self.twotheta_x[int(ncol*0.25)]),str("%0.1f" %self.twotheta_x[int(ncol*0.5)]),str("%0.1f" %self.twotheta_x[int(ncol*0.75)]),str("%0.1f" %self.twotheta_x[int(ncol-1)])))
            plt.xlabel(r"$2\theta(°)$")
            plt.ylabel(r"$\gamma(°)$")
            plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
            plt.close()
            
            for widget in main.Frame3_3_3.winfo_children():
                widget.destroy()  
            canvas = FigureCanvasTkAgg(fig, main.Frame3_3_3)
            canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

        #Frame3_4
            for widget in main.Frame3_4_4_1_1.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, main.Frame3_4_4_1_1)
            canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

        main.root.mainloop()

    def advance(self,calib_2D,import_XRD,main_calcul,stress_calcul,main):
        for widget in main.Frame3_3_2_2.winfo_children():
            widget.destroy()
        main.Frame3_3_2_2_1=Frame(main.Frame3_3_2_2)
        main.Frame3_3_2_2_1.pack(side = TOP)
        main.Frame3_3_2_2_2=Frame(main.Frame3_3_2_2)
        main.Frame3_3_2_2_2.pack(side = TOP)
        
        f=font.Font(size=9,underline=1)
        self.Button_import_gma=Button(main.Frame3_3_2_2_1,compound=CENTER, text="Import",bg="white",command=lambda:self.import_goniometric_angles(self,calib_2D,import_XRD,main_calcul,stress_calcul,main))
        self.Button_import_gma.grid(row=0,column=0,sticky=W)
        Button(main.Frame3_3_2_2_1,compound=CENTER, text="Hide",bg="white",command=lambda:self.hide(self,main)).grid(row=0,column=1,sticky=W)
        
        Label(main.Frame3_3_2_2_1, text="GONIMETER CONFIGURATION",font=f).grid(row=1,column=0,sticky=W)
        self.gonio_config = IntVar()
        Radiobutton(main.Frame3_3_2_2_1, text=u"CHI \u03C7", variable=self.gonio_config, value=1).grid(row=1,column=1,sticky=W)
        Radiobutton(main.Frame3_3_2_2_1, text=u"OMEGA \u03C9", variable=self.gonio_config, value=2).grid(row=2,column=1,sticky=W)
        self.gonio_config.set(1)

        self.Button_next=Button(main.Frame3_3_2_2_1,compound=CENTER, text="Next",bg="white",command=lambda:self.next_step(self,calib_2D,import_XRD,main_calcul,stress_calcul,main))
        self.Button_next.grid(row=3,column=0,sticky=W)

        self.Button_apply_gma=Button(main.Frame3_3_2_2_2,compound=CENTER, text="apply",bg="white")
        
        main.root.mainloop()
        

    def next_step(self,calib_2D,import_XRD,main_calcul,stress_calcul,main):
        for widget in main.Frame3_3_2_2_2.winfo_children():
            widget.destroy()
            
        f=font.Font(size=9,underline=1)
        if self.gonio_config.get()==1:
            Label(main.Frame3_3_2_2_2, text="SCAN MODE",font=f).grid(row=0,column=0,sticky=W)
            self.scan_mode = IntVar()
            Radiobutton(main.Frame3_3_2_2_2, text=u"Chi \u03C7", variable=self.scan_mode, value=1).grid(row=0,column=1,sticky=W)
            Radiobutton(main.Frame3_3_2_2_2, text=u"Phi \u03C6", variable=self.scan_mode, value=2).grid(row=1,column=1,sticky=W)
            self.scan_mode.set(1)

            Label(main.Frame3_3_2_2_2, text="2\u03B8 center").grid(row=2,column=0,sticky=W)
            self.Entry_2theta_center= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_2theta_center.grid(row=2, column=1,sticky=W)

            Label(main.Frame3_3_2_2_2, text="\u03C9 center").grid(row=3,column=0,sticky=W)
            self.Entry_omega_center= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_omega_center.grid(row=3, column=1,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"\u03C6 start").grid(row=4,column=0,sticky=W)
            self.Entry_phi_start= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_phi_start.grid(row=4, column=1,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"\u03C6 end").grid(row=4,column=2,sticky=W)
            self.Entry_phi_end= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_phi_end.grid(row=4, column=3,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"Number \u03C6").grid(row=5,column=0,sticky=W)
            self.Entry_phi_number= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_phi_number.grid(row=5, column=1,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"\u03C7 start").grid(row=6,column=0,sticky=W)
            self.Entry_chi_start= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_chi_start.grid(row=6, column=1,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"\u03C7 end").grid(row=6,column=2,sticky=W)
            self.Entry_chi_end= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_chi_end.grid(row=6, column=3,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"Number \u03C7").grid(row=7,column=0,sticky=W)
            self.Entry_chi_number= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_chi_number.grid(row=7, column=1,sticky=W)

            self.Button_apply_gma=Button(main.Frame3_3_2_2_2,compound=CENTER, text="apply",bg="white",command=lambda:self.apply_advance_1(self,calib_2D,import_XRD,main_calcul,stress_calcul,main))
            self.Button_apply_gma.grid(row=8,column=1,sticky=W)

        elif self.gonio_config.get()==2:
            Label(main.Frame3_3_2_2_2, text="SCAN MODE",font=f).grid(row=0,column=0,sticky=W)
            self.scan_mode = IntVar()
            Radiobutton(main.Frame3_3_2_2_2, text=u"Omega \u03C9", variable=self.scan_mode, value=1).grid(row=0,column=1,sticky=W)
            Radiobutton(main.Frame3_3_2_2_2, text=u"Phi \u03C6", variable=self.scan_mode, value=2).grid(row=1,column=1,sticky=W)
            self.scan_mode.set(1)

            Label(main.Frame3_3_2_2_2, text="2\u03B8 center").grid(row=2,column=0,sticky=W)
            self.Entry_2theta_center= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_2theta_center.grid(row=2, column=1,sticky=W)

            Label(main.Frame3_3_2_2_2, text="\u03C7").grid(row=3,column=0,sticky=W)
            self.Entry_chi= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_chi.grid(row=3, column=1,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"\u03C6 start").grid(row=4,column=0,sticky=W)
            self.Entry_phi_start= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_phi_start.grid(row=4, column=1,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"\u03C6 end").grid(row=4,column=2,sticky=W)
            self.Entry_phi_end= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_phi_end.grid(row=4, column=3,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"Number \u03C6").grid(row=5,column=0,sticky=W)
            self.Entry_phi_number= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_phi_number.grid(row=5, column=1,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"\u03C9 start").grid(row=6,column=0,sticky=W)
            self.Entry_omega_start= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_omega_start.grid(row=6, column=1,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"\u03C9 end").grid(row=6,column=2,sticky=W)
            self.Entry_omega_end= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_omega_end.grid(row=6, column=3,sticky=W)

            Label(main.Frame3_3_2_2_2, text=u"Number \u03C9").grid(row=7,column=0,sticky=W)
            self.Entry_omega_number= Entry(main.Frame3_3_2_2_2,width=10)
            self.Entry_omega_number.grid(row=7, column=1,sticky=W)
            
            self.Button_apply_gma=Button(main.Frame3_3_2_2_2,compound=CENTER, text="apply",bg="white",command=lambda:self.apply_advance_2(self,calib_2D,import_XRD,main_calcul,stress_calcul,main))
            self.Button_apply_gma.grid(row=8,column=1,sticky=W)
        
        main.root.mainloop()
            
    def hide(self,main):
        for widget in main.Frame3_3_2_2.winfo_children():
            widget.destroy()
            
        main.Frame3_3_2_2_1=Frame(main.Frame3_3_2_2)
        main.Frame3_3_2_2_2=Frame(main.Frame3_3_2_2)
        self.Button_import_gma=Button(main.Frame3_3_2_2_1)
        self.Button_next=Button(main.Frame3_3_2_2_1)
        self.Button_apply_gma=Button(main.Frame3_3_2_2_2)
        
        main.root.mainloop()

    def apply_advance_1(self,calib_2D,import_XRD,main_calcul,stress_calcul,main):
        try:
            twotheta_center=float(self.Entry_2theta_center.get())
            omega_center=float(self.Entry_omega_center.get())
            phi_start=float(self.Entry_phi_start.get())
            phi_end=float(self.Entry_phi_end.get())
            phi_number=int(self.Entry_phi_number.get())
            chi_start=float(self.Entry_chi_start.get())
            chi_end=float(self.Entry_chi_end.get())
            chi_number=int(self.Entry_chi_number.get())
        except ValueError:
            showinfo(title="Error",message="Please verify all values are numbers\nPlease use '.' instead of ',' to insert a number")
        else:
            calib_2D.angles_modif_valid=True
            if (phi_number-1)>=1:
                phi_step=(phi_end-phi_start)/(phi_number-1)
            else:
                phi_step=0
            if (chi_number-1)>=1:
                chi_step=(chi_end-chi_start)/(chi_number-1)
            else:
                chi_step=0

            self.twotheta_center=[twotheta_center]*len(import_XRD.phi)
            self.omega=[omega_center]*len(import_XRD.phi)
            
            self.phi=[]
            self.chi=[]
            if self.scan_mode.get()==1:
                for i in range(phi_number):
                    for j in range(chi_number):
                        self.phi.append(phi_start+i*phi_step)
                        self.chi.append(chi_start+j*chi_step)
            if self.scan_mode.get()==2:
                for i in range(chi_number):
                    for j in range(phi_number):
                        self.phi.append(phi_start+j*phi_step)
                        self.chi.append(chi_start+i*chi_step)

            if len(self.phi)>len(import_XRD.phi):
                for i in range(len(self.phi)-len(import_XRD.phi)):
                    del self.phi[-1]
                    del self.chi[-1]

            if len(self.phi)<len(import_XRD.phi):
                for i in range(len(import_XRD.phi)-len(self.phi)):
                    self.phi.append(float('NaN'))
                    self.chi.append(float('NaN'))

            twotheta_shift=self.twotheta_center[0]-calib_2D.twotheta_center[0]
            
            self.twotheta_x=[]
            for i in range(len(calib_2D.twotheta_x)):
                self.twotheta_x.append(calib_2D.twotheta_x[i]+twotheta_shift)

            intensity_2D_calib=calib_2D.intensity_2D_calib

            calib_2D.angles_modif_valid=True
 
            nrow=calib_2D.nrow
            ncol=calib_2D.ncol

            self.gamma_y=calib_2D.gamma_y

            #Frame3_3
            for widget in main.Frame3_3_1.winfo_children():
                widget.destroy()
            scrollbar = Scrollbar(main.Frame3_3_1)
            scrollbar.pack( side = RIGHT, fill=Y) 
            mylist= Listbox(main.Frame3_3_1, yscrollcommand = scrollbar.set,width=50)
            for i in range(len(calib_2D.phi)):
                mylist.insert(END, str(i+1)+u".\u03C6="+str(self.phi[i])+u"; \u03C7="+str(self.chi[i])+u"; \u03C9="+str(self.omega[i])+
                              ' (.'+str(import_XRD.nfile[i]+1)+'.'+str(import_XRD.nimage_i[i]+1)+'.)')
            mylist.pack( side = LEFT, fill = BOTH )
            scrollbar.config( command = mylist.yview )

            fig=plt.figure(1,facecolor="0.94")
            cmap_var=calib_2D.cmap_var_3_2.get()
            try:
                legend_from= float(calib_2D.Entry_legend_from_3_2.get())
                legend_to= float(calib_2D.Entry_legend_to_3_2.get())
            except ValueError:
                plt.imshow(intensity_2D_calib, cmap=cmap_var,origin='lower')
            else:
                plt.imshow(intensity_2D_calib,clim=(legend_from, legend_to),cmap=cmap_var,origin='lower')
                
            plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %self.gamma_y[0]),str("%0.1f" %self.gamma_y[int(nrow*0.25)]),str("%0.1f" %self.gamma_y[int(nrow*0.5)]),str("%0.1f" %self.gamma_y[int(nrow*0.75)]),str("%0.1f" %self.gamma_y[int(nrow-1)])))
            plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %self.twotheta_x[0]),str("%0.1f" %self.twotheta_x[int(ncol*0.25)]),str("%0.1f" %self.twotheta_x[int(ncol*0.5)]),str("%0.1f" %self.twotheta_x[int(ncol*0.75)]),str("%0.1f" %self.twotheta_x[int(ncol-1)])))
            plt.xlabel(r"$2\theta(°)$")
            plt.ylabel(r"$\gamma(°)$")
            plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
            plt.close()
            
            for widget in main.Frame3_3_3.winfo_children():
                widget.destroy()  
            canvas = FigureCanvasTkAgg(fig, main.Frame3_3_3)
            canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

        #Frame3_4
            for widget in main.Frame3_4_4_1_1.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, main.Frame3_4_4_1_1)
            canvas.get_tk_widget().pack(fill=BOTH,expand=YES)
                
        main.root.mainloop()


    def apply_advance_2(self,calib_2D,import_XRD,main_calcul,stress_calcul,main):
        try:
            twotheta_center=float(self.Entry_2theta_center.get())
            chi=float(self.Entry_chi.get())
            phi_start=float(self.Entry_phi_start.get())
            phi_end=float(self.Entry_phi_end.get())
            phi_number=int(self.Entry_phi_number.get())
            omega_start=float(self.Entry_omega_start.get())
            omega_end=float(self.Entry_omega_end.get())
            omega_number=int(self.Entry_omega_number.get())
        except ValueError:
            showinfo(title="Error",message="Please verify all values are numbers\nPlease use '.' instead of ',' to insert a number")
        else:
            calib_2D.angles_modif_valid=True
            if (phi_number-1)>=1:
                phi_step=(phi_end-phi_start)/(phi_number-1)
            else:
                phi_step=0
                
            if (omega_number-1)>=1:
                omega_step=(omega_end-omega_start)/(omega_number-1)
            else:
                omega_step=0

            self.twotheta_center=[twotheta_center]*len(import_XRD.phi)
            self.chi=[chi]*len(import_XRD.phi)
            
            self.phi=[]
            self.omega=[]
            if self.scan_mode.get()==1:
                for i in range(phi_number):
                    for j in range(chi_number):
                        self.phi.append(phi_start+i*phi_step)
                        self.omega.append(omega_start+j*omega_step)
            if self.scan_mode.get()==2:
                for i in range(chi_number):
                    for j in range(phi_number):
                        self.phi.append(phi_start+j*phi_step)
                        self.omega.append(omega_start+i*omega_step)

            if len(self.phi)>len(import_XRD.phi):
                for i in range(len(self.phi)-len(import_XRD.phi)):
                    del self.phi[-1]
                    del self.omega[-1]

            if len(self.phi)<len(import_XRD.phi):
                for i in range(len(import_XRD.phi)-len(self.phi)):
                    self.phi.append(float('NaN'))
                    self.omega.append(float('NaN'))

            twotheta_shift=self.twotheta_center[0]-calib_2D.twotheta_center[0]
            
            self.twotheta_x=[]
            for i in range(len(calib_2D.twotheta_x)):
                self.twotheta_x.append(calib_2D.twotheta_x[i]+twotheta_shift)

            intensity_2D_calib=calib_2D.intensity_2D_calib

            calib_2D.angles_modif_valid=True
 
            nrow=calib_2D.nrow
            ncol=calib_2D.ncol

            self.gamma_y=calib_2D.gamma_y

            #Frame3_3
            for widget in main.Frame3_3_1.winfo_children():
                widget.destroy()
            scrollbar = Scrollbar(main.Frame3_3_1)
            scrollbar.pack( side = RIGHT, fill=Y) 
            mylist= Listbox(main.Frame3_3_1, yscrollcommand = scrollbar.set,width=50)
            for i in range(len(calib_2D.phi)):
                mylist.insert(END, str(i+1)+u".\u03C6="+str(self.phi[i])+u"; \u03C7="+str(self.chi[i])+u"; \u03C9="+str(self.omega[i])+
                              ' (.'+str(import_XRD.nfile[i]+1)+'.'+str(import_XRD.nimage_i[i]+1)+'.)')
            mylist.pack( side = LEFT, fill = BOTH )
            scrollbar.config( command = mylist.yview )

            fig=plt.figure(1,facecolor="0.94")
            cmap_var=calib_2D.cmap_var_3_2.get()
            try:
                legend_from= float(calib_2D.Entry_legend_from_3_2.get())
                legend_to= float(calib_2D.Entry_legend_to_3_2.get())
            except ValueError:
                plt.imshow(intensity_2D_calib, cmap=cmap_var,origin='lower')
            else:
                plt.imshow(intensity_2D_calib,clim=(legend_from, legend_to),cmap=cmap_var,origin='lower')

            plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %self.gamma_y[0]),str("%0.1f" %self.gamma_y[int(nrow*0.25)]),str("%0.1f" %self.gamma_y[int(nrow*0.5)]),str("%0.1f" %self.gamma_y[int(nrow*0.75)]),str("%0.1f" %self.gamma_y[int(nrow-1)])))
            plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %self.twotheta_x[0]),str("%0.1f" %self.twotheta_x[int(ncol*0.25)]),str("%0.1f" %self.twotheta_x[int(ncol*0.5)]),str("%0.1f" %self.twotheta_x[int(ncol*0.75)]),str("%0.1f" %self.twotheta_x[int(ncol-1)])))
            plt.xlabel(r"$2\theta(°)$")
            plt.ylabel(r"$\gamma(°)$")
            plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
            plt.close()
            
            for widget in main.Frame3_3_3.winfo_children():
                widget.destroy()  
            canvas = FigureCanvasTkAgg(fig, main.Frame3_3_3)
            canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

        #Frame3_4
            for widget in main.Frame3_4_4_1_1.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, main.Frame3_4_4_1_1)
            canvas.get_tk_widget().pack(fill=BOTH,expand=YES)
                
        main.root.mainloop()

    def import_goniometric_angles(self,calib_2D,import_XRD,main_calcul,stress_calcul,main):
        f = askopenfilename(parent=main.root,title="Open file",filetypes=[('file type','*.gma;*.GMA'),('all files','.*')])
        if f is not None or f is not '':
            try:
                f_open=open(f,"r")
                line_text=f_open.readline() #Phi Chi Omega 2theta
                
                self.phi=[]
                self.chi=[]
                self.twotheta_center=[]
                self.omega=[]
                line_text=f_open.readline()
                while line_text is not None and line_text is not '' and len(self.phi)<len(import_XRD.phi):
                    angles=line_text.split()
                    try:
                        self.phi.append(float(angles[1]))
                        self.chi.append(float(angles[2]))
                        self.omega.append(float(angles[3]))
                        self.twotheta_center.append(float(angles[4]))
                    except Exception:
                        showinfo(title="Warning",message="Invalid format")
                        return
                    line_text=f_open.readline()

                if len(self.phi)<len(import_XRD.phi):
                    for i in range(len(import_XRD.phi)-len(self.phi)):
                        self.phi.append(float('NaN'))
                        self.chi.append(float('NaN'))
                        self.omega.append(float('NaN'))
                        self.twotheta_center.append(float('NaN'))

                twotheta_shift=self.twotheta_center[0]-calib_2D.twotheta_center[0]
                self.twotheta_x=[]
                for i in range(len(calib_2D.twotheta_x)):
                    self.twotheta_x.append(calib_2D.twotheta_x[i]+twotheta_shift)

                intensity_2D_calib=calib_2D.intensity_2D_calib

                calib_2D.angles_modif_valid=True
     
                nrow=calib_2D.nrow
                ncol=calib_2D.ncol

                self.gamma_y=calib_2D.gamma_y

                #Frame3_3
                for widget in main.Frame3_3_1.winfo_children():
                    widget.destroy()
                scrollbar = Scrollbar(main.Frame3_3_1)
                scrollbar.pack( side = RIGHT, fill=Y) 
                mylist= Listbox(main.Frame3_3_1, yscrollcommand = scrollbar.set,width=50)
                for i in range(len(calib_2D.phi)):
                    mylist.insert(END, str(i+1)+u".\u03C6="+str(self.phi[i])+u"; \u03C7="+str(self.chi[i])+u"; \u03C9="+str(self.omega[i])+
                                  ' (.'+str(import_XRD.nfile[i]+1)+'.'+str(import_XRD.nimage_i[i]+1)+'.)')
                mylist.pack( side = LEFT, fill = BOTH )
                scrollbar.config( command = mylist.yview )

                fig=plt.figure(1,facecolor="0.94")
                cmap_var=calib_2D.cmap_var_3_2.get()
                try:
                    legend_from= float(calib_2D.Entry_legend_from_3_2.get())
                    legend_to= float(calib_2D.Entry_legend_to_3_2.get())
                except ValueError:
                    plt.imshow(intensity_2D_calib, cmap=cmap_var,origin='lower')
                else:
                    plt.imshow(intensity_2D_calib,clim=(legend_from, legend_to),cmap=cmap_var,origin='lower')
         
                plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), (str("%0.1f" %self.gamma_y[0]),str("%0.1f" %self.gamma_y[int(nrow*0.25)]),str("%0.1f" %self.gamma_y[int(nrow*0.5)]),str("%0.1f" %self.gamma_y[int(nrow*0.75)]),str("%0.1f" %self.gamma_y[int(nrow-1)])))
                plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), (str("%0.1f" %self.twotheta_x[0]),str("%0.1f" %self.twotheta_x[int(ncol*0.25)]),str("%0.1f" %self.twotheta_x[int(ncol*0.5)]),str("%0.1f" %self.twotheta_x[int(ncol*0.75)]),str("%0.1f" %self.twotheta_x[int(ncol-1)])))
                plt.xlabel(r"$2\theta(°)$")
                plt.ylabel(r"$\gamma(°)$")
                plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
                plt.close()
                
                for widget in main.Frame3_3_3.winfo_children():
                    widget.destroy()  
                canvas = FigureCanvasTkAgg(fig, main.Frame3_3_3)
                canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

            #Frame3_4
                for widget in main.Frame3_4_4_1_1.winfo_children():
                    widget.destroy()
                canvas = FigureCanvasTkAgg(fig, main.Frame3_4_4_1_1)
                canvas.get_tk_widget().pack(fill=BOTH,expand=YES)
            except Exception:
                showinfo(title="Error",message="Uncorrected file format")
            else:
                calib_2D.angles_modif_valid=True

        main.root.mainloop()
                
