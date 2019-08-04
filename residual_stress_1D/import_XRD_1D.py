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
from tkinter import font
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import Progressbar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import traceback

from read_file.scan_1D.read_scan_1D import read_scan_1D
from read_file.import_material import import_material
from residual_stress_1D.main_calcul_1D import main_calcul
from residual_stress_1D.angles_modification_1D import angles_modif
from visualisation.preview_1D import limit_preview, fit_preview
from visualisation.pack_Frame import pack_Frame_1D
from visualisation.fig_style import fig_style
from tools.calcul_parameters import import_calcul_parameters, export_calcul_parameters
from tools.peak_shift_correction import import_peak_shift_correction
from tools.add_peak import add_peak, delete_peak
from visualisation.show_XRD_1D import show_original_graph
from tools.export_graph_1D import export_all_original_graph

class import_XRD:
    def __init__(self,main):
        try:
            self.process(main)
        except Exception as e:
            showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
            return
        else:
            angles_modif.def_button(angles_modif,self,main)
            
        main.root.mainloop()

    def process(self,main):
        format_='*.uxd;*.nja;*.raw;*.Profile;*.txt;*.UXD;*.NJA;*.RAW;*.PROFILE;*TXT'
        f = askopenfilenames(parent=main.root,title="Open file",filetypes=[('all supported format',format_),
                                                                           ('all files','.*')])
        self.file_link = main.root.tk.splitlist(f)
        if len(self.file_link)>0:
            self.import_file(main)
            if len(self.data_y)>0:
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.destroy_widget(main)
                self.graphic_frame3_1(main)
                #----------------------
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.attribute_graphic_frame3_2(main)
                #----------------------
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.attribute_graphic_frame3_3(main)
                #----------------------
                for widget in main.Frame1_2.winfo_children():
                    widget.destroy()
                pack_Frame_1D(main,1)
            else:
                showinfo(title="Warning",message="The scan is empty")

    def import_file(self,main):
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()
        Label(main.Frame1_2,text="Import files").pack(side=LEFT)
        self.progress = Progressbar(main.Frame1_2,orient="horizontal",  mode='determinate')
        self.progress.pack()
        self.progress["value"] = 0
        self.progress["maximum"] = len(self.file_link)+3
            
        self.filename=[]
        self.phi=[]
        self.chi=[]
        self.omega=[]
        self.twotheta=[]
        self.data_x=[]
        self.data_y=[]
        self.k_alpha=[]
        self.file_info=[]
        self.range_info=[]
            
        for i in range(len(self.file_link)):
            self.progress["value"] = self.progress["value"]+1
            self.progress.update()

            f=self.file_link[i].split("/")
            self.filename.append(f[len(f)-1])

            read_scan_1D(self.file_link[i],self)

    def destroy_widget(self,main):
        for widget in main.Frame3_1_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_1_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_1_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_1_4.winfo_children():
            widget.destroy()
            
        for widget in main.Frame3_2_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_2_3.winfo_children():
            widget.destroy()
            
        for widget in main.Frame3_3_4.winfo_children():
            widget.destroy()

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
        for widget in main.Frame3_4_3_3.winfo_children():
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
        for widget in main.Frame3_5_3_3.winfo_children():
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
  
    def graphic_frame3_1(self,main):
        scrollbar = Scrollbar(main.Frame3_1_1)
        scrollbar.pack(side = RIGHT, fill=BOTH) 
        mylist = Listbox(main.Frame3_1_1, yscrollcommand = scrollbar.set)
        mylist.insert(END, "0.All original graphs")
        for i in range(len(self.phi)):
            mylist.insert(END,str(i+1)+u".\u03C6="+str(float(self.phi[i]))+u"; \u03C7="+str(float(self.chi[i]))+u"; \u03C9="+str(float(self.omega[i])))
        mylist.pack(side = LEFT, fill=BOTH,expand=YES)
        mylist.bind("<ButtonRelease-1>", lambda event: show_original_graph(event,self,main))
        scrollbar.config( command = mylist.yview )   

        f=plt.figure(1,facecolor="0.94")
        for i in range(len(self.phi)):
            plt.plot(self.data_x[i],self.data_y[i],label=str(i+1))
        plt.xlabel(r"$2\theta$"+'°')
        plt.ylabel("Intensity")
        plt.title("All original graph")
        plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.)
        plt.subplots_adjust(bottom=0.4)
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_1_2)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
  
        canvas = FigureCanvasTkAgg(f, main.Frame3_2_3)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        fig_style(self,main.Frame3_1_3)

        Button(main.Frame3_1_4, text = 'Export all as image',bg="white", command = lambda: export_all_original_graph(self,main)).grid(row=1,column=0,sticky=W)

    def graphic_frame3_2(self,main):
        #self.angles_modif_valid=False
        Label(main.Frame3_2_2_1, text="ANGLES MODIFICATION",bg="white").grid(row=0,column=0,sticky=W)
        Label(main.Frame3_2_2_1, text=u"PHI \u03C6").grid(row=1,column=0,sticky=W)
        Label(main.Frame3_2_2_1, text="offset (°)").grid(row=1,column=1,sticky=W)
        
        Label(main.Frame3_2_2_1, text=u"CHI \u03C7").grid(row=2,column=0,sticky=W)
        Label(main.Frame3_2_2_1, text="offset (°)").grid(row=2,column=1,sticky=W)
        
        Label(main.Frame3_2_2_1, text=u"2 THETA 2\u03B8").grid(row=3,column=0,sticky=W)
        Label(main.Frame3_2_2_1, text="offset (°)").grid(row=3,column=1,sticky=W)

        Label(main.Frame3_2_2_1, text=u"OMEGA \u03C9").grid(row=4,column=0,sticky=W)
        Label(main.Frame3_2_2_1, text="offset (°)").grid(row=4,column=1,sticky=W)
        
        self.phi_invert = IntVar()
        Checkbutton(main.Frame3_2_2_1, text="Invert", variable=self.phi_invert).grid(row=1,column=3,sticky=W)
        self.chi_invert = IntVar()
        Checkbutton(main.Frame3_2_2_1, text="Invert", variable=self.chi_invert).grid(row=2,column=3,sticky=W)
        
        self.Entry_phi_offset= Entry(main.Frame3_2_2_1)
        self.Entry_chi_offset= Entry(main.Frame3_2_2_1)
        self.Entry_twotheta_offset= Entry(main.Frame3_2_2_1)
        self.Entry_omega_offset= Entry(main.Frame3_2_2_1)
        
        self.Entry_phi_offset.grid(row=1, column=2,sticky=W)
        self.Entry_chi_offset.grid(row=2, column=2,sticky=W)
        self.Entry_twotheta_offset.grid(row=3, column=2,sticky=W)
        self.Entry_omega_offset.grid(row=4, column=2,sticky=W)
        
        self.Entry_phi_offset.insert(0,"0")
        self.Entry_chi_offset.insert(0,"0")
        self.Entry_twotheta_offset.insert(0,"0")
        self.Entry_omega_offset.insert(0,"0")
                              
        self.button_apply=Button(main.Frame3_2_2_1,compound=CENTER, text="Apply",bg="white",command=lambda:None)
        self.button_apply.grid(row=5, column=0,sticky=W)
        self.button_init=Button(main.Frame3_2_2_1,compound=CENTER, text="Initialize",bg="white",command=lambda:None)
        self.button_init.grid(row=6,column=0,sticky=W)
        self.button_advance=Button(main.Frame3_2_2_1,compound=CENTER, text="Advance",bg="white",command=lambda:None)
        self.button_advance.grid(row=8,column=0,sticky=W)

        self.button_import_gma=Button(main.Frame3_2_2_2,compound=CENTER, text="Import",bg="white",command=lambda:None)
        self.button_next_gma=Button(main.Frame3_2_2_4,compound=CENTER, text="Next",bg="white",command=lambda:None)
        self.button_apply_gma=Button(main.Frame3_2_2_6,compound=CENTER, text="apply",bg="white",command=lambda:None)
    
        self.gonio_config = IntVar()

    def attribute_graphic_frame3_2(self,main):
        scrollbar = Scrollbar(main.Frame3_2_1)
        scrollbar.pack( side = RIGHT, fill=BOTH,expand=YES) 
        mylist = Listbox(main.Frame3_2_1, yscrollcommand = scrollbar.set)
        for i in range(len(self.phi)):
            mylist.insert(END, str(i+1)+u".\u03C6="+str(float(self.phi[i]))+u"; \u03C7="+str(float(self.chi[i]))+u"; \u03C9="+str(float(self.omega[i])))
        mylist.pack( side = LEFT, fill = BOTH ,expand=YES)
        scrollbar.config( command = mylist.yview )

        self.angles_modif_valid=False
                             
        self.button_apply.config(command=lambda:angles_modif.apply(angles_modif,self,main))
        self.button_init.config(command=lambda:angles_modif.init(angles_modif,self,main))
        self.button_advance.config(command=lambda:angles_modif.advance(angles_modif,self,main))

        self.button_import_gma.config(command=lambda:angles_modif.import_goniometric_angles(angles_modif,self,main))
        self.button_next_gma.config(command=lambda:angles_modif.next_step(angles_modif,self,main))

        if self.gonio_config.get()==1:
            self.button_apply_gma.config(command=lambda:angles_modif.apply_advance_1(angles_modif,self,main))
        elif self.gonio_config.get()==2:
            self.button_apply_gma.config(command=lambda:angles_modif.apply_advance_2(angles_modif,self,main))

    def graphic_frame3_3(self,main):
        #background limit
        f=font.Font(size=9,underline=1)
        
        i=0
        Label(main.Frame3_3_1, text="BACKGROUND",bg="white").grid(row=i,column=0,sticky=W)
        Label(main.Frame3_3_1, text=u"2\u03B8 from(°)").grid(row=i,column=1,sticky=W)
        Label(main.Frame3_3_1, text=u"2\u03B8 to(°)").grid(row=i,column=2,sticky=W)

        Label(main.Frame3_3_1, text="range 1,2,...").grid(row=i+1,column=0,sticky=W)
        self.Entry_background_from=Entry(main.Frame3_3_1,width=10)
        self.Entry_background_from.grid(row=i+1,column=1,sticky=W)
        #self.Entry_background_from.delete(0,END)
        #self.Entry_background_from.insert(0,str(int(self.data_x[0][0])+1)+','+str(int(self.data_x[0][len(self.data_x[0])-1])-2))
        
        self.Entry_background_to=Entry(main.Frame3_3_1,width=10)
        self.Entry_background_to.grid(row=i+1,column=2,sticky=W)
        #self.Entry_background_to.delete(0,END)
        #self.Entry_background_to.insert(0,str(int(self.data_x[0][0])+2)+','+str(int(self.data_x[0][len(self.data_x[0])-1])-1))
        
        Label(main.Frame3_3_1, text="Polynomial fit").grid(row=i+2,column=0,sticky=W)
        Label(main.Frame3_3_1, text="degrees").grid(row=i+2,column=2,sticky=W)
        self.Entry_background_polynominal_degrees=Entry(main.Frame3_3_1,width=10)
        self.Entry_background_polynominal_degrees.grid(row=i+2,column=1,sticky=W)
        self.Entry_background_polynominal_degrees.delete(0,END)
        #self.Entry_background_polynominal_degrees.insert(0,str(1))

        #fitting limits
        i=i+3
        Label(main.Frame3_3_1, text="--------------------").grid(row=i,column=0,sticky=W)
        Label(main.Frame3_3_1, text="FITTING RANGE",bg="white").grid(row=i+1,column=0,sticky=W)
        Label(main.Frame3_3_1, text=u"2\u03B8").grid(row=i+1,column=1,sticky=W)
        Label(main.Frame3_3_1, text="from(°)").grid(row=i+2,column=0,sticky=W)
        Label(main.Frame3_3_1, text="to(°)").grid(row=i+3,column=0,sticky=W)
        self.Entry_twotheta_from = Entry(main.Frame3_3_1,width=10)
        self.Entry_twotheta_to = Entry(main.Frame3_3_1,width=10)
        self.Entry_twotheta_from.grid(row=i+2, column=1,sticky=W)
        self.Entry_twotheta_to.grid(row=i+3, column=1,sticky=W)

        self.Entry_twotheta_from.delete(0,END)
        self.Entry_twotheta_to.delete(0,END)
        #self.Entry_twotheta_from.insert(0,str('%0.2f' % self.data_x[0][0]))
        #self.Entry_twotheta_to.insert(0,str('%0.2f' % self.data_x[0][len(self.data_x[0])-1]))
        
        #peak option
        i=i+4
        Label(main.Frame3_3_1, text="--------------------").grid(row=i,column=0,sticky=W)
        Label(main.Frame3_3_1, text="PEAK FIT MODEL",bg="white").grid(row=i+1,column=0,sticky=W)
        Label(main.Frame3_3_1, text="Function",font=f).grid(row=i+2,column=0,sticky=W)
        self.function_fit = IntVar()
        Radiobutton(main.Frame3_3_1, text="Pearson_VII", variable=self.function_fit, value=1).grid(row=i+3,column=0,sticky=W)
        Radiobutton(main.Frame3_3_1, text="Pseudo-Voigt", variable=self.function_fit, value=2).grid(row=i+4,column=0,sticky=W)
        Radiobutton(main.Frame3_3_1, text="Voigt", variable=self.function_fit, value=3).grid(row=i+5,column=0,sticky=W)
        Radiobutton(main.Frame3_3_1, text="Gaussian", variable=self.function_fit, value=4).grid(row=i+6,column=0,sticky=W)
        Radiobutton(main.Frame3_3_1, text="Lorentzian", variable=self.function_fit, value=5).grid(row=i+7,column=0,sticky=W)
        self.function_fit.set(1)

        Label(main.Frame3_3_1, text="Peak shape",font=f).grid(row=i+2,column=1,sticky=W)
        self.peak_shape = IntVar()
        Radiobutton(main.Frame3_3_1, text="Symmetric", variable=self.peak_shape, value=1).grid(row=i+3,column=1,sticky=W)
        Radiobutton(main.Frame3_3_1, text="Asymmetric", variable=self.peak_shape, value=2).grid(row=i+4,column=1,sticky=W)
        self.peak_shape.set(1)

        
        Label(main.Frame3_3_1, text="Peak rejection",font=f).grid(row=i+5,column=1,sticky=W)
        Label(main.Frame3_3_1, text="Correlation r >").grid(row=i+6,column=1,sticky=W)
        self.Entry_r=Entry(main.Frame3_3_1,width=10)
        self.Entry_r.grid(row=i+6, column=2,sticky=W)
        #self.Entry_r.insert(0,0.5)
        
        i=i+8
        Label(main.Frame3_3_1, text="Initial guess",font=f).grid(row=i,column=0,sticky=W)
        self.init_guess = IntVar()
        Radiobutton(main.Frame3_3_1, text="Auto", variable=self.init_guess, value=1).grid(row=i,column=1,sticky=W)
        Radiobutton(main.Frame3_3_1, text="Fix", variable=self.init_guess, value=2).grid(row=i,column=2,sticky=W)
        self.init_guess.set(1)
        
        Label(main.Frame3_3_1, text=u"2\u03B8(°)").grid(row=i+1,column=1,sticky=W)
        Label(main.Frame3_3_1, text="FWHM(°)").grid(row=i+1,column=2,sticky=W)
        
        self.Entry_peak=[]
        self.Entry_limit_peak=[]
        self.Entry_peak_width=[]
        
        Label(main.Frame3_3_1, text="1 - stress").grid(row=i+2,column=0,sticky=W)
        Label(main.Frame3_3_1, text=u"\u00B1(°)").grid(row=i+3,column=0,sticky=W)
        
        self.Entry_peak.append(Entry(main.Frame3_3_1,width=10))
        self.Entry_limit_peak.append(Entry(main.Frame3_3_1,width=10))
        self.Entry_peak_width.append(Entry(main.Frame3_3_1,width=10))
        
        self.Entry_peak[0].grid(row=i+2, column=1,sticky=W)
        self.Entry_limit_peak[0].grid(row=i+3, column=1,sticky=W)
        self.Entry_peak_width[0].grid(row=i+2, column=2,sticky=W)

        #self.Entry_limit_peak[0].insert(0,2)

        self.row_i=i+4
        self.number_peak=1
        
        self.Label_1=[]
        self.Label_2=[]
        self.Label_3=[]
        self.add_peak=Button(main.Frame3_3_1,compound=CENTER, text="Add",bg="white",command=lambda:add_peak(self,main.Frame3_3_1))
        self.add_peak.grid(row=self.row_i,column=0,sticky=W)
        
        self.delete_peak=Button(main.Frame3_3_1,compound=CENTER, text="Delete",bg="white",command=lambda:delete_peak(self,main.Frame3_3_1))

        #Material propreties--------------
        Label(main.Frame3_3_2, text="MATERIAL PROPERTIES",bg="white").grid(row=0,column=0,sticky=W)
        Label(main.Frame3_3_2, text="Material").grid(row=1,column=0,sticky=W)
        Label(main.Frame3_3_2, text=u"Source").grid(row=2,column=0,sticky=W)
        Label(main.Frame3_3_2, text=u"{hkl} 2\u03B8(°)").grid(row=3,column=0,sticky=W)
        Label(main.Frame3_3_2, text=u"Unstressed 2\u03B8(°) ").grid(row=4,column=0,sticky=W)
        Label(main.Frame3_3_2, text=u"s\u2081(MPa\u207B\u00B9)").grid(row=5,column=0,sticky=W)
        Label(main.Frame3_3_2, text=u"s\u2082/2(MPa\u207B\u00B9)").grid(row=6,column=0,sticky=W)
        Label(main.Frame3_3_2, text="Young's modulus(MPa)").grid(row=7,column=0,sticky=W)
        Label(main.Frame3_3_2, text="Poisson's ratio").grid(row=8,column=0,sticky=W)

        self.Entry_twotheta0=Entry(main.Frame3_3_2,width=10)
        self.Entry_s1=Entry(main.Frame3_3_2,width=10)
        self.Entry_half_s2=Entry(main.Frame3_3_2,width=10)
        self.Entry_Young=Entry(main.Frame3_3_2,width=10)
        self.Entry_Poisson=Entry(main.Frame3_3_2,width=10)

        self.Entry_twotheta0.grid(row=4, column=1,sticky=W)  
        self.Entry_s1.grid(row=5, column=1,sticky=W)
        self.Entry_half_s2.grid(row=6, column=1,sticky=W)
        self.Entry_Young.grid(row=7, column=1,sticky=W)
        self.Entry_Poisson.grid(row=8, column=1,sticky=W)
                
        import_material(self,main.Frame3_3_2)

        i=9
        Label(main.Frame3_3_2, text="--------------------").grid(row=i,column=0,sticky=W)
        Label(main.Frame3_3_2, text="X-RAYS PROPETIES",bg="white").grid(row=i+1,column=0,sticky=W)
        Label(main.Frame3_3_2, text=u"\u03BB"+"("+u"\u212B"+")"+" k"+u"\u03B1"+"1").grid(row=i+2,column=0,sticky=W)
        Label(main.Frame3_3_2, text=u"\u03BB"+"("+u"\u212B"+")"+" k"+u"\u03B1"+"2").grid(row=i+3,column=0,sticky=W)
        Label(main.Frame3_3_2, text="k"+u"\u03B1"+" ratio").grid(row=i+4,column=0,sticky=W)

        self.Entry_kalpha=[]
        for j in range(3):
            self.Entry_kalpha.append(Entry(main.Frame3_3_2,width=10))
            self.Entry_kalpha[j].grid(row=i+2+j, column=1,sticky=W)

            self.Entry_kalpha[j].delete(0,END)
            #if len(self.k_alpha)>j:
                #self.Entry_kalpha[j].insert(0,str(self.k_alpha[j]))
        #if len(self.k_alpha)==1:
            #self.Entry_kalpha[1].insert(0,str(0))
            #self.Entry_kalpha[2].insert(0,str(0))
        #if len(self.k_alpha)==2:
            #self.Entry_kalpha[2].insert(0,str(0.5))

        #for j in range(2):
            #self.Entry_kalpha[j].config(state='disabled')

        self.button_init_wavelength=Button(main.Frame3_3_2,compound=CENTER,text="Initialize",bg="white",command=None)
        self.button_init_wavelength.grid(row=i+5,column=1,sticky=W)
        Button(main.Frame3_3_2,compound=CENTER,text="Lock",bg="white",command=lambda:self.x_ray_lock(self)).grid(row=i+2,column=2,sticky=W)
        Button(main.Frame3_3_2,compound=CENTER,text="Unlock",bg="white",command=lambda:self.x_ray_unlock(self)).grid(row=i+3,column=2,sticky=W)
        
        i=i+6
        Label(main.Frame3_3_2, text="--------------------").grid(row=i,column=0,sticky=W)
        self.peak_shift_correction_coefficient=[]
        self.i=i
        self.Label_sc=Label(main.Frame3_3_2)
        self.Button_delete=Button(main.Frame3_3_2)
        self.button_psc=Button(main.Frame3_3_2,compound=CENTER,text="Peak shift correction",bg="white",command=None)
        self.button_psc.grid(row=i+1,column=0,sticky=W) 

        #tools                
        Button(main.Frame3_3_3,compound=CENTER,text="Import template",bg="white",command=lambda:import_calcul_parameters(self,main)).grid(row=0,column=0)
        Button(main.Frame3_3_3,compound=CENTER,text="Export template",bg="white",command=lambda:export_calcul_parameters(self,main)).grid(row=1,column=0)
        Label(main.Frame3_3_3, text="--------------------").grid(row=2,column=0) 
        self.Button_limit_preview=Button(main.Frame3_3_3,compound=CENTER,text="Limits preview",bg="white",command=None)
        self.Button_limit_preview.grid(row=3,column=0)
        self.Button_fit_preview=Button(main.Frame3_3_3,compound=CENTER,text="Fit preview",bg="white",command=None)
        self.Button_fit_preview.grid(row=4,column=0)
        Label(main.Frame3_3_3, text="--------------------").grid(row=5,column=0)        
        self.Button_run_calcul=Button(main.Frame3_3_3,compound=CENTER, text="RUN CALCULATION",bg="white",command=None)
        self.Button_run_calcul.grid(row=6,column=0)       
        #----------------------------
        f=plt.figure(1,facecolor="0.94")
        plt.close(f)
        canvas = FigureCanvasTkAgg(f, main.Frame3_3_4)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    def attribute_graphic_frame3_3(self,main):
        if self.Entry_background_from.get() in ['', None,'\n']:
            self.Entry_background_from.insert(0,str(int(self.data_x[0][0])+1)+','+str(int(self.data_x[0][len(self.data_x[0])-1])-2))
            
        if self.Entry_background_to.get() in ['', None,'\n']:
            self.Entry_background_to.insert(0,str(int(self.data_x[0][0])+2)+','+str(int(self.data_x[0][len(self.data_x[0])-1])-1))
            
        if self.Entry_background_polynominal_degrees.get() in ['', None,'\n']:
            self.Entry_background_polynominal_degrees.insert(0,str(1))

        if self.Entry_twotheta_from.get() in ['', None,'\n']:
            self.Entry_twotheta_from.insert(0,str('%0.2f' % self.data_x[0][0]))

        if self.Entry_twotheta_to.get() in ['', None,'\n']:
            self.Entry_twotheta_to.insert(0,str('%0.2f' % self.data_x[0][len(self.data_x[0])-1]))

        if self.Entry_r.get() in ['', None,'\n']:
            self.Entry_r.insert(0,0.5)

        if self.Entry_limit_peak[0].get() in ['', None,'\n']:
            self.Entry_limit_peak[0].insert(0,2)
            
        for j in range(3):
            if len(self.k_alpha)>j:
                if self.Entry_kalpha[j].get() in ['', None,'\n']:
                    self.Entry_kalpha[j].insert(0,str(self.k_alpha[j]))
        if len(self.k_alpha)==1:
            if self.Entry_kalpha[1].get() in ['', None,'\n']:
                self.Entry_kalpha[1].insert(0,str(0))
            if self.Entry_kalpha[2].get() in ['', None,'\n']:
                self.Entry_kalpha[2].insert(0,str(0))
        if len(self.k_alpha)==2:
            if self.Entry_kalpha[2].get() in ['', None,'\n']:
                if import_XRD.k_alpha[0][1]==0:
                    self.Entry_kalpha[2].insert(0,str(0))
                else:
                    self.Entry_kalpha[2].insert(0,str(0.5))

        for j in range(2):
            self.Entry_kalpha[j].config(state='disabled')

        self.button_init_wavelength.config(command=self.x_ray_initialize)
        
        i=15
        Label(main.Frame3_3_2, text="--------------------").grid(row=i,column=0,sticky=W)
        self.peak_shift_correction_coefficient=[]
        self.i=i
        self.Label_sc=Label(main.Frame3_3_2)
        self.Button_delete=Button(main.Frame3_3_2)
        self.button_psc.config(command=lambda:import_peak_shift_correction(self,self.i,main))

        #tools                
        self.Button_limit_preview.config(command=lambda:limit_preview(self,angles_modif,main))
        self.Button_fit_preview.config(command=lambda:fit_preview(self,angles_modif,main))       
        self.Button_run_calcul.config(command=lambda:main_calcul(self,angles_modif,main))   
        #----------------------------
        f=plt.figure(1,facecolor="0.94")
        for i in range(len(self.phi)):
            plt.plot(self.data_x[i],self.data_y[i],label=""+str(i+1)+"")
        plt.xlabel(r"$2\theta$")
        plt.ylabel("Intensity")
        plt.title("All original graph")
        plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.,fontsize='x-small')
        plt.subplots_adjust(bottom=0.4)
        plt.close(f)
        canvas = FigureCanvasTkAgg(f, main.Frame3_3_4)
        canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

        
    def x_ray_initialize(self):
        for j in range(3):
            self.Entry_kalpha[j].delete(0,END)
            if len(self.k_alpha)>j:
                self.Entry_kalpha[j].insert(0,str(self.k_alpha[j]))
        if len(self.k_alpha)==1:
            self.Entry_kalpha[1].insert(0,str(0))
            self.Entry_kalpha[2].insert(0,str(0))
        if len(self.k_alpha)==2:
            self.Entry_kalpha[2].insert(0,str(0.5))

    def x_ray_lock(self):
        for j in range(2):
            self.Entry_kalpha[j].config(state='disabled')

    def x_ray_unlock(self):
        for j in range(2):
            self.Entry_kalpha[j].config(state='normal')
