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
   
def import_poni_parameters(self,main):
    f = askopenfilename(title="File.PONI",filetypes=[('PONI files','*.PONI;*.edf'),('all files','.*')])
    if f is not None and f is not '':
        f_open=open(f,"r")
        data=0
        line_text="0"
        try:
            while line_text is not None and line_text is not "":
                line_text=f_open.readline()
                if "pixel1" in line_text:
                    line_text=line_text.replace(",","")
                    line_text=line_text.replace("}","")
                    info=line_text.split()
                    
                    self.Entry_pixel_1.delete(0,END)
                    self.Entry_pixel_1.insert(0,info[2])

                    self.Entry_pixel_2.delete(0,END)
                    self.Entry_pixel_2.insert(0,info[4])

                    data=data+2
                    
                if "PixelSize1" in line_text:
                    self.Entry_pixel_1.delete(0,END)
                    self.Entry_pixel_1.insert(0,line_text.split()[1])
                    data=data+1
                if "PixelSize2" in line_text:
                    self.Entry_pixel_2.delete(0,END)
                    self.Entry_pixel_2.insert(0,line_text.split()[1])
                    data=data+1
                if "Distance" in line_text:
                    self.Entry_distance_calib.delete(0,END)
                    self.Entry_distance_calib.insert(0,line_text.split()[1])
                    data=data+1
                if "Poni1" in line_text:
                    self.Entry_poni_1.delete(0,END)
                    self.Entry_poni_1.insert(0,line_text.split()[1])
                    data=data+1
                if "Poni2" in line_text:
                    self.Entry_poni_2.delete(0,END)
                    self.Entry_poni_2.insert(0,line_text.split()[1])
                    data=data+1
                if "Rot1" in line_text:
                    self.Entry_rot_1.delete(0,END)
                    self.Entry_rot_1.insert(0,line_text.split()[1])
                    data=data+1
                if "Rot2" in line_text:
                    self.Entry_rot_2.delete(0,END)
                    self.Entry_rot_2.insert(0,line_text.split()[1])
                    data=data+1
                if "Rot3" in line_text:
                    self.Entry_rot_3.delete(0,END)
                    self.Entry_rot_3.insert(0,line_text.split()[1])
                    data=data+1
                if "Wavelength" in line_text:
                    self.Entry_wl_calib.delete(0,END)
                    self.Entry_wl_calib.insert(0,line_text.split()[1])
                    data=data+1
        except Exception as e:
            showinfo(title="Warning",message="Wrong format:"+e)

        if data<9:
            showinfo(title="Warning",message="Some calib parameters are missing\nPlease complete by insert manually")

    main.root.mainloop()
