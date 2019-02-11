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
def delete_peak(self,Frame_1):
    self.Label_1[self.number_peak-2].grid_forget()
    self.Label_2[self.number_peak-2].grid_forget()
    self.Label_3[self.number_peak-2].grid_forget()

    del self.Label_1[self.number_peak-2]
    del self.Label_2[self.number_peak-2]
    del self.Label_3[self.number_peak-2]
        
    self.Entry_peak[self.number_peak-1].grid_forget()
    self.Entry_limit_peak[self.number_peak-1].grid_forget()
    self.Entry_peak_width[self.number_peak-1].grid_forget()

    del self.Entry_peak[self.number_peak-1]
    del self.Entry_limit_peak[self.number_peak-1]
    del self.Entry_peak_width[self.number_peak-1]

    self.row_i=self.row_i-3
    self.number_peak=self.number_peak-1

    self.add_peak.grid(row=self.row_i,column=0,sticky=W)
    if self.number_peak>1:
        self.delete_peak.grid(row=self.row_i,column=1,sticky=W)
    else:
        self.delete_peak.grid_forget()
    
def add_peak(self,Frame_1):
    self.Label_1.append(Label(Frame_1, text=" "))
    self.Label_1[self.number_peak-1].grid(row=self.row_i,column=0,sticky=W)
    self.Label_2.append(Label(Frame_1, text='2,3,...'))
    self.Label_2[self.number_peak-1].grid(row=self.row_i+1,column=0,sticky=W)
    self.Label_3.append(Label(Frame_1, text=u"\u00B1(°)(optional)"))
    self.Label_3[self.number_peak-1].grid(row=self.row_i+2,column=0,sticky=W)
    
    self.Entry_peak.append(Entry(Frame_1,width=10))
    self.Entry_limit_peak.append(Entry(Frame_1,width=10))
    self.Entry_peak_width.append(Entry(Frame_1,width=10))
        
    self.Entry_peak[self.number_peak].grid(row=self.row_i+1, column=1,sticky=W)
    self.Entry_limit_peak[self.number_peak].grid(row=self.row_i+2, column=1,sticky=W)
    self.Entry_peak_width[self.number_peak].grid(row=self.row_i+1, column=2,sticky=W)

    self.row_i=self.row_i+3
    self.number_peak=self.number_peak+1

    self.add_peak.grid_forget()
    self.delete_peak.grid(row=self.row_i,column=1,sticky=W)
        

