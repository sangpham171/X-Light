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
from tkinter.ttk import Progressbar
import math as math

def export_original_data(index,import_XRD,main):
    f=asksaveasfile(title="Export data",mode='w',defaultextension=".text",filetypes=[('text files','.txt'),('all files','.*')])
    if f is not None and f is not '':
        f.write("Wavelength=")
        for i in range(3):
            f.write(str(import_XRD.k_alpha[i])+'  ')
        f.write('\n')
        f.write("-------------\n")
        f.write("Phi="+str(import_XRD.phi[index])+"\n")
        f.write("Chi="+str(import_XRD.chi[index])+"\n")
        f.write("Omega="+str(import_XRD.omega[index])+"\n")
        f.write("2theta="+str(import_XRD.twotheta[index])+"\n")
        f.write("twotheta\t")
        f.write("intensity\n")

        for i in range(len(import_XRD.data_x[index])):
            f.write(str("%0.9f" % import_XRD.data_x[index][i])+"\t")
            f.write(str("%0.3f" % import_XRD.data_y[index][i])+"\n")
        f.close()
    main.root.mainloop()

def export_all_original_data(import_XRD,main):
    f=asksaveasfile(title="Export data",mode='w',defaultextension=".text",filetypes=[('text files','.txt'),('all files','.*')])
    if f is not None and f is not '':
        f.write("Wavelength=")
        for i in range(3):
            f.write(str(import_XRD.k_alpha[i])+'  ')
        f.write('\n')
        f.write("-------------\n")

        for i in range(len(import_XRD.phi)):
            f.write("Scan "+str(i+1)+'\n')
            f.write("Phi="+str(float(import_XRD.phi[i]))+"\n")
            f.write("Chi="+str(float(import_XRD.chi[i]))+"\n")
            f.write("Omega="+str(float(import_XRD.omega[i]))+"\n")
            f.write("2theta="+str(import_XRD.twotheta[i])+"\n")
            f.write("twotheta\t")
            f.write("intensity\n")

            for j in range(len(import_XRD.data_x[i])):
                f.write(str("%0.9f" % import_XRD.data_x[i][j])+"\t")
                f.write(str("%0.3f" % import_XRD.data_y[i][j])+"\n")
            f.write("-------------\n")
        f.close()
    main.root.mainloop()

def export_all_original_data_2(import_XRD,main):
    location=askdirectory(title="Please choose a directory")
    if location is not None and location is not '':
        for i in range(len(import_XRD.phi)):               
            name=str(location)+'/'+'scan_'+str(i+1)+'.txt'                 
            f=open(name,'w')

            for j in range(len(import_XRD.data_x[i])):
                f.write(str("%0.9f" % import_XRD.data_x[i][j])+"\t")
                f.write(str("%0.3f" % import_XRD.data_y[i][j])+"\n")
            f.close()
    main.root.mainloop()
    
def export_fit_data(index,main_calcul,main):
    f=asksaveasfile(title="Export data",mode='w',defaultextension=".text",filetypes=[('text files','.txt'),('all files','.*')])
    if f is not None and f is not '':     
        f.write("Phi="+str(main_calcul.phi[index])+"\n")
        f.write("Psi="+str(main_calcul.chi[index])+"\n")
        f.write("Omega="+str(main_calcul.omega[index])+"\n")
        f.write("a="+str(main_calcul.a[index])+"\n")
        f.write("r="+str(main_calcul.r[index])+"\n")
        f.write("pic 2 theta: "+str(main_calcul.peaks_position[index])+"\n")
        f.write(" twotheta\t")
        f.write("  original\t")
        f.write("background\t")
        f.write("substrat_background\t")
        f.write("   kalpha1\t")
        f.write("   kalpha2\t")
        f.write("fitting_pearson_vii\t")
        f.write("\n")

        for i in range(len(main_calcul.data_x_limit[index])):
            f.write(str("%10.4g" % main_calcul.data_x_limit[index][i])+"\t")
            f.write(str("%10.4g" % main_calcul.data_y_limit[index][i])+"\t")
            f.write(str("%10.4g" % main_calcul.data_y_background_fit[index][i])+"\t")
            f.write(str("%19.4g" % main_calcul.data_y_net[index][i])+"\t")
            f.write(str("%10.4g" % main_calcul.data_y_k1_fit[index][i])+"\t")
            f.write(str("%10.4g" % main_calcul.data_y_k2_fit[index][i])+"\t")
            f.write(str("%19.4g" % main_calcul.data_y_fit_total[index][i])+"\t")
            f.write("\n")
        f.close()
    main.root.mainloop()
#-------------------------------------------
def export_all_fit_data(main_calcul,main):
    f=asksaveasfile(title="Export data",mode='w',defaultextension=".txt",filetypes=[('text files','.txt'),('all files','.*')])
    if f is not None and f is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(main_calcul.phi)
        for i in range(len(main_calcul.peaks_position)):
            progress["value"] = progress["value"]+1
            progress.update()

            f.write("Range "+str(i+1)+"\n")
            f.write("Phi="+str(float(main_calcul.phi[i]))+"\n")
            f.write("Psi="+str(float(main_calcul.chi[i]))+"\n")
            f.write("Omega="+str(float(main_calcul.omega[i]))+"\n")
            f.write("a="+str(main_calcul.a[i])+"\n")
            f.write("r="+str(main_calcul.r[i])+"\n")
            f.write("pic 2 theta: "+str(main_calcul.peaks_position[i])+"\n")
            f.write("\n")
            f.write(" twotheta\t")
            f.write("  original\t")
            f.write("background\t")
            f.write("substrat_background\t")
            f.write("   kalpha1\t")
            f.write("   kalpha2\t")
            f.write("fitting_pearson_vii\t")
            f.write("\n")

            for j in range(len(main_calcul.data_x_limit[i])):
                try:
                    f.write(str("%10.4g" % main_calcul.data_x_limit[i][j])+"\t")
                    f.write(str("%10.4g" % main_calcul.data_y_limit[i][j])+"\t")
                    f.write(str("%10.4g" % main_calcul.data_y_background_fit[i][j])+"\t")
                    f.write(str("%19.4g" % main_calcul.data_y_net[i][j])+"\t")
                    f.write(str("%10.4g" % main_calcul.data_y_k1_fit[i][j])+"\t")
                    f.write(str("%10.4g" % main_calcul.data_y_k2_fit[i][j])+"\t")
                    f.write(str("%19.4g" % main_calcul.data_y_fit_total[i][j])+"\t")
                    f.write("\n")
                except (IndexError,ValueError):
                    pass
            f.write("--------------------------------------------------------------\n")
            f.write("\n")
        f.close()
        for widget in main.Frame1_2.winfo_children():
            widget.destroy() 
    main.root.mainloop()

#----------------------------------------------------
def export_all_stress_data(main_calcul,stress_calcul,main):
    f=asksaveasfile(title="Export data",mode='w',defaultextension=".text",filetypes=[('text files','.txt'),('all files','.*')])
    if f is not None and f is not '':
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()       
        Label(main.Frame1_2,text="Export").pack(side=LEFT)
        progress = Progressbar(main.Frame1_2,orient="horizontal",mode='determinate')
        progress.pack(side=LEFT)
        progress["value"] = 0
        progress["maximum"] = len(main_calcul.phi)+2
        
        if stress_calcul.stress_valid>=1:
            f.write("SIN2PSI METHOD\n")
            for i in range(len(stress_calcul.liste_phi)):
                f.write("Phi= "+str(stress_calcul.liste_phi[i])+"°")
                f.write("Linear fit: "+"sigma= "+str(stress_calcul.sigma_phi_linear[i])+"+/-"+str(stress_calcul.error_sigma_phi_linear[i])+"MPa"+"\n")
                f.write("Elliptic fit: "+"sigma= "+str(stress_calcul.sigma_phi_elliptic[i])+"+/-"+str(stress_calcul.error_sigma_phi_elliptic[i])+"MPa"+"\n")
                f.write("Elliptic fit: "+"shear= "+str(stress_calcul.shear_phi_elliptic[i])+"+/-"+str(stress_calcul.error_shear_phi_elliptic[i])+"MPa"+"\n")
                f.write("-------------------\n")
        f.write("---------------------------------------------------- \n")
        f.write("---------------------------------------------------- \n")  

        progress["value"] = progress["value"]+1
        progress.update()
        f.write("FUNDAMENTAL METHOD \n")
        if len(stress_calcul.liste_phi)>=1 and stress_calcul.length_strain==3:
            f.write("---Biaxial stress----- \n")
            f.write('sigma 11 = '+str(stress_calcul.tensor_biaxial[0][0])+"+/-"+str(stress_calcul.tensor_biaxial[1][0,0]**0.5)+"MPa"+"\n")
            f.write('sigma 22 = '+str(stress_calcul.tensor_biaxial[0][1])+"+/-"+str(stress_calcul.tensor_biaxial[1][1,1]**0.5)+"MPa"+"\n")     
            f.write("---------------------- \n")

        if len(stress_calcul.liste_phi)>=1 and stress_calcul.length_strain==4:
            f.write("---Biaxial stress----- \n")
            f.write('sigma 11 = '+str(stress_calcul.tensor_biaxial[0][0])+"+/-"+str(stress_calcul.tensor_biaxial[1][0,0]**0.5)+"MPa"+"\n")
            f.write('sigma 22 = '+str(stress_calcul.tensor_biaxial[0][2])+"+/-"+str(stress_calcul.tensor_biaxial[1][2,2]**0.5)+"MPa"+"\n")     
            f.write('sigma 12 = sigma 21 = '+str(stress_calcul.tensor_biaxial[0][1])+"+/-"+str(stress_calcul.tensor_biaxial[1][1,1]**0.5)+"MPa"+"\n")
            f.write("---------------------- \n")

        if len(stress_calcul.liste_phi)>=1 and stress_calcul.length_strain==5:     
            f.write("---Biaxial+shear stress----- \n")
            f.write('sigma 11 = '+str(stress_calcul.tensor_biaxial_shear[0][0])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][0,0]**0.5)+"MPa"+"\n")
            f.write('sigma 22 = '+str(stress_calcul.tensor_biaxial_shear[0][1])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][1,1]**0.5)+"MPa"+"\n")     
            f.write('sigma 13 = sigma 31 = '+str(stress_calcul.tensor_biaxial_shear[0][2])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][2,2]**0.5)+"MPa"+"\n")
            f.write('sigma 23 = sigma 32 = '+str(stress_calcul.tensor_biaxial_shear[0][3])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][3,3]**0.5)+"MPa"+"\n")
            f.write("---------------------- \n")

        if len(stress_calcul.liste_phi)>=1 and stress_calcul.length_strain>=6:  
            f.write("---Biaxial+shear stress----- \n")
            f.write('sigma 11 = '+str(stress_calcul.tensor_biaxial_shear[0][0])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][0,0]**0.5)+"MPa"+"\n")   
            f.write('sigma 22 = '+str(stress_calcul.tensor_biaxial_shear[0][2])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][2,2]**0.5)+"MPa"+"\n")
            f.write('sigma 12 = sigma 12 = '+str(stress_calcul.tensor_biaxial_shear[0][1])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][1,1]**0.5)+"MPa"+"\n") 
            f.write('sigma 13 = sigma 31 = '+str(stress_calcul.tensor_biaxial_shear[0][3])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][3,3]**0.5)+"MPa"+"\n")
            f.write('sigma 23 = sigma 32 = '+str(stress_calcul.tensor_biaxial_shear[0][4])+"+/-"+str(stress_calcul.tensor_biaxial_shear[1][4,4]**0.5)+"MPa"+"\n")
            f.write("---------------------- \n")

        if len(stress_calcul.liste_phi)>=1 and stress_calcul.length_strain>=6:
            f.write("---Triaxial stress----- \n")
            f.write('sigma 11 = '+str(stress_calcul.tensor_triaxial[0][0])+"+/-"+str(stress_calcul.tensor_triaxial[1][0,0]**0.5)+"MPa"+"\n")
            f.write('sigma 22 = '+str(stress_calcul.tensor_triaxial[0][2])+"+/-"+str(stress_calcul.tensor_triaxial[1][2,2]**0.5)+"MPa"+"\n")     
            f.write('sigma 12 = sigma 21 = '+str(stress_calcul.tensor_triaxial[0][1])+"+/-"+str(stress_calcul.tensor_triaxial[1][1,1]**0.5)+"MPa"+"\n")
            f.write('sigma 13 = sigma 31 = '+str(stress_calcul.tensor_triaxial[0][3])+"+/-"+str(stress_calcul.tensor_triaxial[1][3,3]**0.5)+"MPa"+"\n")
            f.write('sigma 23 = sigma 32 = '+str(stress_calcul.tensor_triaxial[0][4])+"+/-"+str(stress_calcul.tensor_triaxial[1][4,4]**0.5)+"MPa"+"\n")
            f.write('sigma 33 = '+str(stress_calcul.tensor_triaxial[0][5])+"+/-"+str(stress_calcul.tensor_triaxial[1][5,5]**0.5)+"MPa"+"\n")
            f.write("---------------------- \n")
                
        f.write("---------------------------------------------------- \n")
        f.write("---------------------------------------------------- \n")                 

        f.write("phi(°)    chi(°)     omega(°)    peak_2theta(°)    phi(°)     psi(°)\n")
        for i in range(len(stress_calcul.phi_regroup)):
            progress["value"] = progress["value"]+1
            progress.update()
            f.write(str("%3.4g" % main_calcul.phi[i]))
            f.write(str("%10.4g" % main_calcul.chi[i]))
            f.write(str("%10.4g" % main_calcul.omega[i]))
            f.write(str("%10.4g" % stress_calcul.peaks_position[i]))
            f.write(str("%15.4g" % stress_calcul.phi_regroup[i]))
            f.write(str("%15.4g" % stress_calcul.psi_regroup[i]))
            f.write("\n")
        f.close()
        for widget in main.Frame1_2.winfo_children():
            widget.destroy()  
    main.root.mainloop()

def export_strain_sin2psi_data(i_stress,stress_calcul,main):
    f=asksaveasfile(title="Export strain",mode='w',defaultextension=".ssd",filetypes=[('.ssd','.ssd'),('all files','.*')])
    if f is not None and f is not '':
        f.write("Linear_fit: a="+str(stress_calcul.a[i_stress])+"   b="+str(stress_calcul.b[i_stress])+"\n")
        f.write("Linear_fit_erros: error_a="+str(stress_calcul.er_a[i_stress])+"   error_b="+str(stress_calcul.er_b[i_stress])+"\n")
        f.write("sin2psi      strain\n")

        j=-1
        for i in range(len(stress_calcul.phi_regroup)):
            if str(i+1) in stress_calcul.list_graph_error:
                continue
            if stress_calcul.phi_regroup[i]==stress_calcul.liste_phi[i_stress]:
                j=j+1
                f.write(str(stress_calcul.sinpsi_2[i_stress][j]))
                f.write("        ")
                f.write(str(stress_calcul.strain[i_stress][j]))
                f.write("\n")
        f.close()
    main.root.mainloop()
