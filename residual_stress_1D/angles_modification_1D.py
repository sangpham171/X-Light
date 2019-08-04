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
    def init(self,import_XRD,main):
        import_XRD.angles_modif_valid=False

        import_XRD.Entry_phi_offset.delete(0,END)
        import_XRD.Entry_chi_offset.delete(0,END)
        import_XRD.Entry_twotheta_offset.delete(0,END)
        import_XRD.Entry_omega_offset.delete(0,END)
        import_XRD.Entry_phi_offset.insert(0,"0")
        import_XRD.Entry_chi_offset.insert(0,"0")
        import_XRD.Entry_twotheta_offset.insert(0,"0")
        import_XRD.Entry_omega_offset.insert(0,"0")
                
    #main.Frame3_2_1
        for widget in main.Frame3_2_1.winfo_children():
            widget.destroy()

        scrollbar = Scrollbar(main.Frame3_2_1)
        scrollbar.pack( side = RIGHT, fill=Y) 
        mylist = Listbox(main.Frame3_2_1, yscrollcommand = scrollbar.set,width=50)
        for i in range(len(import_XRD.phi)):
            mylist.insert(END, str(i+1)+u".\u03C6="+str(float(import_XRD.phi[i]))+u"; \u03C7="+str(float(import_XRD.chi[i]))+u"; \u03C9="+str(float(import_XRD.omega[i])))
        mylist.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command = mylist.yview )

        for widget in main.Frame3_2_3.winfo_children():
            widget.destroy()
        f=plt.figure(1,facecolor="0.94")
        for i in range(len(self.phi)):
            plt.plot(import_XRD.data_x[i],import_XRD.data_y[i],label=""+str(i+1))
        plt.xlabel(r"$2\theta$")
        plt.ylabel("Intensity")
        plt.title("All original graph")
        plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.,fontsize='x-small')
        plt.subplots_adjust(bottom=0.4)
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_2_3)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        for widget in main.Frame3_3_4.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(f, main.Frame3_3_4)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
           
        main.root.mainloop()
#------------------------------------------------------------------------------ 
    def apply(self,import_XRD,main):
        try:
            phi_offset=float(import_XRD.Entry_phi_offset.get())
            chi_offset=float(import_XRD.Entry_chi_offset.get())
            omega_offset=float(import_XRD.Entry_omega_offset.get())
            twotheta_offset=float(import_XRD.Entry_twotheta_offset.get())
        except ValueError:
            showinfo(title="Error",message="Please insert and verify that phi reference is a number\nPlease use '.' instead of ',' to insert a number")
        else:
            import_XRD.angles_modif_valid=True
            if float(import_XRD.chi_invert.get())==1:
                chi_invert=-1
            else:
                chi_invert=1

            if float(import_XRD.phi_invert.get())==1:
                phi_invert=-1
            else:
                phi_invert=1

            self.phi=list((np.array(import_XRD.phi)-phi_offset)*phi_invert)
            self.chi=list((np.array(import_XRD.chi)-chi_offset)*chi_invert)
            self.twotheta=list(np.array(import_XRD.twotheta)-twotheta_offset)
            self.omega=list(np.array(import_XRD.omega)-omega_offset)

            self.data_x=[]
            for i in range(len(import_XRD.data_x)):
                data_x=list(np.array(import_XRD.data_x[i])-twotheta_offset)
                self.data_x.append(data_x)

    #main.Frame3_2_1
            for widget in main.Frame3_2_1.winfo_children():
                widget.destroy()

            scrollbar = Scrollbar(main.Frame3_2_1)
            scrollbar.pack( side = RIGHT, fill=Y) 
            mylist = Listbox(main.Frame3_2_1, yscrollcommand = scrollbar.set,width=50)
            for i in range(len(self.phi)):
                mylist.insert(END, str(i+1)+u".\u03C6="+str(float(self.phi[i]))+u"; \u03C7="+str(float(self.chi[i]))+u"; \u03C9="+str(float(self.omega[i])))

            mylist.pack( side = LEFT, fill = BOTH )
            scrollbar.config( command = mylist.yview )

            for widget in main.Frame3_2_3.winfo_children():
                widget.destroy()
            f=plt.figure(1,facecolor="0.94")
            for i in range(len(self.phi)):
                plt.plot(self.data_x[i],import_XRD.data_y[i],label=""+str(i+1)+"")
            plt.xlabel(r"$2\theta$")
            plt.ylabel("Intensity")
            plt.title("All original graph")
            plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.,fontsize='x-small')
            plt.subplots_adjust(bottom=0.4)
            plt.close()
            canvas = FigureCanvasTkAgg(f, main.Frame3_2_3)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

            for widget in main.Frame3_3_4.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(f, main.Frame3_3_4)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
        
        main.root.mainloop()
    
    def advance(self,import_XRD,main):
        import_XRD.button_import_gma.grid(row=0,column=0,sticky=W)
        
        f=font.Font(size=9,underline=1)
        #self.Button_import_gma=Button(main.Frame3_2_2_2,compound=CENTER, text="Import from file",bg="white",command=lambda:self.import_goniometric_angles(self,import_XRD,main))
        #self.Button_import_gma.grid(row=0,column=0,sticky=W)
##      Button(main.Frame3_2_2_2,compound=CENTER, text="Hide",bg="white",command=lambda:self.hide(self,main)).grid(row=0,column=1,sticky=W)
        
        Label(main.Frame3_2_2_3, text="GONIO CONFIG",font=f).grid(row=1,column=0,sticky=W)
        #self.gonio_config = IntVar()
        Radiobutton(main.Frame3_2_2_3, text=u"CHI \u03C7", variable=import_XRD.gonio_config, value=1).grid(row=1,column=1,sticky=W)
        Radiobutton(main.Frame3_2_2_3, text=u"OMEGA \u03C9", variable=import_XRD.gonio_config, value=2).grid(row=2,column=1,sticky=W)
        import_XRD.gonio_config.set(1)

        import_XRD.button_next_gma.grid(row=0,column=0,sticky=W)
        main.root.mainloop()

    def next_step(self,import_XRD,main):
        for widget in main.Frame3_2_2_5.winfo_children():
            widget.destroy()
            
        f=font.Font(size=9,underline=1)
        if import_XRD.gonio_config.get()==1:
            Label(main.Frame3_2_2_5, text="SCAN MODE",font=f).grid(row=0,column=0,sticky=W)
            self.scan_mode = IntVar()
            Radiobutton(main.Frame3_2_2_5, text=u"Chi \u03C7", variable=self.scan_mode, value=1).grid(row=0,column=1,sticky=W)
            Radiobutton(main.Frame3_2_2_5, text=u"Phi \u03C6", variable=self.scan_mode, value=2).grid(row=1,column=1,sticky=W)
            self.scan_mode.set(1)

            Label(main.Frame3_2_2_5, text="2\u03B8 start").grid(row=2,column=0,sticky=W)
            self.Entry_2theta_start= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_2theta_start.grid(row=2, column=1,sticky=W)

            Label(main.Frame3_2_2_5, text="2\u03B8 end").grid(row=2,column=2,sticky=W)
            self.Entry_2theta_end= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_2theta_end.grid(row=2, column=3,sticky=W)

            Label(main.Frame3_2_2_5, text="\u03C9").grid(row=3,column=0,sticky=W)
            self.Entry_omega= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_omega.grid(row=3, column=1,sticky=W)

            Label(main.Frame3_2_2_5, text=u"\u03C6 start").grid(row=4,column=0,sticky=W)
            self.Entry_phi_start= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_phi_start.grid(row=4, column=1,sticky=W)

            Label(main.Frame3_2_2_5, text=u"\u03C6 end").grid(row=4,column=2,sticky=W)
            self.Entry_phi_end= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_phi_end.grid(row=4, column=3,sticky=W)

            Label(main.Frame3_2_2_5, text=u"Number \u03C6").grid(row=5,column=0,sticky=W)
            self.Entry_phi_number= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_phi_number.grid(row=5, column=1,sticky=W)

            Label(main.Frame3_2_2_5, text=u"\u03C7 start").grid(row=6,column=0,sticky=W)
            self.Entry_chi_start= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_chi_start.grid(row=6, column=1,sticky=W)

            Label(main.Frame3_2_2_5, text=u"\u03C7 end").grid(row=6,column=2,sticky=W)
            self.Entry_chi_end= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_chi_end.grid(row=6, column=3,sticky=W)

            Label(main.Frame3_2_2_5, text=u"Number \u03C7").grid(row=7,column=0,sticky=W)
            self.Entry_chi_number= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_chi_number.grid(row=7, column=1,sticky=W)

            import_XRD.button_apply_gma.config(command=lambda:self.apply_advance_1(self,import_XRD,main))
            import_XRD.button_apply_gma.grid(row=0,column=1,sticky=W)

        elif import_XRD.gonio_config.get()==2:
            Label(main.Frame3_2_2_5, text="SCAN MODE",font=f).grid(row=0,column=0,sticky=W)
            self.scan_mode = IntVar()
            Radiobutton(main.Frame3_2_2_5, text=u"Omega \u03C9", variable=self.scan_mode, value=1).grid(row=0,column=1,sticky=W)
            Radiobutton(main.Frame3_2_2_5, text=u"Phi \u03C6", variable=self.scan_mode, value=2).grid(row=1,column=1,sticky=W)
            self.scan_mode.set(1)

            Label(main.Frame3_2_2_5, text="2\u03B8 start").grid(row=2,column=0,sticky=W)
            self.Entry_2theta_start= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_2theta_start.grid(row=2, column=1,sticky=W)

            Label(main.Frame3_2_2_5, text="2\u03B8 end").grid(row=2,column=2,sticky=W)
            self.Entry_2theta_end= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_2theta_end.grid(row=2, column=3,sticky=W)

            Label(main.Frame3_2_2_5, text="\u03C7").grid(row=3,column=0,sticky=W)
            self.Entry_chi= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_chi.grid(row=3, column=1,sticky=W)

            Label(main.Frame3_2_2_5, text=u"\u03C6 start").grid(row=4,column=0,sticky=W)
            self.Entry_phi_start= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_phi_start.grid(row=4, column=1,sticky=W)

            Label(main.Frame3_2_2_5, text=u"\u03C6 end").grid(row=4,column=2,sticky=W)
            self.Entry_phi_end= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_phi_end.grid(row=4, column=3,sticky=W)

            Label(main.Frame3_2_2_5, text=u"Number \u03C6").grid(row=5,column=0,sticky=W)
            self.Entry_phi_number= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_phi_number.grid(row=5, column=1,sticky=W)

            Label(main.Frame3_2_2_5, text=u"\u03C9 start").grid(row=6,column=0,sticky=W)
            self.Entry_omega_start= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_omega_start.grid(row=6, column=1,sticky=W)

            Label(main.Frame3_2_2_5, text=u"\u03C9 end").grid(row=6,column=2,sticky=W)
            self.Entry_omega_end= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_omega_end.grid(row=6, column=3,sticky=W)

            Label(main.Frame3_2_2_5, text=u"Number \u03C9").grid(row=7,column=0,sticky=W)
            self.Entry_omega_number= Entry(main.Frame3_2_2_5,width=10)
            self.Entry_omega_number.grid(row=7, column=1,sticky=W)
            
            import_XRD.button_apply_gma.config(command=lambda:self.apply_advance_2(self,import_XRD,main))
            import_XRD.button_apply_gma.grid(row=0,column=1,sticky=W)
        
        main.root.mainloop()
            
    def hide(self,main):
        for widget in main.Frame3_2_2_2.winfo_children():
            widget.destroy()
        main.root.mainloop()

    def apply_advance_1(self,import_XRD,main):
        try:
            twotheta_start=float(self.Entry_2theta_start.get())
            twotheta_end=float(self.Entry_2theta_end.get())
            omega=float(self.Entry_omega.get())
            phi_start=float(self.Entry_phi_start.get())
            phi_end=float(self.Entry_phi_end.get())
            phi_number=int(self.Entry_phi_number.get())
            chi_start=float(self.Entry_chi_start.get())
            chi_end=float(self.Entry_chi_end.get())
            chi_number=int(self.Entry_chi_number.get())
        except ValueError:
            showinfo(title="Error",message="Please verify all values are numbers\nPlease use '.' instead of ',' to insert a number")
        else:
            import_XRD.angles_modif_valid=True
            
            if (phi_number-1)>=1:
                phi_step=(phi_end-phi_start)/(phi_number-1)
            else:
                phi_step=0
            if (chi_number-1)>=1:
                chi_step=(chi_end-chi_start)/(chi_number-1)
            else:
                chi_step=0
                
            twotheta_step=(twotheta_end-twotheta_start)/len(import_XRD.data_x[0])

            self.twotheta=[twotheta_start]*len(import_XRD.phi)
            self.omega=[omega]*len(import_XRD.phi)
            
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

            data_x=[]
            for i in range(len(import_XRD.data_x[0])):
                data_x.append(twotheta_start+i*twotheta_step)

            self.data_x=[]
            for i in range(len(import_XRD.data_x)):
                self.data_x.append(data_x)

            for widget in main.Frame3_2_1.winfo_children():
                widget.destroy()

            scrollbar = Scrollbar(main.Frame3_2_1)
            scrollbar.pack( side = RIGHT, fill=Y) 
            mylist = Listbox(main.Frame3_2_1, yscrollcommand = scrollbar.set,width=50)
            for i in range(len(self.phi)):
                mylist.insert(END, str(i+1)+u".\u03C6="+str(float(self.phi[i]))+u"; \u03C7="+str(float(self.chi[i]))+u"; \u03C9="+str(float(self.omega[i])))

            mylist.pack( side = LEFT, fill = BOTH )
            scrollbar.config( command = mylist.yview )

            for widget in main.Frame3_2_3.winfo_children():
                widget.destroy()
            f=plt.figure(1,facecolor="0.94")
            for i in range(len(self.phi)):
                plt.plot(self.data_x[i],import_XRD.data_y[i],label=str(i+1))
            plt.xlabel(r"$2\theta$")
            plt.ylabel("Intensity")
            plt.title("All original graph")
            plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.,fontsize='x-small')
            plt.subplots_adjust(bottom=0.4)
            plt.close()
            canvas = FigureCanvasTkAgg(f, main.Frame3_2_3)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

            for widget in main.Frame3_3_4.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(f, main.Frame3_3_4)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
                
        main.root.mainloop()

    def apply_advance_2(self,import_XRD,main):
        try:
            twotheta_start=float(self.Entry_2theta_start.get())
            twotheta_end=float(self.Entry_2theta_end.get())
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
            import_XRD.angles_modif_valid=True
            if (phi_number-1)>=1:
                phi_step=(phi_end-phi_start)/(phi_number-1)
            else:
                phi_step=0
                
            if (omega_number-1)>=1:
                omega_step=(omega_end-omega_start)/(omega_number-1)
            else:
                omega_step=0

            twotheta_step=(twotheta_end-twotheta_start)/len(import_XRD.data_x[0])

            self.twotheta=[twotheta_start]*len(import_XRD.phi)
            self.chi=[chi]*len(import_XRD.phi)
            
            self.phi=[]
            self.omega=[]
            if self.scan_mode.get()==1:
                for i in range(phi_number):
                    for j in range(omega_number):
                        self.phi.append(phi_start+i*phi_step)
                        self.omega.append(omega_start+j*omega_step)
            if self.scan_mode.get()==2:
                for i in range(omega_number):
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

            data_x=[]
            for i in range(len(import_XRD.data_x[0])):
                data_x.append(twotheta_start+i*twotheta_step)

            self.data_x=[]
            for i in range(len(import_XRD.data_x)):
                self.data_x.append(data_x)

            for widget in main.Frame3_2_1.winfo_children():
                widget.destroy()

            scrollbar = Scrollbar(main.Frame3_2_1)
            scrollbar.pack( side = RIGHT, fill=Y) 
            mylist = Listbox(main.Frame3_2_1, yscrollcommand = scrollbar.set,width=50)
            for i in range(len(self.phi)):
                mylist.insert(END, str(i+1)+u".\u03C6="+str(float(self.phi[i]))+u"; \u03C7="+str(float(self.chi[i]))+u"; \u03C9="+str(float(self.omega[i])))

            mylist.pack( side = LEFT, fill = BOTH )
            scrollbar.config( command = mylist.yview )

            for widget in main.Frame3_2_3.winfo_children():
                widget.destroy()
            f=plt.figure(1,facecolor="0.94")
            for i in range(len(self.phi)):
                plt.plot(self.data_x[i],import_XRD.data_y[i],label=str(i+1))
            plt.xlabel(r"$2\theta$")
            plt.ylabel("Intensity")
            plt.title("All original graph")
            plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.,fontsize='x-small')
            plt.subplots_adjust(bottom=0.4)
            plt.close()
            canvas = FigureCanvasTkAgg(f, main.Frame3_2_3)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

            for widget in main.Frame3_3_4.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(f, main.Frame3_3_4)
            canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        main.root.mainloop()

    def import_goniometric_angles(self,import_XRD,main):
        f = askopenfilename(parent=main.root,title="Open file",filetypes=[('file type','*.gma;*.GMA'),('all files','.*')])
        if f is not None and f is not '':
            try:
                f_open=open(f,"r")
                line_text=f_open.readline() #Phi Chi Omega 2theta
                
                self.phi=[]
                self.chi=[]
                self.twotheta=[]
                self.omega=[]
                line_text=f_open.readline()
                while line_text is not None and line_text is not '' and len(self.phi)<len(import_XRD.phi):
                    angles=line_text.split()
                    try:
                        self.phi.append(float(angles[1]))
                        self.chi.append(float(angles[2]))
                        self.omega.append(float(angles[3]))
                        self.twotheta.append(float(angles[4]))
                    except Exception:
                        showinfo(title="Warning",message="Invalid format")
                        return
                        
                    line_text=f_open.readline()

                if len(self.phi)<len(import_XRD.phi):
                    for i in range(len(import_XRD.phi)-len(self.phi)):
                        self.phi.append(float('NaN'))
                        self.chi.append(float('NaN'))
                        self.omega.append(float('NaN'))
                        self.twotheta.append(float('NaN'))

                twotheta_shift=self.twotheta[0]-import_XRD.twotheta[0]
                data_x=[]
                for i in range(len(import_XRD.data_x[0])):
                    data_x.append(import_XRD.data_x[0][i]+twotheta_shift)

                self.data_x=[]
                for i in range(len(import_XRD.data_x)):
                    self.data_x.append(data_x)

                for widget in main.Frame3_2_1.winfo_children():
                    widget.destroy()

                scrollbar = Scrollbar(main.Frame3_2_1)
                scrollbar.pack( side = RIGHT, fill=Y) 
                mylist = Listbox(main.Frame3_2_1, yscrollcommand = scrollbar.set,width=50)
                for i in range(len(self.phi)):
                    mylist.insert(END, str(i+1)+u".\u03C6="+str(float(self.phi[i]))+u"; \u03C7="+str(float(self.chi[i]))+u"; \u03C9="+str(float(self.omega[i])))

                mylist.pack( side = LEFT, fill = BOTH )
                scrollbar.config( command = mylist.yview )

                for widget in main.Frame3_2_3.winfo_children():
                    widget.destroy()
                f=plt.figure(1,facecolor="0.94")
                for i in range(len(self.phi)):
                    plt.plot(self.data_x[i],import_XRD.data_y[i],label=str(i+1))
                plt.xlabel(r"$2\theta$")
                plt.ylabel("Intensity")
                plt.title("All original graph")
                plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.,fontsize='x-small')
                plt.subplots_adjust(bottom=0.4)
                plt.close()
                canvas = FigureCanvasTkAgg(f, main.Frame3_2_3)
                canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

                for widget in main.Frame3_3_4.winfo_children():
                    widget.destroy()
                canvas = FigureCanvasTkAgg(f, main.Frame3_3_4)
                canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
            except Exception as e:
                showinfo(title="Error",message="Uncorrected file format")
            else:
                import_XRD.angles_modif_valid=True

        main.root.mainloop()
                
        
