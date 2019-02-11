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
from tkinter.filedialog import *
from tkinter.messagebox import *
from pyFAI.app.calib2 import main as pyFAI_calib

class poni:
    def poni_GUI(self,main):
        Label(main.Frame3_2_1_2, text="pyFAI-calib").grid(row=0,column=0,sticky=W)
        Label(main.Frame3_2_1_2, text="2D XRD image").grid(row=1,column=0,sticky=W)
        Label(main.Frame3_2_1_2, text="d spacing file").grid(row=2,column=0,sticky=W)
        Label(main.Frame3_2_1_2, text="Wavelength(A°)").grid(row=3,column=0,sticky=W)
        Label(main.Frame3_2_1_2, text="Pixel size (µm)").grid(row=4,column=0,sticky=W)
        Label(main.Frame3_2_1_2, text="pixel1,pixel2").grid(row=4,column=2,sticky=W)

        Button(main.Frame3_2_1_2,compound=CENTER, text="Import",bg="white",command=lambda:self.pyFAI_calib_loc(self,main)).grid(row=0,column=1,sticky=W)
        self.pyFAI_calib=''
        Button(main.Frame3_2_1_2,compound=CENTER, text="Import",bg="white",command=lambda:self.ref_2D_image(self,main)).grid(row=1,column=1,sticky=W)
        self.image_ref=''
        Button(main.Frame3_2_1_2,compound=CENTER, text="Import",bg="white",command=lambda:self.hkl_distance(self,main)).grid(row=2,column=1,sticky=W)
        self.hkl=''
        
        self.Entry_wavelength = Entry(main.Frame3_2_1_2)
        self.Entry_wavelength.grid(row=3,column=1,sticky=W)

        self.Entry_pixel = Entry(main.Frame3_2_1_2)
        self.Entry_pixel.grid(row=4,column=1,sticky=W)

        self.pyFAI_calib=''
        self.data_files=[]
        self.hkl=''
        
        Button(main.Frame3_2_1_2,compound=CENTER, text="Run pyFAI-calib",bg="white",command=lambda:pyFAI_calib()).grid(row=6,column=1,sticky=W)
        
    def pyFAI_calib_loc(self,main):
        f = askopenfilename(title="pyFAI-calib.exe",filetypes=[('exe files','*.exe;*.EXE'),('all files','.*')])
        if f is not None and f is not '':
            self.pyFAI_calib=f
            f=f.split('/')
            f=f[len(f)-1]
            Label(main.Frame3_2_1_2, text=f).grid(row=0,column=2,sticky=W)
            
    def ref_2D_image(self,main):
        f = askopenfilename(title="2D XRD image",filetypes=[('all files','.*')])
        if f is not None and f is not '':
            self.data_files=[f]
            f=f.split('/')
            f=f[len(f)-1]
            Label(main.Frame3_2_1_2, text=f).grid(row=1,column=2,sticky=W)

    def hkl_distance(self,main):
        f = askopenfilename(title="hkl file",filetypes=[('D files','*.d;*.D'),('all files','.*')])
        if f is not None and f is not '':
            self.hkl=f
            f=f.split('/')
            f=f[len(f)-1]
            Label(main.Frame3_2_1_2, text=f).grid(row=2,column=2,sticky=W)
            
    def run_pyFAI_calib(self,main):	
        import subprocess
        wavelength=str(self.Entry_wavelength.get())
        pixel=str(self.Entry_pixel.get())

        if self.pyFAI_calib is '':
            showinfo(title="Warning",message="Please import pyFAI-calib\n .../python/Scripts/pyFAI-calib")
        elif self.hkl is '':
            showinfo(title="Warning",message="Please import dSpacing file")
        elif len(self.data_files)<1 :
            showinfo(title="Warning",message="Please import 2D XRD image")
        else:
            command_line=self.pyFAI_calib + ' -w ' + wavelength +' -c ' + '"'+self.hkl+'"' + ' -p '+ pixel + ' "'+self.data_files[0]+'"'
            subprocess.call(command_line)

    def run_pyFAI_calib_2(self,main):
        wavelength=float(self.Entry_wavelength.get())*1e-10
        pixel=str(self.Entry_pixel.get())
        pixelSize=[float(pixel.split(",")[0])*1e-6,float(pixel.split(",")[1])*1e-6]

        c=Calibration()
        c.__init__(dataFiles=self.data_files,pixelSize=pixelSize,wavelength=wavelength,calibrant=self.hkl)
        c.gui_peakPicker()
