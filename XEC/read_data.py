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
from tkinter.messagebox import *
def read_strain(f,filename,import_strain):
    f_open = open(f, "r", encoding="utf-8",errors='ignore')
    try:
        line_text=f_open.readline()
        line_text=line_text.split()
        import_strain.slope.append(float(line_text[1].split('=')[1].rstrip()))
        import_strain.interception.append(float(line_text[2].split('=')[1].rstrip()))

        line_text=f_open.readline()
        line_text=line_text.split()
        import_strain.er_slope.append(float(line_text[1].split('=')[1].rstrip()))
        import_strain.er_interception.append(float(line_text[2].split('=')[1].rstrip()))

        f_open.readline()
        strain=[]
        sin2psi=[]
        line_text=f_open.readline()
        while line_text is not '':                               
            line_text=line_text.split()
            strain.append(float(line_text[1].rstrip()))
            sin2psi.append(float(line_text[0].rstrip()))
            line_text=f_open.readline()
        import_strain.strain.append(strain)
        import_strain.sin2psi.append(sin2psi)
    except (ValueError,IndexError):
        showinfo(title="Warning",message="File "+str(filename)+" error")

def read_load(import_load):
    f_open = open(import_load.f, "r", encoding="utf-8",errors='ignore')
    i=0
    line_text=f_open.readline()
    while line_text is not '' and line_text is not None:
        i=i+1
        try:
            import_load.load.append(float(line_text.rstrip()))
            import_load.load_number.append(i)
        except ValueError:
            i=i-1
        line_text=f_open.readline()
            
        
