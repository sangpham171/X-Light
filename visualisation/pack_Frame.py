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
def pack_Frame_1D(self,index):
    for i in range(1,len(self.Frame3_)):
        self.Frame3_[i].pack_forget()
        self.Button3_[i].config(bg="gray94")
   
    self.Frame3_[index].pack()
    self.Button3_[index].config(bg="white")

    if index<7:
        self.Button_next.config(command=lambda:pack_Frame_1D(self,index+1))
    if index==7:
        self.Button_next.config(command=lambda:pack_Frame_1D(self,7))
    if index>1:
        self.Button_prev.config(command=lambda:pack_Frame_1D(self,index-1))
    if index==1:
        self.Button_prev.config(command=lambda:pack_Frame_1D(self,1))
    self.root.mainloop()

def pack_Frame_2D(self,index): 
    for i in range(1,len(self.Frame3_)):
        self.Frame3_[i].pack_forget()
        self.Button3_[i].config(bg="gray94")

    self.Frame3_[index].pack()
    self.Button3_[index].config(bg="white")

    if index<8:
        self.Button_next.config(command=lambda:pack_Frame_2D(self,index+1))
    if index==8:
        self.Button_next.config(command=lambda:pack_Frame_2D(self,8))
    if index>1:
        self.Button_prev.config(command=lambda:pack_Frame_2D(self,index-1))
    if index==1:
        self.Button_prev.config(command=lambda:pack_Frame_2D(self,1))
        
    self.root.mainloop()


def pack_Frame_XEC(self,Frame_pack,button_pack): 
    self.Frame3_1.pack_forget()
    self.Frame3_2.pack_forget()
    self.Frame3_3.pack_forget()
    self.Button3_1.config(bg="gray94")
    self.Button3_2.config(bg="gray94")
    self.Button3_3.config(bg="gray94")
    Frame_pack.pack()
    button_pack.config(bg="white")
    self.root.mainloop()

