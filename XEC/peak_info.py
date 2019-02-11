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

from visualisation.pack_Frame import pack_Frame_XEC

def import_peak_info(main):
    f = askopenfilename(parent=main.root,title="Open file",filetypes=[('*.txt','*.txt'),('all files','.*')])
    if f is not None and f is not '':
        f_open = open(f, "r", encoding="utf-8",errors='ignore')
        line_text="0"
        peak="peak="
        point="--------------------------------"
        list_number=[]
        list_peak=[]
        list_peak_width=[]
        list_I_max=[]
        list_peak_error=[]
        list_peak_width_error=[]
        list_I_max_error=[]
        list_2theta=[]
        list_peak_curve=[]
        i=0
        while line_text is not '' and line_text is not None:
            line_text=f_open.readline()
            if peak in line_text:
                i=i+1
                list_number.append(i)
                
                data=line_text.split("=")
                data=data[1].split("+/-")
                list_peak.append(float(data[0]))
                list_peak_error.append(float(data[1]))

                
                line_text=f_open.readline()
                data=line_text.split("=")
                data=data[1].split("+/-")
                list_peak_width.append(float(data[0]))
                list_peak_width_error.append(float(data[1]))
                
                line_text=f_open.readline()
                data=line_text.split("=")
                data=data[1].split("+/-")
                list_I_max.append(float(data[0]))
                list_I_max_error.append(float(data[1]))
                
                line_text=f_open.readline()
                line_text=f_open.readline()
                twotheta=[]
                peak_curve=[]
                line_text=f_open.readline()
                while point not in line_text:
                    data=line_text.split()
                    twotheta.append(float(data[0]))
                    peak_curve.append(float(data[4]))
                    line_text=f_open.readline()
                list_2theta.append(twotheta)
                list_peak_curve.append(peak_curve)

        for widget in main.Frame3_1_1.winfo_children():
            widget.destroy()
        Button(main.Frame3_1_1,text = 'Export graphs',bg="white", command = lambda:export_graphs(list_2theta,list_peak_curve,main)).pack(side=TOP)
        Button(main.Frame3_1_1,text = 'Export data',bg="white", command = lambda:export_data(list_2theta,list_peak_curve,main)).pack(side=TOP)
        Button(main.Frame3_1_1,text = 'Export peak info',bg="white", command = lambda:export_peak_info(list_peak,list_peak_width,list_I_max,list_peak_error,list_peak_width_error,list_I_max_error,main)).pack(side=TOP)
                
        for widget in main.Frame3_1_2.winfo_children():
            widget.destroy()
        
        f=plt.figure(1,facecolor="0.94")
        for i in range(len(list_2theta)):
            plt.plot(list_2theta[i],list_peak_curve[i],label=str(i+1))
        plt.xlabel(r"$2\theta$")
        plt.ylabel("Intensity")
        plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.5,fontsize='x-small')
        plt.subplots_adjust(bottom=0.4)
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_1_2)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        for widget in main.Frame3_1_3.winfo_children():
            widget.destroy()
        
        f=plt.figure(1,facecolor="0.94")
        plt.plot(list_number,list_peak,'o')
        plt.xlabel("Number")
        plt.ylabel("Peak(°)")
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_1_3)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        for widget in main.Frame3_2_1.winfo_children():
            widget.destroy()
        f=plt.figure(1,facecolor="0.94")
        plt.plot(list_number,list_peak_width,'o')
        plt.xlabel("Number")
        plt.ylabel("Peak_width(°)")
        plt.title("Peak width")
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_2_1)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        for widget in main.Frame3_2_2.winfo_children():
            widget.destroy()
        f=plt.figure(1,facecolor="0.94")
        plt.plot(list_number,list_I_max,'o')
        plt.xlabel("Number")
        plt.ylabel("I_max")
        plt.title("I_max")
        plt.close()
        canvas = FigureCanvasTkAgg(f, main.Frame3_2_2)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        pack_Frame_XEC(main,main.Frame3_1,main.Button3_1)
 
        main.root.mainloop()

def export_graphs(list_2theta,list_peak_curve,main):
    name=asksaveasfile(title="Export file",defaultextension=".png",filetypes=[('png files','.png'),('all files','.*')])
    if name is not None and name is not '':
        name=str(name)
        name=list(name)
        del(name[-29:])
        del(name[:25])
        name="".join(name)

        f=plt.figure(figsize=(10,10),dpi=100)
        for i in range(len(list_2theta)):
            plt.plot(list_2theta[i],list_peak_curve[i],label=str(i+1))
        plt.xlabel(r"$2\theta(°)$")
        plt.ylabel("Intensity")
        plt.legend(loc='upper left' , bbox_to_anchor=(-0.1, -0.2, 1.2, 0), ncol=10,mode="expand",borderaxespad=0.5,fontsize='x-small')
        plt.subplots_adjust(bottom=0.4)
        plt.savefig(str(name), bbox_inches="tight")
        plt.close()
    main.root.mainloop()

def export_data(list_2theta,list_peak_curve,main):
    f=asksaveasfile(title="Export file",mode='w',defaultextension=".txt",filetypes=[('.txt','.txt'),('all files','.*')])
    if f is not None and f is not '':
        f.write("2theta      Intensity\n")
        for i in range(len(list_2theta[0])):
            f.write(str(list_2theta[0][i]))
            f.write("   ")
            for j in range(len(list_peak_curve)):
                f.write(str(list_peak_curve[j][i]))
                f.write("   ")
            f.write("\n")
        f.close()
    main.root.mainloop()

def export_peak_info(list_peak,list_peak_width,list_I_max,list_peak_error,list_peak_width_error,list_I_max_error,main):
    f=asksaveasfile(title="Export file",mode='w',defaultextension=".txt",filetypes=[('.txt','.txt'),('all files','.*')])
    if f is not None and f is not '':
        f.write("peak    peak_error    peak_width    peak_width_error    peak_intensity    peak_intensity_error\n")
        for i in range(len(list_peak)):
            f.write(str(list_peak[i]))
            f.write("     ")
            f.write(str(list_peak_error[i]))
            f.write("     ")
            f.write(str(list_peak_width[i]))
            f.write("     ")
            f.write(str(list_peak_width_error[i]))
            f.write("     ")
            f.write(str(list_I_max[i]))
            f.write("     ")
            f.write(str(list_I_max_error[i]))
            f.write("\n")
        f.close()
    main.root.mainloop()
            

