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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def rotate_0(self,main):     
    nrow=self.nrow[0]
    ncol=self.ncol[0]
    phi=self.phi[0]
    chi=self.chi[0]

    self.rotate=0
    self.flip=0

    for widget in main.Frame3_1_2.winfo_children():
        widget.destroy()
    fig=plt.figure(1,facecolor="0.94")
    try:
        legend_from= float(self.legend_from_entry.get())
        legend_to= float(self.legend_to_entry.get())
    except ValueError:
        plt.imshow(self.intensity_2D, cmap="hot",origin='lower')
    else:
        plt.imshow(self.intensity_2D,clim=(legend_from, legend_to),cmap="hot",origin='lower')

    plt.title(u'\u03C6='+str(float(phi))+" ; "+u'\u03C7='+str(float(chi)))
    plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), ('1',str(int(nrow*0.25)),str(int(nrow*0.5)),str(int(nrow*0.75)),str(int(nrow))))
    plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), ('1',str(int(ncol*0.25)),str(int(ncol*0.5)),str(int(ncol*0.75)),str(int(ncol))))
    plt.xlabel("pixel")
    plt.ylabel("pixel")
    plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
    plt.close()
    canvas = FigureCanvasTkAgg(fig, main.Frame3_1_2)
    canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    main.root.mainloop()
#--------------------------
def rotate_90(self,main):
    nrow=self.ncol[0]
    ncol=self.nrow[0]
    phi=self.phi[0]
    chi=self.chi[0]

    intensity_2D=np.rot90(self.intensity_2D,k=1,axes=(0, 1))
    
    self.rotate=90

    for widget in main.Frame3_1_2.winfo_children():
        widget.destroy()
    fig=plt.figure(1,facecolor="0.94")
    try:
        legend_from= float(self.legend_from_entry.get())
        legend_to= float(self.legend_to_entry.get())
    except ValueError:
        plt.imshow(intensity_2D, cmap="hot",origin='lower')
    else:
        plt.imshow(intensity_2D,clim=(legend_from, legend_to),cmap="hot",origin='lower')
    plt.title(u'\u03C6='+str(float(phi))+" ; "+u'\u03C7='+str(float(chi)))
    plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), ('1',str(int(nrow*0.25)),str(int(nrow*0.5)),str(int(nrow*0.75)),str(int(nrow))))
    plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), ('1',str(int(ncol*0.25)),str(int(ncol*0.5)),str(int(ncol*0.75)),str(int(ncol))))
    plt.xlabel("pixel")
    plt.ylabel("pixel")
    plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
    plt.close()
    canvas = FigureCanvasTkAgg(fig, main.Frame3_1_2)
    canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    main.root.mainloop()
#------------------------------------
def rotate_180(self,main):
    nrow=self.nrow[0]
    ncol=self.ncol[0]
    phi=self.phi[0]
    chi=self.chi[0]

    intensity_2D=np.rot90(self.intensity_2D,k=2,axes=(0, 1))
    
    self.rotate=180

    for widget in main.Frame3_1_2.winfo_children():
        widget.destroy()
    fig=plt.figure(1,facecolor="0.94")
    try:
        legend_from= float(self.legend_from_entry.get())
        legend_to= float(self.legend_to_entry.get())
    except ValueError:
        plt.imshow(intensity_2D, cmap="hot",origin='lower')
    else:
        plt.imshow(intensity_2D,clim=(legend_from, legend_to),cmap="hot",origin='lower')

    plt.title(u'\u03C6='+str(float(phi))+" ; "+u'\u03C7='+str(float(chi)))
    plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), ('1',str(int(nrow*0.25)),str(int(nrow*0.5)),str(int(nrow*0.75)),str(int(nrow))))
    plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), ('1',str(int(ncol*0.25)),str(int(ncol*0.5)),str(int(ncol*0.75)),str(int(ncol))))
    plt.xlabel("pixel")
    plt.ylabel("pixel")
    plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
    plt.close()
    canvas = FigureCanvasTkAgg(fig, main.Frame3_1_2)
    canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    main.root.mainloop()
#--------------------------------------------
def rotate_270(self,main):
    nrow=self.ncol[0]
    ncol=self.nrow[0]
    phi=self.phi[0]
    chi=self.chi[0]
    
    intensity_2D=np.rot90(self.intensity_2D,k=3,axes=(0, 1))
    
    self.rotate=270

    for widget in main.Frame3_1_2.winfo_children():
        widget.destroy()
    fig=plt.figure(1,facecolor="0.94")
    try:
        legend_from= float(self.legend_from_entry.get())
        legend_to= float(self.legend_to_entry.get())
    except ValueError:
        plt.imshow(intensity_2D, cmap="hot",origin='lower')
    else:
        plt.imshow(intensity_2D,clim=(legend_from, legend_to),cmap="hot",origin='lower')

    plt.title(u'\u03C6='+str(float(phi))+" ; "+u'\u03C7='+str(float(chi)))
    plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), ('1',str(int(nrow*0.25)),str(int(nrow*0.5)),str(int(nrow*0.75)),str(int(nrow))))
    plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), ('1',str(int(ncol*0.25)),str(int(ncol*0.5)),str(int(ncol*0.75)),str(int(ncol))))
    plt.xlabel("pixel")
    plt.ylabel("pixel")
    plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
    plt.close()
    canvas = FigureCanvasTkAgg(fig, main.Frame3_1_2)
    canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    main.root.mainloop()
#----------------------------------
def flip_horizontal(self,main):
    phi=self.phi[0]
    chi=self.chi[0]
    rotate=self.rotate
    self.flip=1
    
    if rotate==0:
        intensity_2D=self.intensity_2D
        nrow=self.nrow[0]
        ncol=self.ncol[0]
       
    if rotate==90:
        intensity_2D=np.rot90(self.intensity_2D,k=1,axes=(0, 1))
        nrow=self.ncol[0]
        ncol=self.nrow[0]
     
    if rotate==180:
        intensity_2D=np.rot90(self.intensity_2D,k=2,axes=(0, 1))
        nrow=self.nrow[0]
        ncol=self.ncol[0]
                
    if rotate==270:
        intensity_2D=np.rot90(self.intensity_2D,k=3,axes=(0, 1))
        nrow=self.ncol[0]
        ncol=self.nrow[0]
        
    intensity_2D=np.flip(intensity_2D,axis=0)
    
    for widget in main.Frame3_1_2.winfo_children():
        widget.destroy()
    fig=plt.figure(1,facecolor="0.94")
    try:
        legend_from= float(self.legend_from_entry.get())
        legend_to= float(self.legend_to_entry.get())
    except ValueError:
        plt.imshow(intensity_2D, cmap="hot",origin='lower')
    else:
        plt.imshow(intensity_2D,clim=(legend_from, legend_to),cmap="hot",origin='lower')

    plt.title(u'\u03C6='+str(float(phi))+" ; "+u'\u03C7='+str(float(chi)))
    plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), ('1',str(int(nrow*0.25)),str(int(nrow*0.5)),str(int(nrow*0.75)),str(int(nrow))))
    plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), ('1',str(int(ncol*0.25)),str(int(ncol*0.5)),str(int(ncol*0.75)),str(int(ncol))))
    plt.xlabel("pixel")
    plt.ylabel("pixel")
    plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
    plt.close()
    canvas = FigureCanvasTkAgg(fig, main.Frame3_1_2)
    canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    main.root.mainloop()

def flip_vertical(self,main):
    phi=self.phi[0]
    chi=self.chi[0]
    rotate=self.rotate
    self.flip=2
    
    if rotate==0:
        intensity_2D=self.intensity_2D
        nrow=self.nrow[0]
        ncol=self.ncol[0]
       
    if rotate==90:
        intensity_2D=np.rot90(self.intensity_2D,k=1,axes=(0, 1))
        nrow=self.ncol[0]
        ncol=self.nrow[0]
     
    if rotate==180:
        intensity_2D=np.rot90(self.intensity_2D,k=2,axes=(0, 1))
        nrow=self.nrow[0]
        ncol=self.ncol[0]
                
    if rotate==270:
        intensity_2D=np.rot90(self.intensity_2D,k=3,axes=(0, 1))
        nrow=self.ncol[0]
        ncol=self.nrow[0]
        
    intensity_2D=np.flip(intensity_2D,axis=1)
    
    for widget in main.Frame3_1_2.winfo_children():
        widget.destroy()
    fig=plt.figure(1,facecolor="0.94")
    try:
        legend_from= float(self.legend_from_entry.get())
        legend_to= float(self.legend_to_entry.get())
    except ValueError:
        plt.imshow(intensity_2D, cmap="hot",origin='lower')
    else:
        plt.imshow(intensity_2D,clim=(legend_from, legend_to),cmap="hot",origin='lower')

    plt.title(u'\u03C6='+str(float(phi))+" ; "+u'\u03C7='+str(float(chi)))
    plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), ('1',str(int(nrow*0.25)),str(int(nrow*0.5)),str(int(nrow*0.75)),str(int(nrow))))
    plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), ('1',str(int(ncol*0.25)),str(int(ncol*0.5)),str(int(ncol*0.75)),str(int(ncol))))
    plt.xlabel("pixel")
    plt.ylabel("pixel")
    plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
    plt.close()
    canvas = FigureCanvasTkAgg(fig, main.Frame3_1_2)
    canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    main.root.mainloop()
