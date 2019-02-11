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
from tkinter.filedialog import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math as math

from XEC.read_data import read_strain
from XEC.main_calcul_XEC import main_calcul
from visualisation.pack_Frame import pack_Frame_XEC

class import_strain:
    def __init__(self,import_load,main):
        namefile = askopenfilenames(parent=main.root,title="Open file",filetypes=[('*.ssd','*.SSD'),('all files','.*')])
        self.list_filename = main.root.tk.splitlist(namefile)
        if len(self.list_filename)>0:
            self.import_file(main)
            if len(self.strain)>0:  
                self.graphic_frame3_1(import_load,main)
                main.button_run.config(command=lambda:main_calcul(self,import_load,main)) 
        pack_Frame_XEC(main,main.Frame3_1,main.Button3_1)
        main.root.mainloop()

    def import_file(self,main):
        self.strain=[]
        self.sin2psi=[]
        self.slope=[]
        self.er_slope=[]
        self.interception=[]
        self.er_interception=[]
        self.filename=[]
        for i in range(len(self.list_filename)):
            f_split=self.list_filename[i].split("/")
            filename=f_split[len(f_split)-1]
            self.filename.append(filename)
            read_strain(self.list_filename[i],filename,self)

    def graphic_frame3_1(self,import_load,main):
        for widget in main.Frame3_1_1.winfo_children():
            widget.destroy()
        scrollbar3_1_1 = Scrollbar(main.Frame3_1_1)
        scrollbar3_1_1.pack( side = RIGHT, fill=BOTH) 
        mylist3_1_1 = Listbox(main.Frame3_1_1, yscrollcommand = scrollbar3_1_1.set)
        mylist3_1_1.insert(END, "0-All strain graph")
        for i in range(len(self.strain)):
            mylist3_1_1.insert(END, str(i+1)+"-"+str(self.filename[i]))
        mylist3_1_1.pack( side = LEFT, fill=BOTH,expand=YES)
        mylist3_1_1.bind("<ButtonRelease-1>", lambda event: show_strain_graph(event,self,main))
        scrollbar3_1_1.config( command = mylist3_1_1.yview )   

        for widget in main.Frame3_1_2.winfo_children():
            widget.destroy()
        self.i_graph=0
        Button(main.Frame3_1_2,text = 'Export without fit',bg="white", command = lambda:export_strain_without_fit(self,main)).pack(side=BOTTOM)
        Button(main.Frame3_1_2,text = 'Export with fit',bg="white", command = lambda:export_strain_with_fit(self,main)).pack(side=BOTTOM)
        Button(main.Frame3_1_2,text = 'Export data',bg="white", command = lambda:export_data(self,main)).pack(side=BOTTOM)

        
        f=plt.figure(1,facecolor="0.94")
        for i in range(len(self.strain)):
            plt.plot(self.sin2psi[i],self.strain[i],'o',label=str(i+1))
        plt.xlabel(r"$sin^{2}\psi$")
        plt.ylabel("Strain")
        plt.title("Strain - "+r"$sin^{2}\psi$")
        plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.5,fontsize='x-small')
        plt.subplots_adjust(bottom=0.4)
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_1_2)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)

        for widget in main.Frame3_1_3.winfo_children():
            widget.destroy()
        Button(main.Frame3_1_3,text = 'Export fit',bg="white", command = lambda:export_fit(self,main)).pack(side=BOTTOM)
        
        self.sin2psi_fit=[]
        for i in range(0,90,5):
            self.sin2psi_fit.append((math.sin(math.radians(i)))**2)

        self.matrix_strain=[]
        for i in range(len(self.slope)):
            strain=[]
            for j in range(len(self.sin2psi_fit)):
                strain.append(self.slope[i]*self.sin2psi_fit[j]+self.interception[i])
            self.matrix_strain.append(strain)
            
        f=plt.figure(1,facecolor="0.94")
        for i in range(len(self.slope)):
            plt.plot(self.sin2psi_fit,self.matrix_strain[i],label="fit "+str(i+1))
        plt.xlabel(r"$sin^{2}\psi$")
        plt.ylabel("Strain")
        plt.title("Strain - "+r"$sin^{2}\psi$")
        plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.,fontsize='x-small')
        plt.subplots_adjust(bottom=0.4)
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_1_3)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)

        from XEC.import_load import import_load        

        main.button_load.config(command=lambda:import_load(self,main))
              
def show_strain_graph(event,self,main):
    widget = event.widget
    selection=widget.curselection()
    selection = widget.get(selection)
    selection=selection.split("-")
    self.i_graph=int(selection[0])

    for widget in main.Frame3_1_2.winfo_children():
        widget.destroy()
    Button(main.Frame3_1_2,text = 'Export without fit',bg="white", command = lambda:export_strain_without_fit(self,main)).pack(side=BOTTOM)
    Button(main.Frame3_1_2,text = 'Export with fit',bg="white", command = lambda:export_strain_with_fit(self,main)).pack(side=BOTTOM)
    Button(main.Frame3_1_2,text = 'Export data',bg="white", command = lambda:export_data(self,main)).pack(side=BOTTOM)
    
    if self.i_graph==0:
        f=plt.figure(1,facecolor="0.94")
        for i in range(len(self.strain)):
            plt.plot(self.sin2psi[i],self.strain[i],'o',label=str(i+1))
        plt.xlabel(r"$sin^{2}\psi$")
        plt.ylabel("Strain")
        plt.title("Strain - "+r"$sin^{2}\psi$")
        plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.5,fontsize='x-small')
        plt.subplots_adjust(bottom=0.4)
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_1_2)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)
    else:            
        f=plt.figure(1,facecolor="0.94")
        plt.plot(self.sin2psi[self.i_graph-1],self.strain[self.i_graph-1],'o',label="data")
        plt.plot(self.sin2psi_fit,self.matrix_strain[self.i_graph-1],label="linear fit")
        plt.xlabel(r"$sin^{2}\psi$")
        plt.ylabel("Strain")
        plt.title("Load "+str(self.i_graph+1))
        plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.5,fontsize='x-small')
        plt.subplots_adjust(bottom=0.4)
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_1_2)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)
    main.root.mainloop()    
        
def export_strain_without_fit(self,main):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),('all files','.*')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)
        if self.i_graph==0:
            f=plt.figure(figsize=(10,10),dpi=100)
            for i in range(len(self.strain)):
                plt.plot(self.sin2psi[i],self.strain[i],'o',label=str(i+1))
            plt.xlabel(r"$sin^{2}\psi$")
            plt.ylabel("Strain")
            plt.title("Strain - "+r"$sin^{2}\psi$")
            plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.5,fontsize='x-small')
            plt.subplots_adjust(bottom=0.4)
            plt.savefig(str(name), bbox_inches="tight")
            plt.close()
        else:
            f=plt.figure(figsize=(10,10),dpi=100)
            plt.plot(self.sin2psi[self.i_graph],self.strain[self.i_graph],'o',label=str(self.i_graph+1))
            plt.xlabel(r"$sin^{2}\psi$")
            plt.ylabel("Strain")
            plt.title("Strain - "+r"$sin^{2}\psi$")
            plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.5,fontsize='x-small')
            plt.subplots_adjust(bottom=0.4)
            plt.savefig(str(name), bbox_inches="tight")
            plt.close()
    main.root.mainloop()

def export_strain_with_fit(self,main):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),('all files','.*')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)
        if self.i_graph==0:
            f=plt.figure(figsize=(10,10),dpi=100)
            for i in range(len(self.strain)):
                plt.plot(self.sin2psi[i],self.strain[i],'o',label=str(i+1))
                plt.plot(self.sin2psi_fit,self.matrix_strain[i],label="fit "+str(i+1))
            plt.xlabel(r"$sin^{2}\psi$")
            plt.ylabel("Strain")
            plt.title("Strain - "+r"$sin^{2}\psi$")
            plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.5,fontsize='x-small')
            plt.subplots_adjust(bottom=0.4)
            plt.savefig(str(name), bbox_inches="tight")
            plt.close()
        else:
            f=plt.figure(figsize=(10,10),dpi=100)
            plt.plot(self.sin2psi[self.i_graph],self.strain[self.i_graph],'o',label=str(self.i_graph+1))
            plt.plot(self.sin2psi_fit,self.matrix_strain[self.i_graph],label="fit"+str(self.i_graph+1))
            plt.xlabel(r"$sin^{2}\psi$")
            plt.ylabel("Strain")
            plt.title("Strain - "+r"$sin^{2}\psi$")
            plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.5,fontsize='x-small')
            plt.subplots_adjust(bottom=0.4)
            plt.savefig(str(name), bbox_inches="tight")
            plt.close()
    main.root.mainloop()

def export_fit(self,main):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),('all files','.*')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)

        f=plt.figure(figsize=(10,10),dpi=100)
        for i in range(len(self.strain)):
            plt.plot(self.sin2psi_fit,self.matrix_strain[i],label="fit"+str(i+1))
        plt.xlabel(r"$sin^{2}\psi$")
        plt.ylabel("Strain")
        plt.title("Strain - "+r"$sin^{2}\psi$")
        plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.5,fontsize='x-small')
        plt.subplots_adjust(bottom=0.4)
        plt.savefig(str(name), bbox_inches="tight")
        plt.close()
    main.root.mainloop() 

def export_data(self,main):
    f=asksaveasfile(title="Export file",mode='w',defaultextension=".txt",filetypes=[('.txt','.txt'),('all files','.*')])
    if f is not None and f is not '':
        f.write("Slope    error     Interception    error\n")
        for i in range(len(self.slope)):
            f.write(str(self.slope[i]))
            f.write('   ')
            f.write(str(self.er_slope[i]))
            f.write('   ')
            f.write(str(self.interception[i]))
            f.write('   ')
            f.write(str(self.er_interception[i]))
            f.write('   ')
            f.write('\n')
        f.close()
    main.root.mainloop()
    
