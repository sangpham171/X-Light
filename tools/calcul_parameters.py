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
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import *
def export_calcul_parameters(self,main):
    f=asksaveasfile(title="Export parameters calcul",mode='w',defaultextension=".spt",filetypes=[('*.spt','.spt'),('all files','.*')])
    if f is not None and f is not '':
        f.write("Material properties\n")
        f.write("Unstressed peak ="+str(self.Entry_twotheta0.get())+"\n")
        f.write("s1="+str(self.Entry_s1.get())+"\n")
        f.write("s2/2="+str(self.Entry_half_s2.get())+"\n")
        f.write("Young="+str(self.Entry_Young.get())+"\n")
        f.write("Poisson="+str(self.Entry_Poisson.get())+"\n")
        f.write("\n")

        f.write("X-ray properties\n")
        f.write("kalpha 1="+str(self.Entry_kalpha[0].get())+"\n")
        f.write("kalpha 2="+str(self.Entry_kalpha[1].get())+"\n")
        f.write("kalpha ratio="+str(self.Entry_kalpha[2].get())+"\n")
        f.write("\n")
        
        f.write("Fitting range\n")
        f.write("twotheta from="+str(self.Entry_twotheta_from.get())+"\n")
        f.write("twotheta to="+str(self.Entry_twotheta_to.get())+"\n")
        try:
            f.write("gamma from="+str(self.Entry_gamma_from.get())+"\n")
            f.write("gamma to="+str(self.Entry_gamma_to.get())+"\n")
            f.write("gamma number step="+str(self.Entry_gamma_number.get())+"\n")
        except AttributeError:
            pass
        f.write("function fit="+str(self.function_fit.get())+"\n")
        f.write("peak_shape="+str(self.peak_shape.get())+"\n")
        f.write("\n")
        
        f.write("Background range\n")
        background_f=((self.Entry_background_from.get()).rstrip(',')).split(',')
        background_t=((self.Entry_background_to.get()).rstrip(',')).split(',')
        for i in range(len(background_f)):
            f.write("range "+str(i+1)+" from="+str(background_f[i])+"\n")
            f.write("range "+str(i+1)+" to="+str(background_t[i])+"\n")
        f.write("\n")
        
        f.write("background polynomial fit degrees="+str(self.Entry_background_polynominal_degrees.get())+"\n")
        f.write("correlation ratio="+str(self.Entry_r.get())+"\n")
        f.write("init guess="+str(self.init_guess.get())+"\n")
        f.write("\n")
        
        f.write("Peaks list\n")
        f.write("Peak 1="+str(self.Entry_peak[0].get())+"\n")
        f.write("Limit peak 1="+str(self.Entry_limit_peak[0].get())+"\n")
        f.write("FWHM 1="+str(self.Entry_peak_width[0].get())+"\n")
        f.write("\n")
        
        if len(self.Entry_peak)==2:
            peak=((self.Entry_peak[1].get()).rstrip(',')).split(',')
            limit_peak=((self.Entry_limit_peak[1].get()).rstrip(',')).split(',')
            peak_width=((self.Entry_peak_width[1].get()).rstrip(',')).split(',')

            for i in range(len(peak)):
                f.write("Peak"+str(i+2)+"="+str(peak[i])+"\n")
                try:
                    f.write("Limit peak"+str(i+2)+"="+str(limit_peak[i])+"\n")
                except IndexError:
                    f.write("Limit peak"+str(i+2)+"= \n")
                try:
                    f.write("FWHM"+str(i+2)+"="+str(peak_width[i])+"\n")
                except IndexError:
                    f.write("FWHM"+str(i+2)+"= \n")
            f.write("\n")
        f.close()
        main.root.mainloop()

def import_calcul_parameters(self,main):
    file=askopenfilename(title="Import parameters calcul",filetypes=[('*.spt','*.SPT'),('all files','.*')])
    if file is not None and file is not '':
        f=open(file,"r")
        try:
            line_text=f.readline()

            line_text=f.readline()
            self.Entry_twotheta0.delete(0,END)
            self.Entry_twotheta0.insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            self.Entry_s1.delete(0,END)
            self.Entry_s1.insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            self.Entry_half_s2.delete(0,END)
            self.Entry_half_s2.insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            self.Entry_Young.delete(0,END)
            self.Entry_Young.insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            self.Entry_Poisson.delete(0,END)
            self.Entry_Poisson.insert(0,str(line_text.split('=')[1]).rstrip())

            f.readline()
            f.readline()

            line_text=f.readline()
            self.Entry_kalpha[0].delete(0,END)
            self.Entry_kalpha[0].insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            self.Entry_kalpha[1].delete(0,END)
            self.Entry_kalpha[1].insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            self.Entry_kalpha[2].delete(0,END)
            self.Entry_kalpha[2].insert(0,str(line_text.split('=')[1]).rstrip())

            f.readline()
            f.readline()
            
            line_text=f.readline()
            self.Entry_twotheta_from.delete(0,END)
            self.Entry_twotheta_from.insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            self.Entry_twotheta_to.delete(0,END)
            self.Entry_twotheta_to.insert(0,str(line_text.split('=')[1]).rstrip())

            try:
                self.Entry_gamma_from.delete(0,END)
            except AttributeError:
                pass
            else:
                line_text=f.readline()
                if "gamma" not in line_text.split('=')[0]:
                    showinfo(title="Warning",message='Format is not corrected')
                    f.close()
                    return
                
                self.Entry_gamma_from.insert(0,str(line_text.split('=')[1]).rstrip())

                line_text=f.readline()
                self.Entry_gamma_to.delete(0,END)
                self.Entry_gamma_to.insert(0,str(line_text.split('=')[1]).rstrip())

                line_text=f.readline()
                self.Entry_gamma_number.delete(0,END)
                self.Entry_gamma_number.insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            if "gamma" in line_text:
                f.readline()
                f.readline()
                line_text=f.readline()
            
            self.function_fit.set(int(str(line_text.split('=')[1]).rstrip()))

            line_text=f.readline()
            self.peak_shape.set(int(str(line_text.split('=')[1]).rstrip()))

            f.readline()
            f.readline()
            
            self.Entry_background_from.delete(0,END)
            self.Entry_background_to.delete(0,END)
            line_text=f.readline()
            while line_text not in ['\n','',None]:
                self.Entry_background_from.insert(END,str(line_text.split('=')[1]).rstrip()+',')
                line_text=f.readline()
                self.Entry_background_to.insert(END,str(line_text.split('=')[1]).rstrip()+',')
                line_text=f.readline()
            
            line_text=f.readline()
            self.Entry_background_polynominal_degrees.delete(0,END)
            self.Entry_background_polynominal_degrees.insert(0,str(line_text.split('=')[1]).rstrip())
            
            line_text=f.readline()
            self.Entry_r.delete(0,END)
            self.Entry_r.insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            self.init_guess.set(int(str(line_text.split('=')[1]).rstrip()))

            f.readline()
            f.readline()

            line_text=f.readline()
            self.Entry_peak[0].delete(0,END)
            self.Entry_peak[0].insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            self.Entry_limit_peak[0].delete(0,END)
            self.Entry_limit_peak[0].insert(0,str(line_text.split('=')[1]).rstrip())

            line_text=f.readline()
            self.Entry_peak_width[0].delete(0,END)
            self.Entry_peak_width[0].insert(0,str(line_text.split('=')[1]).rstrip())

            f.readline()
            if len(self.Entry_peak)==2:
                self.Entry_peak[1].delete(0,END)
                self.Entry_limit_peak[1].delete(0,END)
                self.Entry_peak_width[1].delete(0,END)
                line_text=f.readline()
                while line_text not in ['\n','',None]:
                    self.Entry_peak[1].insert(END,str(line_text.split('=')[1]).rstrip()+',')

                    line_text=f.readline()
                    self.Entry_limit_peak[1].insert(END,str(line_text.split('=')[1]).rstrip()+',')

                    line_text=f.readline()
                    self.Entry_peak_width[1].insert(END,str(line_text.split('=')[1]).rstrip()+',')

                    line_text=f.readline()
        except Exception:
            showinfo(title="Warning",message='Format is not corrected')

        f.close()
        main.root.mainloop()
