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
import numpy as np
from scipy.optimize import curve_fit

def F_linear(x,a,b):
    return a*x+b

def F_elliptic(x,a,b,c):
    return a*x[0]+b*x[1]+c

def tensor_biaxial_simple(p,sigma11,sigma22,sigma_ph):
    return p[0]*sigma11+p[1]*sigma22+p[2]*sigma_ph

def tensor_biaxial(p,sigma11,sigma12,sigma22,sigma_ph):
    return p[0]*sigma11+p[1]*sigma12+p[2]*sigma22+p[3]*sigma_ph

def tensor_biaxial_simple_shear(p,sigma11,sigma22,sigma13,sigma23,sigma_ph):
    return p[0]*sigma11+p[1]*sigma22+p[2]*sigma13+p[3]*sigma23+p[4]*sigma_ph

def tensor_biaxial_shear(p,sigma11,sigma12,sigma22,sigma13,sigma23,sigma_ph):
    return p[0]*sigma11+p[1]*sigma12+p[2]*sigma22+p[3]*sigma13+p[4]*sigma23+p[5]*sigma_ph

def tensor_triaxial(p,sigma11,sigma12,sigma22,sigma13,sigma23,sigma33):
    return p[0]*sigma11+p[1]*sigma12+p[2]*sigma22+p[3]*sigma13+p[4]*sigma23+p[5]*sigma33

def Curve_Fit(F,x,y,err):
    try:
        for Method in ('lm','trf','dogbox'):
            for i in range(10):
                try:
                    val_cov= curve_fit(F,x,y,sigma=err,method=Method)
                except Exception:
                    pass
                else:
                    if True in np.isinf(np.diag(val_cov[1])):
                        pass
                    else:
                        raise StopIteration
    except StopIteration:
        pass
    
    return val_cov

class stress_calcul:
    def remove_peaks_list(self,main_calcul):
        self.list_graph_error=[]
        for i in range(len(main_calcul.peak_non_valide)):
            self.list_graph_error.append(str(main_calcul.peak_non_valide[i]))
        for i in range(len(main_calcul.peak_rejection)):
            self.list_graph_error.append(str(main_calcul.peak_rejection[i]))
        
        list_graph_error_entry=main_calcul.Entry_peak_remove.get()
        if list_graph_error_entry and list_graph_error_entry.strip():
            list_graph_error=list_graph_error_entry.split(",")
            for i in range(len(list_graph_error)):
                if list_graph_error[i] not in self.list_graph_error:
                    self.list_graph_error.append(list_graph_error[i])
    #-----------------------------------------
    def selec_peaks(self,main_calcul):
        peak_shift_correction_coefficient=[]
        
        if len(main_calcul.peak_shift_correction_coefficient)>=1:
            data_x=[] #[2theta1,2theta2,...]
            for i in range(len(main_calcul.peak_shift_correction_coefficient)):
                data_x.append(main_calcul.peak_shift_correction_coefficient[i][0])

            len_coef=len(main_calcul.peak_shift_correction_coefficient[0]) #max degree
                
            data_y=[] #[[degree_0_2theta1,degree_0_2theta2,...],[degree_1_2theta1,degree_1_2theta2,...],...]
            for i in range(1,len_coef):
                data=[]
                for j in range(len(main_calcul.peak_shift_correction_coefficient)):
                    data.append(main_calcul.peak_shift_correction_coefficient[j][i])
                data_y.append(data)
            
            for i in range(len(data_y)): #len(data_y)=max degree fit
                if len(data_y[i])==1:
                    val=data_y[i][0]
                elif len(data_y[i])>1:
                    if main_calcul.twotheta0 < min(data_x) or main_calcul.twotheta0 > max(data_x):
                        poly_coef=np.polyfit(data_x,data_y[i],1)
                        val=poly_coef[0]*main_calcul.twotheta0 + poly_coef[1]
                    else:
                        a=float('inf')
                        b=-float('inf')
                        index_1=0
                        index_2=0
                        for j in range(len(data_x)):
                            c=data_x[j]-main_calcul.twotheta0
                            if c>0 and c<a:
                                a=c
                                index_1=j
                            if c<0 and c>b:
                                b=c
                                index_2=j

                        poly_coef=np.polyfit([data_x[index_1],data_x[index_2]],[data_y[i][index_1],data_y[i][index_2]],1)
                        val=poly_coef[0]*main_calcul.twotheta0 + poly_coef[1]
                peak_shift_correction_coefficient.append(val)
        
        self.peaks_position=[]
        self.error_peaks_position=[]
        for i in range (len(main_calcul.phi)):
            if str(i+1) in self.list_graph_error:
                self.peaks_position.append(float('NaN'))
                self.error_peaks_position.append(float('NaN'))
                continue
            else:
                peak_shift=0
                for j in range(len(peak_shift_correction_coefficient)):
                    peak_shift=peak_shift+peak_shift_correction_coefficient[j]*abs(main_calcul.chi[i])**j
                    
                self.peaks_position.append(main_calcul.peaks_position[i]-peak_shift*main_calcul.twotheta0/100)
                self.error_peaks_position.append(main_calcul.error_peaks_position[i])
                           
    #-----------------------------------------
    def convert_angles_gonio_sampling(self,main_calcul):
        self.phi_sampling=[]
        self.psi_sampling=[]
        self.phi_sampling_2=[]
        for i in range (len(main_calcul.phi)):
            if str(i+1) in self.list_graph_error:
                self.phi_sampling.append(float('NaN'))
                self.phi_sampling_2.append(float('NaN'))
                self.psi_sampling.append(float('NaN'))
            else:
                cos_theta=np.cos(np.radians(self.peaks_position[i]/2))                  
                sin_theta=np.sin(np.radians(self.peaks_position[i]/2))
                cos_omega=np.cos(np.radians(main_calcul.omega[i]))
                sin_omega=np.sin(np.radians(main_calcul.omega[i]))
                cos_chi=np.cos(np.radians(main_calcul.chi[i]))
                sin_chi=np.sin(np.radians(main_calcul.chi[i]))

                cos_psi_sampling=cos_theta*cos_chi*cos_omega+sin_theta*cos_chi*sin_omega
                
                if cos_psi_sampling>1:
                    self.list_graph_error.append(str(i+1))
                    self.phi_sampling.append(float('NaN'))
                    self.psi_sampling.append(float('NaN'))
                else:
                    self.psi_sampling.append(np.sign(main_calcul.chi[i])*np.degrees(np.arccos(cos_psi_sampling)))
                
                tan_delta_phi_sampling=(cos_theta*sin_chi*cos_omega+sin_theta*sin_chi*sin_omega)/(cos_theta*sin_omega-sin_theta*cos_omega)
                if 0<=np.degrees(np.arctan(tan_delta_phi_sampling))<10:
                    delta_phi_sampling=0
                elif 80<np.degrees(np.arctan(tan_delta_phi_sampling))<=90:
                    delta_phi_sampling=90
                else:
                    delta_phi_sampling=round(np.degrees(np.arctan(tan_delta_phi_sampling)))
                    
                self.phi_sampling.append(main_calcul.phi[i]+np.degrees(np.arctan(tan_delta_phi_sampling)))
                self.phi_sampling_2.append(main_calcul.phi[i])
    #-----------------------------------------
    def other_info(self,main_calcul):
        self.psi_calib=[]
        self.chi_calib=[]
        self.phi_calib=[]
        self.peak_shift=[]
        for i in range (len(main_calcul.phi)):
            if str(i+1) in self.list_graph_error:
                continue
            self.psi_calib.append(self.psi_sampling[i])
            self.chi_calib.append(main_calcul.chi[i])
            self.phi_calib.append(self.phi_sampling_2[i])
            self.peak_shift.append(100*(self.peaks_position[i]-main_calcul.twotheta0)/main_calcul.twotheta0)
    #-----------------------------------------
    def regroup_phi_psi(self):
        self.phi_regroup=self.phi_sampling_2*1
        self.psi_regroup=self.psi_sampling*1
        
        self.liste_phi=[]
        for i in range(len(self.phi_regroup)):
            if (True not in (np.isnan((self.phi_regroup[i],self.psi_regroup[i])))) and (True not in (np.isinf((self.phi_regroup[i],self.psi_regroup[i])))):
                for j in range(len(self.liste_phi)):
                    if self.phi_regroup[i]==self.liste_phi[j]+180 or self.phi_regroup[i]==self.liste_phi[j]-180:
                        self.phi_regroup[i]=self.liste_phi[j]
                        self.psi_regroup[i]=-self.psi_regroup[i]
                        break
                if self.phi_regroup[i] not in self.liste_phi:
                    self.liste_phi.append(self.phi_regroup[i])
  
        self.index_psi=[];        self.psi=[];
        self.sinpsi_2=[];         self.sin_2psi=[]
        self.psi_sorted=[];       self.sinpsi_2_sorted=[]
        
        for i in range(len(self.liste_phi)):
            index_psi=[];       psi=[]
            sin_2psi=[];        sinpsi_2=[]
            for j in range(len(self.phi_regroup)):
                if np.isnan(self.phi_regroup[j])==False and (np.isinf(self.phi_regroup[j])==False) and self.phi_regroup[j]==self.liste_phi[i] and str(j+1) not in self.list_graph_error:
                    index_psi.append(j+1)
                    psi.append(self.psi_regroup[j])
                    sinpsi_2.append((np.sin(np.radians(self.psi_regroup[j])))**2)
                    sin_2psi.append(np.sin(np.radians(2*self.psi_regroup[j])))

            psi_sorted=sorted(psi)
            sinpsi_2_sorted=[]
            for j in range(len(psi_sorted)):
                sinpsi_2_sorted.append((np.sin(np.radians(psi_sorted[j])))**2)
                
            self.index_psi.append(index_psi)
            self.psi.append(psi)
            self.psi_sorted.append(psi_sorted)
            self.sinpsi_2.append(sinpsi_2)
            self.sin_2psi.append(sin_2psi)
            self.sinpsi_2_sorted.append(sinpsi_2_sorted)

    def regroup_strain(self,main_calcul):
        self.strain=[];
        self.error_strain=[]
        for i in range(len(self.liste_phi)):
            strain=[];
            error_strain=[] 
            for j in range(len(self.phi_regroup)):
                if np.isnan(self.phi_regroup[j])==False and self.phi_regroup[j]==self.liste_phi[i] and str(j+1) not in self.list_graph_error:
                    strain.append(np.sin(np.radians(main_calcul.twotheta0/2))/np.sin(np.radians(self.peaks_position[j]/2))-1)
                    error_strain.append(abs(np.radians(self.error_peaks_position[j]/2)*
                                            np.cos(np.radians(self.peaks_position[j]/2))*
                                            np.sin(np.radians(main_calcul.twotheta0/2))/
                                            np.sin(np.radians(self.peaks_position[j]/2))**2))

            self.strain.append(strain)
            self.error_strain.append(error_strain)
            
    #-----------------------------------------
    def method_sin2psi(self,main_calcul):
        self.remove_peaks_list(self,main_calcul)
        self.selec_peaks(self,main_calcul)
        self.convert_angles_gonio_sampling(self,main_calcul)
        self.other_info(self,main_calcul)
        self.regroup_phi_psi(self)
        self.regroup_strain(self,main_calcul)
          
        self.strain_linear_fit=[];          self.strain_elliptical_fit=[]
        self.sigma_phi_linear=[];           self.error_sigma_phi_linear=[]
        self.sigma_phi_elliptic=[];         self.error_sigma_phi_elliptic=[]; 
        self.shear_phi_elliptic=[];         self.error_shear_phi_elliptic=[]
        shear_phi_elliptic=[]
        
        self.a=[];      self.er_a=[]
        self.b=[];      self.er_b=[]
        c=[];           er_c=[]

        self.stress_valid=0
        
        for i in range(len(self.liste_phi)):
            if len(self.psi[i])>=3:
                self.stress_valid=self.stress_valid+1
                #fitting linear
                x=self.sinpsi_2[i]
                val_cov=Curve_Fit(F_linear,x,self.strain[i],self.error_strain[i])
                val=val_cov[0]
                cov=val_cov[1]
                self.a.append(val[0])
                self.er_a.append(np.sqrt(cov[0,0]))
                self.b.append(val[1])
                self.er_b.append(np.sqrt(cov[1,1]))
                self.sigma_phi_linear.append(val[0]/main_calcul.s2_2)
                self.error_sigma_phi_linear.append((np.sqrt(cov[0,0]))/main_calcul.s2_2)

                strain_linear_fit=[]
                for j in range(len(self.psi_sorted[i])):
                    strain_linear_fit.append(val[0]*(np.sin(np.radians(self.psi_sorted[i][j])))**2+val[1])
                self.strain_linear_fit.append(strain_linear_fit)

                #fitting elliptic
                x=[]
                x.append(self.sinpsi_2[i])
                x.append(self.sin_2psi[i])
                
                val_cov=Curve_Fit(F_elliptic,x,self.strain[i],self.error_strain[i])
                val=val_cov[0]
                cov=val_cov[1]
                c.append(val[2])
                er_c.append(np.sqrt(cov[2,2]))
                self.sigma_phi_elliptic.append(val[0]/main_calcul.s2_2)
                shear_phi_elliptic.append(val[1]/main_calcul.s2_2)
                self.shear_phi_elliptic.append(abs(val[1])/main_calcul.s2_2)
                self.error_sigma_phi_elliptic.append((np.sqrt(cov[0,0]))/main_calcul.s2_2)
                self.error_shear_phi_elliptic.append((np.sqrt(cov[1,1]))/main_calcul.s2_2)

                strain_elliptical_fit=[]
                for j in range(len(self.psi_sorted[i])):
                    strain_elliptical_fit.append(val[0]*(np.sin(np.radians(self.psi_sorted[i][j])))**2+val[1]*(np.sin(np.radians(2*self.psi_sorted[i][j])))+val[2])
         
                self.strain_elliptical_fit.append(strain_elliptical_fit)
            else:
                self.a.append(float('NaN'))
                self.er_a.append(float('NaN'))
                self.b.append(float('NaN'))
                self.er_b.append(float('NaN'))
                c.append(float('NaN'))
                er_c.append(float('NaN'))
                self.sigma_phi_linear.append(float('NaN'))
                self.error_sigma_phi_linear.append(float('NaN'))
                self.sigma_phi_elliptic.append(float('NaN'))
                shear_phi_elliptic.append(float('NaN'))
                self.shear_phi_elliptic.append(float('NaN'))
                self.error_sigma_phi_elliptic.append(float('NaN'))
                self.error_shear_phi_elliptic.append(float('NaN'))
                self.strain_linear_fit.append([])
                self.strain_elliptical_fit.append([])
              
        self.sigma12_valid=False
        if self.stress_valid>=2:
            for i in range (len(self.liste_phi)):
                if np.isnan(self.sigma_phi_linear[i])==False:
                    if abs(np.sin(np.radians(2*self.liste_phi[i])))>=1e-15:
                        self.sigma12_valid=True
                        break

        co_s11=[];co_s12=[];co_s22=[];co_sph=[];co_sphi=[];co_er_sphi=[] #without shear
        for i in range(len(self.liste_phi)):
            if True not in (np.isnan((self.sigma_phi_linear[i],self.error_sigma_phi_linear[i],self.b[i],self.er_b[i]))):
                co_s11.append((np.cos(np.radians(self.liste_phi[i])))**2)
                co_s12.append(np.sin(np.radians(2*self.liste_phi[i])))
                co_s22.append((np.sin(np.radians(self.liste_phi[i])))**2)
                co_sph.append(0)
                co_sphi.append(self.sigma_phi_linear[i])
                co_er_sphi.append(self.error_sigma_phi_linear[i])
                
                co_s11.append(main_calcul.s1)
                co_s12.append(0)
                co_s22.append(main_calcul.s1)
                co_sph.append(1)
                co_sphi.append(self.b[i])
                co_er_sphi.append(self.er_b[i])
                
        co_s11_shear=[];co_s12_shear=[];co_s22_shear=[];co_s13_shear=[];co_s23_shear=[];co_s33_shear=[];co_sphi_shear=[];co_er_sphi_shear=[];co_sph_shear=[] #with shear
        for i in range (len(self.liste_phi)):
            if True not in (np.isnan((self.sigma_phi_elliptic[i],self.error_sigma_phi_elliptic[i],self.shear_phi_elliptic[i],self.error_shear_phi_elliptic[i],c[i],er_c[i]))) :
                co_s11_shear.append((np.cos(np.radians(self.liste_phi[i])))**2)
                co_s12_shear.append(np.sin(np.radians(2*self.liste_phi[i])))
                co_s22_shear.append((np.sin(np.radians(self.liste_phi[i])))**2)
                co_s13_shear.append(0)
                co_s23_shear.append(0)
                co_s33_shear.append(-1)
                co_sph_shear.append(0)
                co_sphi_shear.append(self.sigma_phi_elliptic[i])
                co_er_sphi_shear.append(self.error_sigma_phi_elliptic[i])
                
                co_s11_shear.append(main_calcul.s1)
                co_s12_shear.append(0)
                co_s22_shear.append(main_calcul.s1)
                co_s13_shear.append(0)
                co_s23_shear.append(0)
                co_s33_shear.append(main_calcul.s2_2+main_calcul.s1)
                co_sph_shear.append(main_calcul.s2_2+3*main_calcul.s1)
                co_sphi_shear.append(c[i])
                co_er_sphi_shear.append(er_c[i])
                
                co_s11_shear.append(0)
                co_s12_shear.append(0)
                co_s22_shear.append(0)
                co_s13_shear.append(np.cos(np.radians(self.liste_phi[i])))
                co_s23_shear.append(np.sin(np.radians(self.liste_phi[i])))
                co_s33_shear.append(0)
                co_sph_shear.append(0)
                co_sphi_shear.append(shear_phi_elliptic[i])
                co_er_sphi_shear.append(self.error_shear_phi_elliptic[i])
  
        if self.sigma12_valid==False and self.stress_valid>=2:
            co=[]
            co.append(co_s11)
            co.append(co_s22)
            co.append(co_sph)
            self.tensor_biaxial_1=curve_fit(tensor_biaxial_simple,co,co_sphi,sigma=co_er_sphi)

            self.all_sigma_phi_biaxial_1=[]
            for i in range(0,361,5):
                self.all_sigma_phi_biaxial_1.append(self.tensor_biaxial_1[0][0]*(np.cos(np.radians(i)))**2+
                                                           self.tensor_biaxial_1[0][1]*(np.sin(np.radians(i)))**2)

            co=[]
            co.append(co_s11_shear)
            co.append(co_s22_shear)
            co.append(co_s13_shear)
            co.append(co_s23_shear)
            co.append(co_sph_shear)
            self.tensor_biaxial_shear_1=curve_fit(tensor_biaxial_simple_shear,co,co_sphi_shear,sigma=co_er_sphi_shear)

            self.all_sigma_phi_biaxial_shear_1=[]
            for i in range(0,361,5):
                self.all_sigma_phi_biaxial_shear_1.append(self.tensor_biaxial_shear_1[0][0]*(np.cos(np.radians(i)))**2+
                                                                 self.tensor_biaxial_shear_1[0][1]*(np.sin(np.radians(i)))**2)
                
        if self.sigma12_valid==True: 
            co=[]
            co.append(co_s11)
            co.append(co_s12)
            co.append(co_s22)
            co.append(co_sph)
            self.tensor_biaxial_1=curve_fit(tensor_biaxial,co,co_sphi,sigma=co_er_sphi)

            self.all_sigma_phi_biaxial_1=[]
            for i in range(0,361,5):
                self.all_sigma_phi_biaxial_1.append(self.tensor_biaxial_1[0][0]*(np.cos(np.radians(i)))**2+
                                              self.tensor_biaxial_1[0][1]*np.sin(np.radians(2*i))+
                                              self.tensor_biaxial_1[0][2]*(np.sin(np.radians(i)))**2)

            co=[]
            co.append(co_s11_shear)
            co.append(co_s12_shear)
            co.append(co_s22_shear)
            co.append(co_s13_shear)
            co.append(co_s23_shear)
            co.append(co_sph_shear)
            self.tensor_biaxial_shear_1=curve_fit(tensor_biaxial_shear,co,co_sphi_shear,sigma=co_er_sphi_shear)

            self.all_sigma_phi_biaxial_shear_1=[]
            for i in range(0,361,5):
                self.all_sigma_phi_biaxial_shear_1.append(self.tensor_biaxial_shear_1[0][0]*(np.cos(np.radians(i)))**2+
                                              self.tensor_biaxial_shear_1[0][1]*np.sin(np.radians(2*i))+
                                              self.tensor_biaxial_shear_1[0][2]*(np.sin(np.radians(i)))**2)

        if self.sigma12_valid==True and self.stress_valid>=3:
            co=[]
            co.append(co_s11_shear)
            co.append(co_s12_shear)
            co.append(co_s22_shear)
            co.append(co_s13_shear)
            co.append(co_s23_shear)
            co.append(co_s33_shear)
            self.tensor_triaxial_1=curve_fit(tensor_triaxial,co,co_sphi_shear,sigma=co_er_sphi_shear)

            self.all_sigma_phi_triaxial_1=[]
            for i in range(0,361,5):
                self.all_sigma_phi_triaxial_1.append(self.tensor_triaxial_1[0][0]*(np.cos(np.radians(i)))**2+
                                               self.tensor_triaxial_1[0][1]*np.sin(np.radians(2*i))+
                                               self.tensor_triaxial_1[0][2]*(np.sin(np.radians(i)))**2-
                                               self.tensor_triaxial_1[0][5])
            self.peak_true_1=2*np.degrees(np.arcsin(np.sin(np.radians(main_calcul.twotheta0/2))/
                                                  np.exp((main_calcul.s2_2+3*main_calcul.s1)*self.tensor_biaxial_shear_1[0][5])))
    #-----------------------------------------
    def method_fundamental(self,main_calcul):
        p11=[];p12=[];p22=[];p13=[];p23=[];p33=[];p_ph=[]
        for i in range(len(main_calcul.phi)):
            if str(i+1) in self.list_graph_error:
                continue
            cos_theta=np.cos(np.radians(self.peaks_position[i]/2))                  
            sin_theta=np.sin(np.radians(self.peaks_position[i]/2))
            cos_omega=np.cos(np.radians(main_calcul.omega[i]+(self.peaks_position[i]-main_calcul.twotheta[i])/2))
            sin_omega=np.sin(np.radians(main_calcul.omega[i]+(self.peaks_position[i]-main_calcul.twotheta[i])/2))
            cos_gamma=np.cos(np.radians(-90))
            sin_gamma=np.sin(np.radians(-90))
            cos_phi=np.cos(np.radians(main_calcul.phi[i]))
            sin_phi=np.sin(np.radians(main_calcul.phi[i]))
            cos_chi=np.cos(np.radians(main_calcul.chi[i]))
            sin_chi=np.sin(np.radians(main_calcul.chi[i]))
                
            a=sin_theta*cos_omega+sin_gamma*cos_theta*sin_omega
            b=-cos_gamma*cos_theta
            c=sin_theta*sin_omega-sin_gamma*cos_theta*cos_omega

            h2=-a*cos_phi-b*cos_chi*sin_phi+c*sin_chi*sin_phi
            h1=a*sin_phi-b*cos_chi*cos_phi+c*sin_chi*cos_phi
            h3=b*sin_chi+c*cos_chi
            
            f11=h1**2
            f22=h2**2
            f33=h3**2
            f12=2*h1*h2
            f13=2*h1*h3
            f23=2*h2*h3
                
            p11.append(main_calcul.s2_2*f11+main_calcul.s1)
            p22.append(main_calcul.s2_2*f22+main_calcul.s1)
            p33.append(main_calcul.s2_2*f33+main_calcul.s1)
            p12.append(main_calcul.s2_2*f12)
            p13.append(main_calcul.s2_2*f13)
            p23.append(main_calcul.s2_2*f23)
            p_ph.append(main_calcul.s2_2+3*main_calcul.s1)
    #----------------------------------------
        strain=[]
        error_strain=[]
        for i in range(len(main_calcul.phi)):
            if str(i+1) in self.list_graph_error:
                continue
            strain.append(np.sin(np.radians(main_calcul.twotheta0/2))/np.sin(np.radians(self.peaks_position[i]/2))-1)
            error_strain.append(abs(np.radians(self.error_peaks_position[i]/2)*
                                    np.cos(np.radians(self.peaks_position[i]/2))*
                                    np.sin(np.radians(main_calcul.twotheta0/2))/
                                    np.sin(np.radians(self.peaks_position[i]/2))**2))
                                                
        self.length_strain=len(strain)

        #--------------------------------------------            
        if len(self.liste_phi)>=1:
            # Biaxial
            if self.length_strain>=3:
                pij=[] 
                pij.append(p11)
                pij.append(p22)
                pij.append(p_ph)

                self.tensor_biaxial=curve_fit(tensor_biaxial_simple,pij,strain,sigma=error_strain)

                self.sigma_phi_biaxial=[]
                self.error_sigma_phi_biaxial=[]
                for i in range(len(self.liste_phi)):
                    self.sigma_phi_biaxial.append(self.tensor_biaxial[0][0]*(np.cos(np.radians(self.liste_phi[i])))**2+
                                                  self.tensor_biaxial[0][1]*(np.sin(np.radians(self.liste_phi[i])))**2)
                    self.error_sigma_phi_biaxial.append(abs((self.tensor_biaxial[1][0,0]**0.5)*(np.cos(np.radians(self.liste_phi[i])))**2+
                                                        (self.tensor_biaxial[1][1,1]**0.5)*(np.sin(np.radians(self.liste_phi[i])))**2))

                self.strain_biaxial=[]
                for i in range(len(self.liste_phi)):
                    strain_biaxial_i=[]
                    for j in range(len(self.sinpsi_2_sorted[i])):
                        strain_biaxial_i.append(main_calcul.s2_2*self.sigma_phi_biaxial[i]*self.sinpsi_2_sorted[i][j]+
                                                main_calcul.s1*(self.tensor_biaxial[0][0]+self.tensor_biaxial[0][1])+
                                                (main_calcul.s2_2+3*main_calcul.s1)*self.tensor_biaxial[0][2])
                    self.strain_biaxial.append(strain_biaxial_i)

                self.all_sigma_phi_biaxial=[]
                for i in range(0,361,5):
                    self.all_sigma_phi_biaxial.append(self.tensor_biaxial[0][0]*(np.cos(np.radians(i)))**2+
                                                      self.tensor_biaxial[0][1]*(np.sin(np.radians(i)))**2)

            # Biaxial+shear
            if self.length_strain>=4:
                pij=[] 
                pij.append(p11)
                pij.append(p12)
                pij.append(p22)
                pij.append(p_ph)            
               
                self.tensor_biaxial=Curve_Fit(tensor_biaxial,pij,strain,error_strain)

                self.sigma_phi_biaxial=[]
                self.error_sigma_phi_biaxial=[]
                for i in range(len(self.liste_phi)):
                    self.sigma_phi_biaxial.append(self.tensor_biaxial[0][0]*(np.cos(np.radians(self.liste_phi[i])))**2+
                                                  self.tensor_biaxial[0][1]*np.sin(np.radians(2*self.liste_phi[i]))+
                                                  self.tensor_biaxial[0][2]*(np.sin(np.radians(self.liste_phi[i])))**2)
                    self.error_sigma_phi_biaxial.append(abs((self.tensor_biaxial[1][0,0]**0.5)*(np.cos(np.radians(self.liste_phi[i])))**2+
                                                        (self.tensor_biaxial[1][1,1]**0.5)*(np.sin(2*np.radians(self.liste_phi[i])))+
                                                        (self.tensor_biaxial[1][2,2]**0.5)*(np.sin(np.radians(self.liste_phi[i])))**2))

                self.strain_biaxial=[]
                for i in range(len(self.liste_phi)):
                    strain_biaxial_i=[]
                    for j in range(len(self.sinpsi_2_sorted[i])):
                        strain_biaxial_i.append(main_calcul.s2_2*self.sigma_phi_biaxial[i]*(np.sin(np.radians(self.psi_sorted[i][j])))**2+
                                                main_calcul.s1*(self.tensor_biaxial[0][0]+self.tensor_biaxial[0][2])+
                                                (main_calcul.s2_2+3*main_calcul.s1)*self.tensor_biaxial[0][3])
                    self.strain_biaxial.append(strain_biaxial_i)

                self.all_sigma_phi_biaxial=[]
                for i in range(0,361,5):
                    self.all_sigma_phi_biaxial.append(self.tensor_biaxial[0][0]*(np.cos(np.radians(i)))**2+
                                                      self.tensor_biaxial[0][1]*np.sin(np.radians(2*i))+
                                                      self.tensor_biaxial[0][2]*(np.sin(np.radians(i)))**2)
                    
            if self.length_strain>=5:
                pij=[] 
                pij.append(p11)
                pij.append(p22)
                pij.append(p13)
                pij.append(p23)
                pij.append(p_ph)

                self.tensor_biaxial_shear=curve_fit(tensor_biaxial_simple_shear,pij,strain,sigma=error_strain)

                self.sigma_phi_biaxial_shear=[]
                self.error_sigma_phi_biaxial_shear=[]
                self.shear_phi_biaxial_shear=[]
                self.error_shear_phi_biaxial_shear=[]
                for i in range(len(self.liste_phi)):
                    self.sigma_phi_biaxial_shear.append(self.tensor_biaxial_shear[0][0]*(np.cos(np.radians(self.liste_phi[i])))**2+
                                                        self.tensor_biaxial_shear[0][1]*(np.sin(np.radians(self.liste_phi[i])))**2)
                    self.error_sigma_phi_biaxial_shear.append((self.tensor_biaxial_shear[1][0,0]**0.5)*(np.cos(np.radians(self.liste_phi[i])))**2+
                                                              (self.tensor_biaxial_shear[1][1,1]**0.5)*(np.sin(np.radians(self.liste_phi[i])))**2)
                    self.shear_phi_biaxial_shear.append(abs(self.tensor_biaxial_shear[0][2]*np.cos(np.radians(self.liste_phi[i]))+
                                                        self.tensor_biaxial_shear[0][3]*np.sin(np.radians(self.liste_phi[i]))))
                    self.error_shear_phi_biaxial_shear.append(abs((self.tensor_biaxial_shear[1][2,2]**0.5)*np.cos(np.radians(self.liste_phi[i]))+
                                                              (self.tensor_biaxial_shear[1][3,3]**0.5)*np.sin(np.radians(self.liste_phi[i]))))

                
                self.strain_biaxial_shear=[]
                for i in range(len(self.liste_phi)):
                    strain_biaxial_shear_i=[]
                    for j in range(len(self.sinpsi_2_sorted[i])):
                        strain_biaxial_shear_i.append(main_calcul.s2_2*self.sigma_phi_biaxial_shear[i]*self.sinpsi_2_sorted[i][j]+
                                                      main_calcul.s2_2*(self.tensor_biaxial_shear[0][2]*np.cos(np.radians(self.liste_phi[i]))+
                                                                        self.tensor_biaxial_shear[0][3]*np.sin(np.radians(self.liste_phi[i])))*np.sin(np.radians(2*self.psi_sorted[i][j]))+
                                                      main_calcul.s1*(self.tensor_biaxial_shear[0][0]+self.tensor_biaxial_shear[0][1])+
                                                      (main_calcul.s2_2+3*main_calcul.s1)*self.tensor_biaxial_shear[0][4])
                    self.strain_biaxial_shear.append(strain_biaxial_shear_i)

                self.all_sigma_phi_biaxial_shear=[]
                for i in range(0,361,5):
                    self.all_sigma_phi_biaxial_shear.append(self.tensor_biaxial_shear[0][0]*(np.cos(np.radians(i)))**2+
                                                            self.tensor_biaxial_shear[0][1]*(np.sin(np.radians(i)))**2)

            #Biaxial+shear:
            if self.length_strain>=6:
                pij=[] 
                pij.append(p11)
                pij.append(p12)
                pij.append(p22)
                pij.append(p13)
                pij.append(p23)
                pij.append(p_ph)
                
                self.tensor_biaxial_shear=curve_fit(tensor_biaxial_shear,pij,strain,sigma=error_strain)

                self.sigma_phi_biaxial_shear=[]
                self.error_sigma_phi_biaxial_shear=[]
                self.shear_phi_biaxial_shear=[]
                self.error_shear_phi_biaxial_shear=[]
                for i in range(len(self.liste_phi)):
                    self.sigma_phi_biaxial_shear.append(self.tensor_biaxial_shear[0][0]*(np.cos(np.radians(self.liste_phi[i])))**2+
                                                        self.tensor_biaxial_shear[0][1]*np.sin(np.radians(2*self.liste_phi[i]))+
                                                        self.tensor_biaxial_shear[0][2]*(np.sin(np.radians(self.liste_phi[i])))**2)
                    self.error_sigma_phi_biaxial_shear.append((np.sqrt(self.tensor_biaxial_shear[1][0,0]))*(np.cos(np.radians(self.liste_phi[i])))**2+
                                                              (np.sqrt(self.tensor_biaxial_shear[1][1,1]))*abs(np.sin(2*np.radians(self.liste_phi[i])))+
                                                              (np.sqrt(self.tensor_biaxial_shear[1][2,2]))*(np.sin(np.radians(self.liste_phi[i])))**2)
                    self.shear_phi_biaxial_shear.append(abs(self.tensor_biaxial_shear[0][3]*np.cos(np.radians(self.liste_phi[i]))+
                                                        self.tensor_biaxial_shear[0][4]*np.sin(np.radians(self.liste_phi[i]))))
                    self.error_shear_phi_biaxial_shear.append(abs((np.sqrt(self.tensor_biaxial_shear[1][3,3]))*np.cos(np.radians(self.liste_phi[i]))+
                                                              (np.sqrt(self.tensor_biaxial_shear[1][4,4]))*np.sin(np.radians(self.liste_phi[i]))))

                self.strain_biaxial_shear=[]
                for i in range(len(self.liste_phi)):
                    strain_biaxial_shear_i=[]
                    for j in range(len(self.sinpsi_2_sorted[i])):
                        strain_biaxial_shear_i.append(main_calcul.s2_2*self.sigma_phi_biaxial_shear[i]*self.sinpsi_2_sorted[i][j]+
                                                      main_calcul.s2_2*(self.tensor_biaxial_shear[0][3]*np.cos(np.radians(self.liste_phi[i]))+
                                                                        self.tensor_biaxial_shear[0][4]*np.sin(np.radians(self.liste_phi[i])))*np.sin(np.radians(2*self.psi_sorted[i][j]))+
                                                      main_calcul.s1*(self.tensor_biaxial_shear[0][0]+self.tensor_biaxial_shear[0][2])+
                                                      (main_calcul.s2_2+3*main_calcul.s1)*self.tensor_biaxial_shear[0][5])
                    self.strain_biaxial_shear.append(strain_biaxial_shear_i)

                self.all_sigma_phi_biaxial_shear=[]
                for i in range(0,361,5):
                    self.all_sigma_phi_biaxial_shear.append(self.tensor_biaxial_shear[0][0]*(np.cos(np.radians(i)))**2+
                                                            self.tensor_biaxial_shear[0][1]*np.sin(np.radians(2*i))+
                                                            self.tensor_biaxial_shear[0][2]*(np.sin(np.radians(i)))**2)

    #Triaial--------------------------------------------------------------------------------
            if self.length_strain>=6:
                pij=[] 
                pij.append(p11)
                pij.append(p12)
                pij.append(p22)
                pij.append(p13)
                pij.append(p23)
                pij.append(p33)
                
                self.tensor_triaxial=curve_fit(tensor_triaxial,pij,strain,sigma=error_strain,absolute_sigma=True)

                self.sigma_phi_triaxial=[]
                self.error_sigma_phi_triaxial=[]
                self.shear_phi_triaxial=[]
                self.error_shear_phi_triaxial=[]
                for i in range(len(self.liste_phi)):
                    self.sigma_phi_triaxial.append(self.tensor_triaxial[0][0]*(np.cos(np.radians(self.liste_phi[i])))**2+
                                                   self.tensor_triaxial[0][1]*np.sin(2*np.radians(self.liste_phi[i]))+
                                                   self.tensor_triaxial[0][2]*(np.sin(np.radians(self.liste_phi[i])))**2-
                                                   self.tensor_triaxial[0][5])
                    self.error_sigma_phi_triaxial.append(abs((self.tensor_triaxial[1][0,0]**0.5)*(np.cos(np.radians(self.liste_phi[i]))**2)+
                                                         (self.tensor_triaxial[1][1,1]**0.5)*np.sin(np.radians(2*self.liste_phi[i]))+
                                                         (self.tensor_triaxial[1][2,2]**0.5)*(np.sin(np.radians(self.liste_phi[i]))**2)-
                                                         self.tensor_triaxial[1][5,5]**0.5))
                    self.shear_phi_triaxial.append(abs(self.tensor_triaxial[0][3]*np.cos(np.radians(self.liste_phi[i]))+
                                                   self.tensor_triaxial[0][4]*np.sin(np.radians(self.liste_phi[i]))))
                    self.error_shear_phi_triaxial.append(abs(self.tensor_triaxial[1][3,3]**0.5*np.cos(np.radians(self.liste_phi[i]))+
                                                             self.tensor_triaxial[1][4,4]**0.5*np.sin(np.radians(self.liste_phi[i]))))

                self.strain_triaxial=[]
                for i in range(len(self.liste_phi)):
                    strain_triaxial_i=[]
                    for j in range(len(self.sinpsi_2_sorted[i])):
                        strain_triaxial_i.append(main_calcul.s2_2*self.sigma_phi_triaxial[i]*self.sinpsi_2_sorted[i][j]+
                                                 main_calcul.s2_2*(self.tensor_triaxial[0][3]*np.cos(np.radians(self.liste_phi[i]))+
                                                                   self.tensor_triaxial[0][4]*np.sin(np.radians(self.liste_phi[i])))*np.sin(np.radians(2*self.psi_sorted[i][j]))+
                                                 main_calcul.s1*(self.tensor_triaxial[0][0]+self.tensor_triaxial[0][2])+
                                                (main_calcul.s1+ main_calcul.s2_2)*self.tensor_triaxial[0][5])
                    self.strain_triaxial.append(strain_triaxial_i)

                self.all_sigma_phi_triaxial=[]
                for i in range(0,361,5):
                    self.all_sigma_phi_triaxial.append(self.tensor_triaxial[0][0]*(np.cos(np.radians(i)))**2+
                                                       self.tensor_triaxial[0][1]*np.sin(np.radians(2*i))+
                                                       self.tensor_triaxial[0][2]*(np.sin(np.radians(i)))**2-
                                                       self.tensor_triaxial[0][5])

            self.peak_true=2*np.degrees(np.arcsin(np.sin(np.radians(main_calcul.twotheta0/2))/
                                                np.exp((main_calcul.s2_2+3*main_calcul.s1)*self.tensor_biaxial_shear[0][5])))
