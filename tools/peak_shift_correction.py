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
import numpy as np

def export_peak_shift_correction(twotheta0,val,main):
    f=asksaveasfile(title="Export calibrant coefficient",mode='a',defaultextension=".psc",filetypes=[('*.psc','.psc'),('all files','.*')])
    if f is not None and f is not '':
        f.write("2theta(°)    peak_shift_coefficients(smallest power first)"+"\n")
        f.write(str(twotheta0)+"   ")
        for i in range(len(val)):
            f.write(str(float(val[len(val)-1-i]))+"   ")
        f.write("\n")
        f.close()
    main.root.mainloop()

def import_peak_shift_correction(self,i,main):
    file=askopenfilename(title="Import calibrant coefficient",filetypes=[('*.psc','*.PSC'),('all files','.*')])
    if file is not None and file is not '':
        filename=file.split("/")
        filename=filename[len(filename)-1]
        format_valid=True
        f=open(file,"r")
        line_text=f.readline()
        self.peak_shift_correction_coefficient=[]

        while line_text is not None and line_text is not '':
            line_text=(f.readline()).split()

            data=[]
            for j in range(len(line_text)):
                try:
                    data.append(float(line_text[j]))
                except Exception as e:
                    format_valid=False
                    self.peak_shift_correction_coefficient=[]
                    showinfo(title="Warning",message="Wrong format:"+e)
                    break
            if format_valid==True:
                self.peak_shift_correction_coefficient.append(data)
                line_text=f.readline()
            else:
                break
    
        if format_valid==True:
            if len(self.peak_shift_correction_coefficient)>1:
                for i in range(len(self.peak_shift_correction_coefficient)):
                    if len(self.peak_shift_correction_coefficient[i]) != len(self.peak_shift_correction_coefficient[0]):
                        format_valid==False
                        self.peak_shift_correction_coefficient=[]
                        showinfo(title="Warning",message="Wrong format: Peak shift coefficients don't have the same dimension for all peaks")
                        break
        if format_valid==True:       
            self.Label_sc.config(text=str(filename))
            self.Label_sc.grid(row=i+1,column=1,sticky=W)

            self.Button_delete.config(compound=CENTER,text="Delete",bg="white",command=lambda:delete_peak_shift_correction(self,main))
            self.Button_delete.grid(row=i+2,column=1,sticky=W)
        
    main.root.mainloop()

def delete_peak_shift_correction(self,main):
    self.peak_shift_correction_coefficient=[]
    self.Label_sc.grid_forget()
    self.Button_delete.grid_forget()
    main.root.mainloop()

def fit_peak_shift_correction(v,twotheta0,Entry_degree,data_x,data_y,Frame_1,main):
    try:
        degree=int(Entry_degree.get())
    except ValueError:
        degree=0

    if degree>0:
        poly_cofficient=np.polyfit(data_x,data_y,degree)

        peak_shift_fit=[]
        psi=[]
        for i in range(-90,91,5):
            psi.append(i)
            val=[]
            for j in range(degree+1):
                val.append(poly_cofficient[j]*i**(degree-j))
            peak_shift_fit.append(sum(val))

        text="y="
        for i in range(degree+1):
            if poly_cofficient[i]>=0:
                text=text+"+"+str('%0.2g' % poly_cofficient[i])+"$x^"+str(degree-i)+"$"
            else:
                text=text+str('%0.2g' % poly_cofficient[i])+"$x^"+str(degree-i)+"$"
        fig=plt.figure(facecolor="0.94")
        plt.plot(data_x,data_y,'ro',label='peak shift')
        plt.plot(psi,peak_shift_fit,label='fit')
        if v==2:
            plt.xlabel(u"\u03C8(°)")
        if v==3:
            plt.xlabel(u"\u03C7(°)")
        plt.ylabel("peak shift(%)")
        plt.title(str(text))
        plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2, 1.2, 0),ncol=3,mode="expand",borderaxespad=0.,fontsize='x-small')
        plt.subplots_adjust(bottom=0.3)
        plt.close(fig)

        for widget in Frame_1.winfo_children():
            widget.destroy()
        Button(Frame_1, text = 'Export as image',bg="white", command = lambda:export_fit_as_image(v,data_x,data_y,psi,peak_shift_fit,poly_cofficient,degree,main)).pack(side=BOTTOM)
        Button(Frame_1, text = 'Export peaks correction',bg="white", command = lambda:export_peak_shift_correction(twotheta0,poly_cofficient,main)).pack(side=BOTTOM)
             
        Entry_degree=Entry(Frame_1,width=10)
        Entry_degree.pack(side=BOTTOM)
        Label(Frame_1, text="Polynomial degree").pack(side=BOTTOM)
        Button(Frame_1, text = 'Fit',bg="white", command = lambda:fit_peak_shift_correction(v,twotheta0,Entry_degree,data_x,data_y,Frame_1,main)).pack(side=BOTTOM)
        
        canvas = FigureCanvasTkAgg(fig, master=Frame_1)
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=YES)
    main.root.mainloop()
    
def export_fit_as_image(v,data_x,data_y,psi,peak_shift_fit,poly_cofficient,degree,main):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),('all files','.*')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)
        text="y="
        for i in range(degree+1):
            if poly_cofficient[i]>=0:
                text=text+"+"+str('%0.2g' % poly_cofficient[i])+"$x^"+str(degree-i)+"$"
            else:
                text=text+str('%0.2g' % poly_cofficient[i])+"$x^"+str(degree-i)+"$"
        fig=plt.figure(facecolor="0.94")
        plt.plot(data_x,data_y,'ro',label='peak shift')
        plt.plot(psi,peak_shift_fit,label='fit')
        if v==2:
            plt.xlabel(u"\u03C8(°)",fontsize=20)
        if v==3:
            plt.xlabel(u"\u03C7(°)",fontsize=20)
        plt.ylabel("peak shift(%)",fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.title(str(text),fontsize=20)
        plt.legend(loc='upper left', bbox_to_anchor=(0, -0.4, 1, 0),ncol=2,mode="expand",borderaxespad=0.,fontsize=20)
        plt.subplots_adjust(bottom=0.3)
        plt.savefig(str(name), bbox_inches="tight")
        plt.close(fig)
    main.root.mainloop()
