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
import os
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import Progressbar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import traceback

from residual_stress_2D.calib_XRD_2D import calib_2D
from residual_stress_2D.angles_modification_2D import angles_modif
from residual_stress_2D.animation_original_frame_2D import rotate_0, rotate_90, rotate_180, rotate_270, flip_horizontal, flip_vertical
from visualisation.definition_poni import definition_poni
from visualisation.show_XRD_2D import show_original_image
from tools.import_poni_parameters_2D import import_poni_parameters
from tools.create_poni_parameters import poni
from read_file.image_2D.read_image_2D import read_header_2D, read_data_2D_1
from visualisation.pack_Frame import pack_Frame_2D
from pyFAI.app.calib2 import main as pyFAI_calib


class import_XRD:
    def __init__(self,main):
        try:
            self.process(main)
        except Exception as e:
            showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
            return
        main.root.mainloop()
        
    def process(self,main):
        format_='*.gfrm;*.edf;*.tif;*.tiff;*.npy;*.cbf;*.mccd;*.xlf;*.nxs;*.raw;*.gfrm;*.EDF;*.TIF;*.TIFF;*.NPY;*.CBF;*.MCCD;*.XLF;*.NXS;*.RAW'
        f = askopenfilenames(parent=main.root,title="Open file",filetypes=[('all supported format',format_),('all files','.*')])
        self.file_link = main.root.tk.splitlist(f)      #list of file link, 1 dimensional list
        if len(self.file_link)>0:
            self.import_image_header(main)
        
            if len(self.phi)>0:
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.destroy_widget(main)
                self.graphic_frame3_1(main)

                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.attribute_graphic_frame3_2(main) 
        
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()
        pack_Frame_2D(main,1)

    def import_image_header(self,main):    
            for widget in main.Frame1_2.winfo_children():
                widget.destroy()       
            Label(main.Frame1_2,text="Import").pack(side=LEFT)
            self.progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
            self.progress.pack(side=LEFT)
            self.progress["value"] = 0
            self.progress["maximum"] = len(self.file_link)+2
            #-----------------find and affiche list phi, chi--------------------------------------
            self.filename=[]            #list of file name, 1 dimensional list
            self.phi=[]                 #list of phi, 1 dimensional list
            self.chi=[]                 #list of chi, 1 dimensional list
            self.omega=[]               #list of omega, 1 dimensional list
            self.twotheta_center=[]     #list of twotheta center, 1 dimensional list
            self.k_alpha=[]             #list of phi, 2 dimensional list: self.kalpha=[[kalpha1,kalpha2],[kalpha1,kalpha2],...]; kalpha1, kalpha2 are float
            self.nrow=[]                #list of number of row, 1 dimensional list
            self.ncol=[]                #list of number of column, 1 dimensional list
            self.row_tick=[]            #list of number of row tick, 2 dimensional list: self.row_tick=[[row_tick],[row_tick],....]; with len(row_tick)=nrow
            self.col_tick=[]            #list of number of column tick, 2 dimensional list: self.col_tick=[[col_tick],[col_tick],....]; with len(col_tick)=ncol
            self.center_row=[]          #list of detector center in row, 1 dimensional list
            self.center_col=[]          #list of detector center in column, 1 dimensional list
            self.distance=[]            #list of distance from detector to sample, 1 dimensional list
            self.nfile=[]               #list index of number of file of image, 1 dimensional list
            self.nimage_i=[]            #list index of number of image in one file, 1 dimensional list
            self.nimage=[]              #list index of number of image in total, 1 dimensional list
            self.file_info=[]           #list of header information of image, 2 dimensional list: self.file_info=[[header_info],[header_info],....]
            self.image=-1               #index of image
            self.dtyp='uint32'          #for raw image
            self.sep=''                #for raw image
            for i in range(len(self.file_link)):
                self.progress["value"] = self.progress["value"]+1
                self.progress.update()
                self.i=i
                
                self.f=self.file_link[i]
                f_split=self.f.split("/")
                self.filename.append(f_split[len(f_split)-1])

                read_header_2D(i,self)

    def destroy_widget(self,main):
        for widget in main.Frame3_1_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_1_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_1_3_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_1_3_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_1_4.winfo_children():
            widget.destroy()
            
        #for widget in main.Frame3_2_1_1.winfo_children():
            #widget.destroy()
        #for widget in main.Frame3_2_1_2.winfo_children():
            #widget.destroy()
        for widget in main.Frame3_2_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_2_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_2_4.winfo_children():
            widget.destroy()
            
        for widget in main.Frame3_3_1.winfo_children():
            widget.destroy()
        #for widget in main.Frame3_3_2_1.winfo_children():
            #widget.destroy()
        #for widget in main.Frame3_3_2_2.winfo_children():
            #widget.destroy()
        for widget in main.Frame3_3_3.winfo_children():
            widget.destroy()
            
        #for widget in main.Frame3_4_1.winfo_children():
            #widget.destroy()
        #for widget in main.Frame3_4_2.winfo_children():
            #widget.destroy()
        #for widget in main.Frame3_4_3.winfo_children():
            #widget.destroy()
        for widget in main.Frame3_4_4_1_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_4_4_1_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_4_4_2.winfo_children():
            widget.destroy()
            
        for widget in main.Frame3_5_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_3_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_3_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_3_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_4_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_4_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_5_4_3.winfo_children():
            widget.destroy()

        for widget in main.Frame3_6_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_2_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_2_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_2_3.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_6_3_3.winfo_children():
            widget.destroy()
            
        for widget in main.Frame3_7_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_2.winfo_children():
            widget.destroy()
        for widget in main.Frame3_7_3.winfo_children():
            widget.destroy()
            
        for widget in main.Frame3_8_1.winfo_children():
            widget.destroy()
        for widget in main.Frame3_8_2.winfo_children():
            widget.destroy()
                       
    def graphic_frame3_1(self,main):
        Label(main.Frame3_1_3_2, text="Image legend",bg="white").grid(row=0,column=0)
        Label(main.Frame3_1_3_2, text="from").grid(row=1,column=0)
        self.legend_from_entry = Entry(main.Frame3_1_3_2,width=6)
        self.legend_from_entry.grid(row=2,column=0)
        
        Label(main.Frame3_1_3_2, text="to").grid(row=3,column=0)
        self.legend_to_entry = Entry(main.Frame3_1_3_2,width=6)
        self.legend_to_entry.grid(row=4,column=0)
        
        self.cmap_var=StringVar()
        Radiobutton(main.Frame3_1_3_2, text="hot", variable=self.cmap_var, value="hot").grid(row=5,column=0,sticky=W)
        Radiobutton(main.Frame3_1_3_2, text="cool", variable=self.cmap_var, value="GnBu").grid(row=6,column=0,sticky=W)
        Radiobutton(main.Frame3_1_3_2, text="gray", variable=self.cmap_var, value="gray").grid(row=7,column=0,sticky=W)
        Radiobutton(main.Frame3_1_3_2, text="nipy", variable=self.cmap_var, value="nipy_spectral").grid(row=8,column=0,sticky=W)
        self.cmap_var.set("hot")
            
        scrollbar = Scrollbar(main.Frame3_1_1)
        scrollbar.pack(side = RIGHT, fill=Y) 
        mylist= Listbox(main.Frame3_1_1, yscrollcommand = scrollbar.set)
        mylist.pack(side = LEFT, fill = BOTH,expand=YES)
        for i in range(len(self.phi)):
            mylist.insert(END, str(i+1)+u'. \u03C6='+str(self.phi[i])+" ; "+u'\u03C7='+str(self.chi[i])+u"; \u03C9="+str(float(self.omega[i]))+
                          ' (.'+str(self.nfile[i]+1)+'.'+str(self.nimage_i[i]+1)+'.)')
        self.rotate=0
        self.flip=0
        mylist.bind("<ButtonRelease-1>", lambda event: show_original_image(event,self,main))
        scrollbar.config(command = mylist.yview)
        #----------------affiche the first image valide---------------------------------------

        data=read_data_2D_1(0,self,main)
        data_dim=len(data.shape)
                    
        if data_dim==2:                 
            self.intensity_2D=data
        elif data_dim==3:
            self.intensity_2D=data[0]
        else:
            self.intensity_2D=[]

        self.legend_from_entry.insert(0,0)
        self.legend_to_entry.insert(0,max(map(max, self.intensity_2D)))
        
        fig=plt.figure(1,facecolor="0.94")
        plt.imshow(self.intensity_2D,cmap="hot",origin='lower')
        plt.title(u'\u03C6='+str(float(self.phi[0]))+" ; "+u'\u03C7='+str(float(self.chi[0]))+u"; \u03C9="+str(float(self.omega[0])))
        nrow=self.nrow[0]
        ncol=self.ncol[0]
        plt.yticks((1,nrow*0.25,nrow*0.5,nrow*0.75,nrow), ('%0.1f' % self.row_tick[0][0],
                                                           '%0.1f' % self.row_tick[0][int(nrow*0.25)],
                                                           '%0.1f' % self.row_tick[0][int(nrow*0.5)],
                                                           '%0.1f' % self.row_tick[0][int(nrow*0.75)],
                                                           '%0.1f' % self.row_tick[0][int(nrow-1)]))
        plt.xticks((1,ncol*0.25,ncol*0.5,ncol*0.75,ncol), ('%0.1f' % self.col_tick[0][0],
                                                           '%0.1f' % self.col_tick[0][int(ncol*0.25)],
                                                           '%0.1f' % self.col_tick[0][int(ncol*0.5)],
                                                           '%0.1f' % self.col_tick[0][int(ncol*0.75)],
                                                           '%0.1f' % self.col_tick[0][int(ncol-1)]))
        plt.xlabel("pixel")
        plt.ylabel("pixel")
        plt.colorbar( cax=plt.axes([0.9, 0.45, 0.02, 0.4]) )
        plt.close()
         
        canvas = FigureCanvasTkAgg(fig, main.Frame3_1_2)
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        Button(main.Frame3_1_3_1,compound=CENTER, text="Original",bg="white",command=lambda:rotate_0(self,main)).pack() 
        Button(main.Frame3_1_3_1,compound=CENTER, text="Rotate +90°",bg="white",command=lambda:rotate_270(self,main)).pack()
        Button(main.Frame3_1_3_1,compound=CENTER, text="Rotate -90°",bg="white",command=lambda:rotate_90(self,main)).pack()    
        Button(main.Frame3_1_3_1,compound=CENTER, text="Rotate +180°",bg="white",command=lambda:rotate_180(self,main)).pack()    
        Button(main.Frame3_1_3_1,compound=CENTER, text="Flip horizontal",bg="white",command=lambda:flip_horizontal(self,main)).pack() 
        Button(main.Frame3_1_3_1,compound=CENTER, text="Flip vertical",bg="white",command=lambda:flip_vertical(self,main)).pack() 

        scrollbar = Scrollbar(main.Frame3_1_4)
        scrollbar.pack(side = RIGHT, fill=BOTH) 
        mylist = Listbox(main.Frame3_1_4, yscrollcommand = scrollbar.set)

        for i in range(len(self.file_info[0])):
            mylist.insert(END,str(self.file_info[0][i]))

        mylist.pack(side = LEFT, fill=BOTH,expand=YES)
        scrollbar.config( command = mylist.yview )

           
        #----------Frame3_2-------------------------------------------------------------------------
    def graphic_frame3_2(self,main):
        Label(main.Frame3_2_1_1, text="PONI PARAMETERS", bg="white").grid(row=0,column=0,sticky=W)
        Label(main.Frame3_2_1_1, text="Pixel size 1 (m)").grid(row=1,column=0,sticky=W)
        Label(main.Frame3_2_1_1, text="Pixel size 2 (m)").grid(row=2,column=0,sticky=W)
        Label(main.Frame3_2_1_1, text="Distance (m)").grid(row=3,column=0,sticky=W)
        Label(main.Frame3_2_1_1, text="Poni 1 (m)").grid(row=4,column=0,sticky=W)
        Label(main.Frame3_2_1_1, text="Poni 2 (m)").grid(row=5,column=0,sticky=W)
        Label(main.Frame3_2_1_1, text="Rotation 1 (radians)").grid(row=6,column=0,sticky=W)
        Label(main.Frame3_2_1_1, text="Rotation 2 (radians)").grid(row=7,column=0,sticky=W)
        Label(main.Frame3_2_1_1, text="Rotation 3 (radians)").grid(row=8,column=0,sticky=W)
        Label(main.Frame3_2_1_1, text="Wavelength (m)").grid(row=9,column=0,sticky=W)
                  
        self.Entry_pixel_1 = Entry(main.Frame3_2_1_1)
        self.Entry_pixel_2 = Entry(main.Frame3_2_1_1)
        self.Entry_distance_calib = Entry(main.Frame3_2_1_1)
        self.Entry_poni_1 = Entry(main.Frame3_2_1_1)
        self.Entry_poni_2 = Entry(main.Frame3_2_1_1)
        self.Entry_rot_1 = Entry(main.Frame3_2_1_1)
        self.Entry_rot_2 = Entry(main.Frame3_2_1_1)
        self.Entry_rot_3 = Entry(main.Frame3_2_1_1)
        self.Entry_wl_calib = Entry(main.Frame3_2_1_1)
                 
        self.Entry_pixel_1.grid(row=1, column=1,sticky=W)
        self.Entry_pixel_2.grid(row=2, column=1,sticky=W)
        self.Entry_distance_calib.grid(row=3, column=1,sticky=W)
        self.Entry_poni_1.grid(row=4, column=1,sticky=W)
        self.Entry_poni_2.grid(row=5, column=1,sticky=W)
        self.Entry_rot_1.grid(row=6, column=1,sticky=W)
        self.Entry_rot_2.grid(row=7, column=1,sticky=W)
        self.Entry_rot_3.grid(row=8, column=1,sticky=W)
        self.Entry_wl_calib.grid(row=9, column=1,sticky=W)
        
        Button(main.Frame3_2_1_1,compound=CENTER, text="PONI definition",bg="white",command=definition_poni).grid(row=10,column=0,sticky=W)
        Button(main.Frame3_2_1_1,compound=CENTER, text="Import poni parameters",bg="white",command=lambda:import_poni_parameters(self,main)).grid(row=0,column=1,sticky=W)
        self.button_run_calib=Button(main.Frame3_2_1_1,compound=CENTER, text="RUN CALIBRATION",bg="white",command=lambda:None)
        self.button_run_calib.grid(row=0,column=2,sticky=W)     
        Button(main.Frame3_2_1_1,compound=CENTER, text="Create PONI parameters",bg="white",command=lambda:pyFAI_calib()).grid(row=11,column=0,sticky=W)

    def attribute_graphic_frame3_2(self,main):
        self.button_run_calib.config(command=lambda:calib_2D(self,main))
        calib_2D.button_apply.config(command=lambda:None)
        calib_2D.button_init.config(command=lambda:None)
        calib_2D.button_advance.config(command=lambda:None)
        calib_2D.button_init_wavelength.config(command=lambda:None)
        calib_2D.button_psc.config(command=lambda:None)
        calib_2D.Button_limit_preview.config(command=lambda:None) 
        calib_2D.Button_fit_preview.config(command=lambda:None)       
        calib_2D.Button_run_calcul.config(command=lambda:None)

        angles_modif.Button_import_gma.config(command=lambda:None)
        angles_modif.Button_next.config(command=lambda:None)
        angles_modif.Button_apply_gma.config(command=lambda:None)
        
