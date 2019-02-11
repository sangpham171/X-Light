from tkinter import *

def fig_style(self,Frame_1):
    t=["Fig size = ",       #0
       "Font size = ",      #1
       "Marker style = ",   #2
       "Marker size = ",    #3
       "Color = ",          #4
       "Line style = ",     #5
       "dpi ="]             #6
    val=["10,10",
         "10",
         "o",
         "2",
         "g",
         "",
         "100"]
    Label(Frame_1,text="Figure style",bg="white").grid(row=0,column=0,sticky=W)        
    self.Entry_fig=[]
    for i in range(len(t)):
        Label(Frame_1,text=t[i]).grid(row=i+1,column=0,sticky=W)
        self.Entry_fig.append(Entry(Frame_1,width=10))
        self.Entry_fig[i].insert(0,val[i])
        self.Entry_fig[i].grid(row=i+1,column=1,sticky=W)
