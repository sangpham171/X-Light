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
from tkinter.messagebox import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import curve_fit

from visualisation.pack_Frame import pack_Frame_XEC

class main_calcul:
    def __init__(self,import_strain,import_load,main):
        valid=True
        try:
            e=float(import_load.entry_e.get())
            b=float(import_load.entry_b.get())
            vf=float(import_load.entry_volume.get())
            load_effect=float(import_load.entry_load_effect.get())
            vf=vf/100
            load_effect=load_effect/100
        except (ValueError,AttributeError):
            showinfo(title="Warning",message="Sample dimensions error")
            valid=False
            pass
        else:
            if len(import_load.load)!=len(import_strain.slope):
                valid=False
                showinfo(title="Warning",message="Strain and load don't have the same dimension")
            elif len(import_load.load)!=len(import_strain.interception):
                valid=False
                showinfo(title="Warning",message="Strain and load don't have the same dimension")
        if valid==True:
            self.load=[]
            for i in range(len(import_load.load)):
                self.load.append(import_load.load[i]*load_effect/(e*b*vf))
                
            def F_linear(x,a,b):
                return a*x+b
            val,cov=curve_fit(F_linear,self.load,import_strain.slope,sigma=import_strain.er_slope)
            self.s2_2=val[0]
            self.er_s2_2=cov[0,0]**0.5
            self.b=val[1]

            self.slope_linear=[]
            for i in range(len(self.load)):
                self.slope_linear.append(val[0]*self.load[i]+val[1])
            
            val,cov=curve_fit(F_linear,self.load,import_strain.interception,sigma=import_strain.er_interception)
            self.s1=val[0]
            self.er_s1=cov[0,0]**0.5
            self.c=val[1]

            self.interception_linear=[]
            for i in range(len(self.load)):
                self.interception_linear.append(val[0]*self.load[i]+val[1])
            
            self.E=1/(self.s1+self.s2_2)*10**-3
            self.er_E=abs(self.er_s1+self.er_s2_2)/((self.s1+self.s2_2)**2)*10**-3
            
            self.v=-self.s1*self.E*10**3
            self.er_v=abs(self.er_s1*self.E*10**3)+abs(self.s1*self.er_E*10**3)
            
            self.graphic3_3_1(import_strain,import_load,main)
            pack_Frame_XEC(main,main.Frame3_3,main.Button3_3)

        main.root.mainloop()

    def graphic3_3_1(self,import_strain,import_load,main):
        for widget in main.Frame3_3_1.winfo_children():
            widget.destroy()
        Label(main.Frame3_3_1,text="E= "+str('%0.1f' % self.E)+u"\u00B1"+str('%0.1f' % self.er_E)+"GPa").pack()
        Label(main.Frame3_3_1,text="v= "+str('%0.2f' % self.v)+u"\u00B1"+str('%0.2f' % self.er_v)).pack()
        Label(main.Frame3_3_1,text="s1= "+str('%0.4g' % self.s1)+u"\u00B1"+str('%0.4g' % self.er_s1)+"MPa-1").pack()
        Label(main.Frame3_3_1,text=u"s\u2082/2= "+str('%0.4g' % self.s2_2)+u"\u00B1"+str('%0.4g' % self.er_s2_2)+"MPa-1").pack()
        
        for widget in main.Frame3_3_2_1.winfo_children():
            widget.destroy()
        Button(main.Frame3_3_2_1,text = 'Export data',bg="white", command = lambda:export_data_slope(self,import_strain,import_load,main)).pack(side=BOTTOM)
        Button(main.Frame3_3_2_1,text = 'Export graph',bg="white", command = lambda:export_slope(self,import_strain,import_load,main)).pack(side=BOTTOM)
        
        f=plt.figure(1,facecolor="0.94")
        plt.plot(self.load,import_strain.slope,'o')
        plt.plot(self.load,self.slope_linear)
        plt.xlabel("Load(MPa)")
        plt.ylabel(r"Slope of strain($sin^{2}\psi$)")
        plt.title("y="+str('%0.4g' % self.s2_2)+"x+"+str('%0.4g' % self.b))
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_3_2_1)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)

        for widget in main.Frame3_3_2_2.winfo_children():
            widget.destroy()
        Button(main.Frame3_3_2_2,text = 'Export data',bg="white", command = lambda:export_data_constant(self,import_strain,import_load,main)).pack(side=BOTTOM)
        Button(main.Frame3_3_2_2,text = 'Export graph',bg="white", command = lambda:export_constant(self,import_strain,import_load,main)).pack(side=BOTTOM)
        f=plt.figure(1,facecolor="0.94")
        plt.plot(self.load,import_strain.interception,'o')
        plt.plot(self.load,self.interception_linear)
        plt.xlabel("Load(MPa)")
        plt.ylabel(r"Interception of ($sin^{2}\psi$)")
        plt.title("y="+str('%0.4g' % self.s1)+"x+"+str('%0.4g' % self.c))
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_3_2_2)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES,side=TOP)
        
def export_slope(self,import_strain,import_load,main):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),('all files','.*')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)

        f=plt.figure(figsize=(10,10),dpi=100)
        plt.plot(import_load.load,import_strain.slope,'o')
        plt.plot(import_load.load,self.slope_linear)
        plt.xlabel("Load(MPa)")
        plt.ylabel(r"Slope of strain($sin^{2}\psi$)")
        plt.title("y="+str('%0.4g' % self.s2_2)+"x+"+str('%0.4g' % self.b))
        plt.savefig(str(name), bbox_inches="tight")
        plt.close()
    main.root.mainloop()
        
def export_constant(self,import_strain,import_load,main):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),('all files','.*')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)

        f=plt.figure(figsize=(10,10),dpi=100)
        plt.plot(import_load.load,import_strain.interception,'o')
        plt.plot(import_load.load,self.interception_linear)
        plt.xlabel("Load(MPa)")
        plt.ylabel(r"Interception of ($sin^{2}\psi$)")
        plt.title("y="+str('%0.4g' % self.s1)+"x+"+str('%0.4g' % self.c))
        plt.savefig(str(name), bbox_inches="tight")
        plt.close()
    main.root.mainloop()

def export_data_slope(self,import_strain,import_load,main):
    f=asksaveasfile(title="Export file",mode='w',defaultextension=".txt",filetypes=[('.txt','.txt'),('all files','.*')])
    if f is not None and f is not '':
        f.write("Load      slope     linear_fit\n")
        for i in range(len(import_load.load)):
            f.write(str(import_load.load[i]))
            f.write("     ")
            f.write(str(import_strain.slope[i]))
            f.write("     ")
            f.write(str(self.slope_linear[i]))
            f.write("\n")
        f.close()
    main.root.mainloop()
        
def export_data_constant(self,import_strain,import_load,main):
    f=asksaveasfile(title="Export file",mode='w',defaultextension=".txt",filetypes=[('.txt','.txt'),('all files','.*')])
    if f is not None and f is not '':
        f.write("Load      Interception       linear_fit\n")
        for i in range(len(import_load.load)):
            f.write(str(import_load.load[i]))
            f.write("     ")
            f.write(str(import_strain.interception[i]))
            f.write("     ")
            f.write(str(self.interception_linear[i]))
            f.write("\n")
        f.close()
    main.root.mainloop()
