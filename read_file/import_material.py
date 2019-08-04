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
import os.path
import math as math
class import_material:
    def __init__(self,mat,Frame_1):
        if getattr(sys, 'frozen', False):
            path = sys._MEIPASS
        elif __file__:
            path = os.path.dirname(__file__)
            
        filename = 'mat_database.mdb'
        filepath=os.path.join(path, filename)
        try:
            self.optionmenu1.grid_forget()
            self.optionmenu2.grid_forget()
            self.optionmenu3.grid_forget()
        except (UnboundLocalError,AttributeError):
            pass

        f_open = open(filepath, "r")
        matrix_material_data=[]
        material_data=[]
        number_line=0
        line_text=f_open.readline()
        #read line by line
        while line_text is not None and line_text is not "":
            number_line=number_line+1
            material_info=line_text
            material_info=material_info.split()
            material_data=[]
            for i in range(len(material_info)):
                material_data.append(material_info[i])
            matrix_material_data.append(material_data)

            line_text=f_open.readline()

        filename = 'x_ray_source.xrs'
        filepath=os.path.join(path, filename)

        f_open = open(filepath, "r")
        self.liste_source=[]
        self.lamda=[]
        ka1=[]
        ka2=[]
        
        line_text=f_open.readline()
        line_text=f_open.readline()
        while line_text is not None and line_text is not "":
            line_text=line_text.split()
            self.liste_source.append(line_text[0])
            ka1.append(float(line_text[1]))
            ka2.append(float(line_text[2]))
            line_text=f_open.readline()
        self.lamda.append(ka1)
        self.lamda.append(ka2)
        #re-organise matrix material by name,source,plan
        self.matrix_material=[]
        for j in range(len(matrix_material_data[0])):
            data=[]
            for i in range(len(matrix_material_data)):
                data.append(matrix_material_data[i][j])
            self.matrix_material.append(data)

        liste_material=[]
        for i in range(1,len(self.matrix_material[0])): 
            if self.matrix_material[0][i] not in liste_material:
                liste_material.append(self.matrix_material[0][i])

        master=Frame_1
        variable = StringVar(Frame_1)
        variable.set(self.matrix_material[0][0]) # default value
        self.optionmenu1=OptionMenu(master, variable,*liste_material,command=lambda value:self.option1(value,mat,Frame_1))
        self.optionmenu1.grid(row=1,column=1,sticky=W)
  
    #----------------------------------------------------------------
    def option1(self,value,mat,Frame_1):
        try:
            self.optionmenu2.grid_forget()
            self.optionmenu3.grid_forget()
        except (UnboundLocalError,AttributeError):
            pass

        mat.Entry_twotheta0.delete(0,END)        
        mat.Entry_s1.delete(0,END)
        mat.Entry_half_s2.delete(0,END)
        mat.Entry_Young.delete(0,END)
        mat.Entry_Poisson.delete(0,END)

        mat.Entry_peak[0].delete(0,END)
        
        self.index_source=[]
        for i in range(1,len(self.matrix_material[0])):
            if value == self.matrix_material[0][i]:
                self.index_source.append(i)
                    
        master=Frame_1
        variable = StringVar(Frame_1)
        variable.set(self.matrix_material[1][0]) # default value
        self.optionmenu2=OptionMenu(master, variable,*self.liste_source,command=lambda value:self.option2(value,mat,Frame_1))
        self.optionmenu2.grid(row=2,column=1,sticky=W)

    #----------------------------------------------------------------
    def option2(self,value,mat,Frame_1):
        try:
            self.optionmenu3.grid_forget()
        except (UnboundLocalError,AttributeError):
            pass

        mat.Entry_twotheta0.delete(0,END)
        mat.Entry_s1.delete(0,END)
        mat.Entry_half_s2.delete(0,END)
        mat.Entry_Young.delete(0,END)
        mat.Entry_Poisson.delete(0,END)
        mat.Entry_peak[0].delete(0,END)

        liste_2theta0=[]
        self.index_2theta0=[]

        for i in self.index_source:
            self.index_2theta0.append(i)

        for i in range(len(self.liste_source)):
            if self.liste_source[i]==value:
                lamda_2=self.lamda[0][i]
                mat.Entry_kalpha[0].delete(0,END)
                mat.Entry_kalpha[1].delete(0,END)
                mat.Entry_kalpha[0].insert(0,str(self.lamda[0][i]))
                mat.Entry_kalpha[1].insert(0,str(self.lamda[1][i]))
                                             
        for i in self.index_2theta0:
            for j in range(len(self.liste_source)):
                if self.liste_source[j] in self.matrix_material[1][i]:
                    lamda_1=self.lamda[0][j]
                
            try:
                twotheta0= 2*math.degrees(math.asin((lamda_2/lamda_1)*math.sin(math.radians(float(self.matrix_material[2][i])/2))))
            except ValueError:
                pass
            else:
                liste_2theta0.append("{"+str(self.matrix_material[3][i])+"} "+str("%0.3f" % twotheta0))

        master=Frame_1
        variable = StringVar(Frame_1)
        variable.set(self.matrix_material[2][0]) # default value
        self.optionmenu3=OptionMenu(master, variable,*liste_2theta0,command=lambda value:self.option3(value,mat,Frame_1))
        self.optionmenu3.grid(row=3,column=1,sticky=W)
   
    #----------------------------------------------------------------
    def option3(self,value,mat,Frame_1):
        twotheta=value.split()[1]

        mat.Entry_peak[0].delete(0,END)
        mat.Entry_peak[0].insert(0,str(twotheta))
        
        for i in self.index_2theta0:
            if self.matrix_material[3][i] in value:
                index=i

        mat.Entry_twotheta0.delete(0,END)
        mat.Entry_s1.delete(0,END)
        mat.Entry_half_s2.delete(0,END)
        mat.Entry_Young.delete(0,END)
        mat.Entry_Poisson.delete(0,END)

        mat.Entry_twotheta0.insert(0,twotheta)
        mat.Entry_s1.insert(0,str(self.matrix_material[4][index]))
        mat.Entry_half_s2.insert(0,str(self.matrix_material[5][index]))
        mat.Entry_Young.insert(0,str(self.matrix_material[6][index]))
        mat.Entry_Poisson.insert(0,str(self.matrix_material[7][index]))  
