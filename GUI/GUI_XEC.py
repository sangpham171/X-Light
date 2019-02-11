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
from visualisation.pack_Frame import pack_Frame_XEC
from XEC.import_strain import import_strain
from XEC.import_load import import_load
from XEC.peak_info import import_peak_info
screen_width=1920
screen_height=1080
###########################################################################################################################################
def GUI_XEC(self):
    from GUI.GUI_home import GUI_home, about, root_exit
    
    for widget in self.root.winfo_children():
        widget.destroy()

    self.Frame0 = Frame(self.root, borderwidth=0, relief=GROOVE,width=screen_width,height=screen_height*0.1)
    self.Frame0.pack(fill=X,expand=YES,side=TOP)
    self.Frame0.pack_propagate(1)

    self.Frame1 = Frame(self.root, borderwidth=0, relief=GROOVE,width=screen_width,height=screen_height*0.1)
    self.Frame1.pack(fill=X,expand=YES,side=TOP)
    self.Frame1.pack_propagate(1)

    self.Frame1_1 = Frame(self.Frame1, borderwidth=0, relief=GROOVE,width=screen_width*0.5,height=screen_height*0.1)
    self.Frame1_1.pack(side=LEFT)
    self.Frame1_1.pack_propagate(1)

    self.Frame1_2 = Frame(self.Frame1, borderwidth=0, relief=GROOVE,width=screen_width*0.5,height=screen_height*0.1)
    self.Frame1_2.pack(side=RIGHT)
    self.Frame1_2.pack_propagate(1)

    self.Frame2 = Frame(self.root, borderwidth=2, relief=GROOVE,width=screen_width,height=screen_height*0.1)
    self.Frame2.pack(fill=X,expand=YES,side=TOP)
    self.Frame2.pack_propagate(1)

    self.Frame3 = Frame(self.root, borderwidth=0, relief=GROOVE,width=screen_width,height=screen_height)
    self.Frame3.pack(fill=X,expand=YES,side=TOP)
    self.Frame3.pack_propagate(1)
    
    Label(self.Frame0, text='X-RAY ELASTIC CONSTANT ANALYSIS',bg="white").pack()
    self.menubar = Menu(self.root)
    self.menu1 = Menu(self.menubar, tearoff=0)
    self.menu1.add_command(label="Exit", command=lambda:root_exit(self))
    self.menubar.add_cascade(label="Files", menu=self.menu1) 
    self.menubar.add_command(label="About", command=lambda:about(self))
    self.root.config(menu=self.menubar)
    
    self.button_strain=Button(self.Frame1_1, compound=CENTER, text="Import strain",bg="white")
    self.button_strain.config(command=lambda:import_strain(import_load,self))
    self.button_strain.pack(padx=5,pady=5,side=LEFT)

    #self.button_load=Button(self.Frame1_1, compound=CENTER, text="Import peak info",bg="white")
    #self.button_load.config(command=lambda:import_peak_info(self))
    #self.button_load.pack(padx=5,pady=5,side=LEFT)
    
    self.button_load=Button(self.Frame1_1, compound=CENTER, text="Import load",bg="white")
    self.button_load.config(command=lambda:import_load(import_strain,self))
    self.button_load.pack(padx=5,pady=5,side=LEFT)
    
    self.button_run=Button(self.Frame1_1, compound=CENTER, text="Run",bg="white")
    self.button_run.pack(padx=5,pady=5,side=LEFT)

    Button(self.Frame1_1,compound=CENTER, text="Home",bg="white",command=lambda:GUI_home(self)).pack(padx=5,pady=5,side=RIGHT)

    self.Frame3_1 = Frame(self.Frame3,width=screen_width,height=screen_height)
    self.Frame3_1.pack_propagate(1)
    paned=PanedWindow(self.Frame3_1,orient=HORIZONTAL,width=screen_width,height=screen_height)
    self.Frame3_1_1= Frame(self.Frame3_1,width=screen_width*0.1,height=screen_height)   
    self.Frame3_1_2= Frame(self.Frame3_1,width=screen_width*0.4,height=screen_height)
    self.Frame3_1_3= Frame(self.Frame3_1,width=screen_width*0.4,height=screen_height)
    
    paned.add(self.Frame3_1_1,stretch="never")
    paned.add(self.Frame3_1_2,stretch="always")
    paned.add(self.Frame3_1_3,stretch="always")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1) 

    self.Frame3_2 = Frame(self.Frame3,width=screen_width,height=screen_height)
    self.Frame3_2.pack_propagate(1)
    self.Frame3_2_1= Frame(self.Frame3_2,width=screen_width*0.7,height=screen_height)
    self.Frame3_2_1.pack(side=LEFT)
    self.Frame3_2_1.pack_propagate(1)    
    self.Frame3_2_2= Frame(self.Frame3_2,width=screen_width*0.3,height=screen_height)
    self.Frame3_2_2.pack(side=LEFT)
    self.Frame3_2_2.pack_propagate(1)
    self.Frame3_2_3= Frame(self.Frame3_2,height=screen_height)
    self.Frame3_2_3.pack(side=LEFT)
    self.Frame3_2_3.pack_propagate(1)
    
    self.Frame3_3 = Frame(self.Frame3,width=screen_width,height=screen_height)
    self.Frame3_3.pack_propagate(1)
    self.Frame3_3_1= Frame(self.Frame3_3,width=screen_width,height=screen_height*0.1)
    self.Frame3_3_1.pack(side=TOP)
    self.Frame3_3_1.pack_propagate(1)        
    self.Frame3_3_2= Frame(self.Frame3_3,width=screen_width,height=screen_height)
    self.Frame3_3_2.pack(side=TOP)
    self.Frame3_3_2.pack_propagate(1)

    paned=PanedWindow(self.Frame3_3_2,orient=HORIZONTAL,width=screen_width,height=screen_height)
    self.Frame3_3_2_1= Frame(self.Frame3_3_2,width=screen_width*0.5,height=screen_height)
    self.Frame3_3_2_2= Frame(self.Frame3_3_2,width=screen_width*0.5,height=screen_height)
    paned.add(self.Frame3_3_2_1,stretch="always")
    paned.add(self.Frame3_3_2_2,stretch="always")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1)
 
    self.Button3_1=Button(self.Frame2,compound=CENTER, text="STRAIN",bg="white",command=lambda:pack_Frame_XEC(self,self.Frame3_1,self.Button3_1))
    self.Button3_1.pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)
    self.Button3_2=Button(self.Frame2,compound=CENTER, text="LOAD",bg="white",command=lambda:pack_Frame_XEC(self,self.Frame3_2,self.Button3_2))
    self.Button3_2.pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)
    self.Button3_3=Button(self.Frame2,compound=CENTER, text="RESULT",bg="white",command=lambda:pack_Frame_XEC(self,self.Frame3_3,self.Button3_3))
    self.Button3_3.pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)
    self.root.mainloop()
