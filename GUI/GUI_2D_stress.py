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
from residual_stress_2D.import_XRD_2D import import_XRD
from residual_stress_2D.calib_XRD_2D import calib_2D
from residual_stress_2D.angles_modification_2D import angles_modif
from residual_stress_2D.main_calcul_2D import main_calcul
from visualisation.pack_Frame import pack_Frame_2D
screen_width=1920
screen_height=1080

def GUI_2D_stress(self):
    from GUI.GUI_home import GUI_home, about, root_exit
    
    for widget in self.root.winfo_children():
        widget.destroy()
    #Frame0,1,2,3 in vertical direction
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

    self.Frame2 = Frame(self.root, borderwidth=2, relief=GROOVE,width=screen_width,height=screen_height*0.1) #tittle graphical representation
    self.Frame2.pack(fill=X,expand=YES,side=TOP)
    self.Frame2.pack_propagate(1)

    self.Frame3 = Frame(self.root, borderwidth=0, relief=GROOVE,width=screen_width,height=screen_height) #graphical representation, Frame3_1,2.. in horizontal direction
    self.Frame3.pack(fill=X,expand=YES,side=TOP)
    self.Frame3.pack_propagate(1)
    
    Label(self.Frame0, text='2D XRD STRESS ANALYSIS',bg="white").pack()
    self.menubar = Menu(self.root)
    self.menu1 = Menu(self.menubar, tearoff=0)
    self.menu1.add_command(label="Import XRD 2D",command=lambda:import_XRD(self))
    self.menu1.add_separator()
    self.menu1.add_command(label="Exit", command=lambda:root_exit(self))
    self.menubar.add_cascade(label="Files", menu=self.menu1) 
    self.menubar.add_command(label="About", command=lambda:about(self))
    self.root.config(menu=self.menubar)
    
    Button(self.Frame1_1, compound=CENTER, text="Import XRD",bg="white",command=lambda:import_XRD(self)).pack(padx=5,pady=5,side=LEFT) #import images XRD
    Button(self.Frame1_1,compound=CENTER, text="Home",bg="white",command=lambda:GUI_home(self)).pack(padx=5,pady=5,side=RIGHT) #return home

    self.Button_next=Button(self.Frame1_1,compound=CENTER, text=u"\u27F6",bg="white") #next Frame
    self.Button_next.pack(padx=5,pady=5,side=RIGHT)
    
    self.Button_prev=Button(self.Frame1_1,compound=CENTER, text=u"\u27F5",bg="white")
    self.Button_prev.pack(padx=5,pady=5,side=RIGHT)

    self.Frame3_=[]
    self.Frame3_.append(None)
                
    self.Frame3_.append(Frame(self.Frame3,width=screen_width,height=screen_height))
    self.Frame3_[1].pack_propagate(1)
    paned=PanedWindow(self.Frame3_[1],orient=HORIZONTAL,width=screen_width,height=screen_height)
    self.Frame3_1_1= Frame(self.Frame3_[1],width=screen_width*0.1,height=screen_height)
    self.Frame3_1_2= Frame(self.Frame3_[1],width=screen_width*0.5,height=screen_height, borderwidth=2, relief=GROOVE)
    self.Frame3_1_3= Frame(self.Frame3_[1],width=screen_width*0.1,height=screen_height)
    self.Frame3_1_4= Frame(self.Frame3_[1],width=screen_width*0.3,height=screen_height, borderwidth=2, relief=GROOVE)
    paned.add(self.Frame3_1_1,stretch="never")
    paned.add(self.Frame3_1_2,stretch="always")
    paned.add(self.Frame3_1_3,stretch="never")
    paned.add(self.Frame3_1_4,stretch="never")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1)

    self.Frame3_1_3_1= Frame(self.Frame3_1_3)
    self.Frame3_1_3_1.pack(side=TOP)
    self.Frame3_1_3_2= Frame(self.Frame3_1_3)
    self.Frame3_1_3_2.pack(side=BOTTOM)
    
    self.Frame3_.append(Frame(self.Frame3,width=screen_width,height=screen_height))
    self.Frame3_[2].pack_propagate(1)
    paned=PanedWindow(self.Frame3_[2],orient=HORIZONTAL,width=screen_width,height=screen_height)
    self.Frame3_2_1= Frame(self.Frame3_[2],width=screen_width*0.4,height=screen_height)
    self.Frame3_2_2= Frame(self.Frame3_[2],width=screen_width*0.1,height=screen_height)
    self.Frame3_2_3= Frame(self.Frame3_[2],width=screen_width*0.4,height=screen_height)
    self.Frame3_2_4= Frame(self.Frame3_[2],width=screen_width*0.1,height=screen_height)
    paned.add(self.Frame3_2_1,stretch="never")
    paned.add(self.Frame3_2_2,stretch="never")
    paned.add(self.Frame3_2_3,stretch="always")
    paned.add(self.Frame3_2_4,stretch="never")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1)

    self.Frame3_2_1_1= Frame(self.Frame3_2_1)
    self.Frame3_2_1_1.pack(side=TOP)
    self.Frame3_2_1_2= Frame(self.Frame3_2_1)
    self.Frame3_2_1_2.pack(side=TOP)

    self.Frame3_.append(Frame(self.Frame3,width=screen_width,height=screen_height))
    self.Frame3_[3].pack_propagate(1)
    paned=PanedWindow(self.Frame3_[3],orient=HORIZONTAL,width=screen_width,height=screen_height)
    self.Frame3_3_1= Frame(self.Frame3_[3],width=screen_width*0.05,height=screen_height)
    self.Frame3_3_2= Frame(self.Frame3_[3],width=screen_width*0.2,height=screen_height, borderwidth=2, relief=GROOVE)
    self.Frame3_3_3= Frame(self.Frame3_[3],width=screen_width*0.5,height=screen_height)
    paned.add(self.Frame3_3_1,stretch="never")
    paned.add(self.Frame3_3_2,stretch="never")
    paned.add(self.Frame3_3_3,stretch="always")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1)

    self.Frame3_3_2_1= Frame(self.Frame3_3_2)
    self.Frame3_3_2_1.pack(side=TOP)
    self.Frame3_3_2_2= Frame(self.Frame3_3_2)
    self.Frame3_3_2_2.pack(side=TOP)
    
    self.Frame3_.append(Frame(self.Frame3,width=screen_width,height=screen_height))
    self.Frame3_[4].pack_propagate(1)
    paned=PanedWindow(self.Frame3_[4],orient=HORIZONTAL,width=screen_width,height=screen_height)
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1)
    self.Frame3_4_1= Frame(self.Frame3_[4],width=screen_width*0.3,height=screen_height, borderwidth=2, relief=GROOVE)
    self.Frame3_4_2= Frame(self.Frame3_[4],width=screen_width*0.3,height=screen_height, borderwidth=2, relief=GROOVE)
    self.Frame3_4_3= Frame(self.Frame3_[4],width=screen_width*0.05,height=screen_height, borderwidth=2, relief=GROOVE)
    self.Frame3_4_4= Frame(self.Frame3_[4],width=screen_width*0.35,height=screen_height)
    paned.add(self.Frame3_4_1,stretch="never")
    paned.add(self.Frame3_4_2,stretch="never")
    paned.add(self.Frame3_4_3,stretch="never")
    paned.add(self.Frame3_4_4,stretch="always")

    paned=PanedWindow(self.Frame3_4_4,orient=VERTICAL,width=screen_width,height=screen_height)
    self.Frame3_4_4_1= Frame(self.Frame3_4_4,width=screen_width*0.35,height=screen_height*0.5, borderwidth=1, relief=GROOVE)
    self.Frame3_4_4_2= Frame(self.Frame3_4_4,width=screen_width*0.35,height=screen_height*0.5, borderwidth=1, relief=GROOVE)
    paned.add(self.Frame3_4_4_1,stretch="always")
    paned.add(self.Frame3_4_4_2,stretch="always")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1)

    paned=PanedWindow(self.Frame3_4_4_1,orient=HORIZONTAL,width=screen_width,height=screen_height)
    self.Frame3_4_4_1_1= Frame(self.Frame3_4_4_1)
    self.Frame3_4_4_1_2= Frame(self.Frame3_4_4_1)
    paned.add(self.Frame3_4_4_1_1,stretch="always")
    paned.add(self.Frame3_4_4_1_2,stretch="never")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1)

    self.Frame3_.append(Frame(self.Frame3,width=screen_width,height=screen_height))
    self.Frame3_[5].pack_propagate(1)
    paned=PanedWindow(self.Frame3_[5],orient=HORIZONTAL,width=screen_width,height=screen_height)
    self.Frame3_5_1= Frame(self.Frame3_[5],width=screen_width*0.05,height=screen_height)
    self.Frame3_5_2= Frame(self.Frame3_[5],width=screen_width*0.45,height=screen_height, borderwidth=2, relief=GROOVE)
    self.Frame3_5_3= Frame(self.Frame3_[5],width=screen_width*0.05,height=screen_height)
    self.Frame3_5_4= Frame(self.Frame3_[5],width=screen_width*0.45,height=screen_height, borderwidth=2, relief=GROOVE)    
    paned.add(self.Frame3_5_1,stretch="never")
    paned.add(self.Frame3_5_2,stretch="always")
    paned.add(self.Frame3_5_3,stretch="never")
    paned.add(self.Frame3_5_4,stretch="always")
    paned.pack(expand=YES,fill=BOTH)
    paned.pack_propagate(1)

    self.Frame3_5_3_1= Frame(self.Frame3_5_3)
    self.Frame3_5_3_1.pack(side=TOP)
    self.Frame3_5_3_2= Frame(self.Frame3_5_3)
    self.Frame3_5_3_2.pack(side=BOTTOM)
    self.Frame3_5_3_3= Frame(self.Frame3_5_3)
    self.Frame3_5_3_3.pack(side=BOTTOM)

    paned=PanedWindow(self.Frame3_5_4,orient=VERTICAL,width=screen_width*0.45,height=screen_height)
    self.Frame3_5_4_1= Frame(self.Frame3_5_4)
    self.Frame3_5_4_2= Frame(self.Frame3_5_4,height=screen_height*0.05)
    self.Frame3_5_4_3= Frame(self.Frame3_5_4,height=screen_height*0.05)
    paned.add(self.Frame3_5_4_1,stretch="always")
    paned.add(self.Frame3_5_4_2,stretch="never")
    paned.add(self.Frame3_5_4_3,stretch="never")
    paned.pack(expand=YES,fill=BOTH)
    paned.pack_propagate(1)
    
    self.Frame3_.append(Frame(self.Frame3,width=screen_width,height=screen_height))
    self.Frame3_[6].pack_propagate(1)
    paned=PanedWindow(self.Frame3_[6],orient=HORIZONTAL,width=screen_width,height=screen_height)
    self.Frame3_6_1= Frame(self.Frame3_[6],width=screen_width*0.1,height=screen_height)
    self.Frame3_6_2= Frame(self.Frame3_[6],width=screen_width*0.8,height=screen_height, borderwidth=2, relief=GROOVE)
    self.Frame3_6_3= Frame(self.Frame3_[6],width=screen_width*0.1,height=screen_height)
    paned.add(self.Frame3_6_1,stretch="never")
    paned.add(self.Frame3_6_2,stretch="always")
    paned.add(self.Frame3_6_3,stretch="never")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1) 
    
    paned=PanedWindow(self.Frame3_6_2,orient=VERTICAL,width=screen_width*0.8,height=screen_height)
    self.Frame3_6_2_1= Frame(self.Frame3_6_2,width=screen_width*0.8,height=screen_height*0.1)
    self.Frame3_6_2_2= Frame(self.Frame3_6_2,width=screen_width*0.8,height=screen_height*0.1, borderwidth=2, relief=GROOVE)
    self.Frame3_6_2_3= Frame(self.Frame3_6_2,width=screen_width*0.8,height=screen_height*0.9)
    paned.add(self.Frame3_6_2_1,stretch="never")
    paned.add(self.Frame3_6_2_2,stretch="never")
    paned.add(self.Frame3_6_2_3,stretch="always")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1)

    self.Frame3_6_3_1= Frame(self.Frame3_6_3)
    self.Frame3_6_3_1.pack(side=TOP)
    self.Frame3_6_3_2= Frame(self.Frame3_6_3)
    self.Frame3_6_3_2.pack(side=TOP)
    self.Frame3_6_3_3= Frame(self.Frame3_6_3)
    self.Frame3_6_3_3.pack(side=TOP)
    
    self.Frame3_.append(Frame(self.Frame3,width=screen_width,height=screen_height))
    self.Frame3_[7].pack_propagate(1)
    paned=PanedWindow(self.Frame3_[7],orient=HORIZONTAL,width=screen_width,height=screen_height)
    self.Frame3_7_1= Frame(self.Frame3_[7],width=screen_width*0.1,height=screen_height)
    self.Frame3_7_2= Frame(self.Frame3_[7],width=screen_width*0.45,height=screen_height)
    self.Frame3_7_3= Frame(self.Frame3_[7],width=screen_width*0.45,height=screen_height)
    paned.add(self.Frame3_7_1,stretch="never")
    paned.add(self.Frame3_7_2,stretch="always")
    paned.add(self.Frame3_7_3,stretch="always")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1) 

    self.Frame3_.append(Frame(self.Frame3,width=screen_width,height=screen_height))
    self.Frame3_[8].pack_propagate(1)
    paned=PanedWindow(self.Frame3_[8],orient=HORIZONTAL,width=screen_width,height=screen_height)
    self.Frame3_8_1= Frame(self.Frame3_[8],width=screen_width*0.1,height=screen_height)
    self.Frame3_8_2= Frame(self.Frame3_[8],width=screen_width*0.5,height=screen_height)
    paned.add(self.Frame3_8_1,stretch="never")
    paned.add(self.Frame3_8_2,stretch="always")
    paned.pack(expand=YES, fill=BOTH)
    paned.pack_propagate(1) 

    self.Button3_=[]
    self.Button3_.append(None)
    
    self.Button3_.append(Button(self.Frame2,compound=CENTER, text="ORIGINAL XRD",bg="white",command=lambda:pack_Frame_2D(self,1)))
    self.Button3_[1].pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)
    
    self.Button3_.append(Button(self.Frame2,compound=CENTER, text="CALIB XRD",bg="white",command=lambda:pack_Frame_2D(self,2)))
    self.Button3_[2].pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)
    
    self.Button3_.append(Button(self.Frame2,compound=CENTER, text="ANGLES MODIFICATION",bg="white",command=lambda:pack_Frame_2D(self,3)))
    self.Button3_[3].pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)
    
    self.Button3_.append(Button(self.Frame2,compound=CENTER, text="STRESS PARAMETERS",bg="white",command=lambda:pack_Frame_2D(self,4)))
    self.Button3_[4].pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)
    
    self.Button3_.append(Button(self.Frame2,compound=CENTER, text="FIT RESULTS",bg="white",command=lambda:pack_Frame_2D(self,5)))
    self.Button3_[5].pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)
    
    self.Button3_.append(Button(self.Frame2,compound=CENTER, text="STRESS RESULTS",bg="white",command=lambda:pack_Frame_2D(self,6)))
    self.Button3_[6].pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)
    
    self.Button3_.append(Button(self.Frame2,compound=CENTER, text="STRESS TENSOR",bg="white",command=lambda:pack_Frame_2D(self,7)))
    self.Button3_[7].pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)
    
    self.Button3_.append(Button(self.Frame2,compound=CENTER, text="OTHER INFO",bg="white",command=lambda:pack_Frame_2D(self,8)))
    self.Button3_[8].pack(padx=5,pady=5,side=LEFT,fill=X,expand=YES)

    import_XRD.graphic_frame3_2(import_XRD,self) #create "CALIB XRD" graphic, residual_stress_2D/import_XRD_2D
    
    calib_2D.graphic_Frame3_3(calib_2D,import_XRD,angles_modif,main_calcul,self) #create "ANGLES MODIFICATION" graphic, residual_stress_2D/calib_XRD_2D
    calib_2D.graphic_Frame3_4(calib_2D,import_XRD,angles_modif,main_calcul,self) #create "STRESS PARAMETERS" graphic, residual_stress_2D/calib_XRD_2D
    angles_modif.__init__(angles_modif,self) #reset buttons in "ANGLES MODIFICATION" graphic, residual_stress_2D/angles_modification_2D

    self.root.mainloop()
