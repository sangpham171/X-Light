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

from XEC.read_data import read_load
from XEC.main_calcul_XEC import main_calcul
from visualisation.pack_Frame import pack_Frame_XEC

class import_load:
    def __init__(self,import_strain,main):
        self.f = askopenfilename(parent=main.root,title="Open file",filetypes=[('*.load','*.LOAD'),('all files','.*')])
        if self.f is not None and self.f is not '':
            self.import_file(main)
            if len(self.load)>0:  
                self.graphic_frame3_2(import_strain,main)
                main.button_run.config(command=lambda:main_calcul(import_strain,self,main))
        pack_Frame_XEC(main,main.Frame3_2,main.Button3_2)
        main.root.mainloop()

    def import_file(self,main):
        self.load=[]
        self.load_number=[]
 
        read_load(self)

    def graphic_frame3_2(self,import_strain,main):
        for widget in main.Frame3_2_1.winfo_children():
            widget.destroy()
        f=plt.figure(1,facecolor="0.94")
        plt.plot(self.load_number,self.load,'-o')
        for i in range(len(self.load)):
            plt.annotate(str(i+1),xy=(self.load_number[i],self.load[i]))
        plt.xlabel("Number")
        plt.ylabel("Load(N)")
        plt.title("Applied load")
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_2_1)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        Label(main.Frame3_2_2,text="Load effective(%)").grid(column=0,row=0)
        self.entry_load_effect=Entry(main.Frame3_2_2)
        self.entry_load_effect.grid(column=1,row=0)
        self.entry_load_effect.insert(0,str(100))
        
        Label(main.Frame3_2_2,text=" ").grid(column=0,row=1)
        
        Label(main.Frame3_2_2,text="Sample thickness(mm)").grid(column=0,row=2)
        self.entry_e=Entry(main.Frame3_2_2)
        self.entry_e.grid(column=1,row=2)

        Label(main.Frame3_2_2,text="Sample width(mm)").grid(column=0,row=3)
        self.entry_b=Entry(main.Frame3_2_2)
        self.entry_b.grid(column=1,row=3)

        Label(main.Frame3_2_2,text="Volume(%)").grid(column=0,row=4)
        self.entry_volume=Entry(main.Frame3_2_2)
        self.entry_volume.grid(column=1,row=4)
        self.entry_volume.insert(0,str(100))

        from XEC.import_strain import import_strain

        main.button_strain.config(command=lambda:import_strain(self,main))
