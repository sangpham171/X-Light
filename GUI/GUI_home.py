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
from tkinter.messagebox import *
from GUI.GUI_1D_stress import GUI_1D_stress
from GUI.GUI_2D_stress import GUI_2D_stress
from GUI.GUI_XEC import GUI_XEC
import pyFAI
from pyFAI.app.calib2 import main as run_pyFAI_calib
screen_width=1920
screen_height=1080
###########################################################################################################################################
######################## -----------------------------------------------###################################################################
def GUI_home(self):
    for widget in self.root.winfo_children():
        widget.destroy()
            
    menubar = Menu(self.root) # menu interface
    menu1 = Menu(menubar, tearoff=0)
    menu1.add_separator()
    menu1.add_command(label="Exit", command=lambda:root_exit(self))
    menubar.add_cascade(label="Files", menu=menu1)        
    menubar.add_command(label="About", command= lambda:about(self))

    self.root.config(menu=menubar)

    Frame0 = Frame(self.root, borderwidth=0, relief=GROOVE,width=screen_width*0.5,height=screen_height*0.1)
    Frame0.pack(expand=YES,side=TOP)

    Frame1 = Frame(self.root, borderwidth=0, relief=GROOVE,width=screen_width*0.5,height=screen_height)
    Frame1.pack(expand=YES,side=TOP)

    Frame2 = Frame(self.root, borderwidth=0, relief=GROOVE,width=screen_width*0.5,height=screen_height*0.5)
    Frame2.pack(expand=YES,side=TOP)

    Label(Frame0, text='PLEASE CHOOSE AN ANALYSIS!',bg="white").pack()

    #Buttons fonction
    Button(Frame1,text = '1D XRD STRESS',bg="white", command = lambda:GUI_1D_stress(self)).grid(column=0,row=0,ipadx=20,ipady=20,padx=20,pady=20)   #create 1D stress interface
    Button(Frame1,text = '2D XRD STRESS',bg="white", command = lambda:GUI_2D_stress(self)).grid(column=0,row=1,ipadx=20,ipady=20,padx=20,pady=20)   #create 1D stress interface
    Button(Frame1,text = '2D pyFAI-calib',bg="white", command = lambda:pyFAI_calib()).grid(column=0,row=2,ipadx=20,ipady=20,padx=20,pady=20)        #open pyFAI calib
    Button(Frame1,text = 'XEC ANALYSIS',bg="white", command = lambda:GUI_XEC(self)).grid(column=0,row=3,ipadx=20,ipady=20,padx=20,pady=20)          #create X-ray Elastic Constant interface
#-----------------------------------------------------------------------------------------------------------------------
def about(self):
    showinfo(title="About",message="X-Light-v1.1\nXRD Residual Stress Analysis\nCopy right: PHAM Tu Quoc Sang\n(sang.phamtuquoc@gmail.com)")
    self.root.mainloop()
#-----------------------------------------------------------------------------------------------------------------------
def root_exit(self):
    self.root.quit()
    self.root.destroy()
#-----------------------------------------------------------------------------------------------------------------------
def pyFAI_calib():
    result = run_pyFAI_calib()
    sys.exit(result)
