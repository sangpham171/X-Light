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
import os.path
import sys
from tkinter import *
from GUI.GUI_home import GUI_home, about, root_exit
sys.setrecursionlimit(10000)
import warnings
warnings.filterwarnings("ignore")
###########################################################################################################################################
######################## -----------------------------------------------###################################################################
###########################################################################################################################################
class main:
    def __init__(self):
        self.root = Tk()
        try:
            self.root.wm_state('zoomed')
        except Exception:
            pass
        self.root.title('X-Light 1.1')

        if getattr(sys, 'frozen', False):
            path = sys._MEIPASS
        elif __file__:
            path =os.path.dirname(__file__)
        filename = 'X-Light.gif'
        
        img=PhotoImage(file=os.path.join(path, filename))
        try:
            self.root.wm_iconphoto(True,img)
        except Exception:
            pass
        #self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        #self.root.iconbitmap(default=os.path.join(path, filename))

        GUI_home(self)
        self.root.mainloop()
    #-----------------------------------------------------------------------------------------------------------------------

main()
