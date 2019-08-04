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
from scipy.optimize import curve_fit
import numpy as np
import warnings
from scipy.optimize import OptimizeWarning

def Lorentzian_fit(intensity,two_theta,kalpha_1,kalpha_2,kalpha_ratio,p_0,peak_shape):
    if kalpha_2==0:
        kalpha_ratio=0

    if peak_shape==1:
        p0_guess=[]
        bound_inf=[]
        bound_sup=[]
        for i in range(len(p_0)):
            p0_guess.append(p_0[i][0]) #I0
            p0_guess.append(p_0[i][1]) #2theta1
            p0_guess.append(p_0[i][2]) #w

            bound_inf.append(0)
            bound_inf.append(min(two_theta))
            bound_inf.append(0)
            
            bound_sup.append(max(intensity)*2)
            bound_sup.append(max(two_theta))
            bound_sup.append(max(two_theta)-min(two_theta))
                
        def F_lorentzian(x,*p):
            I=0
            for i in range(len(p_0)):
                w=p[i*3+2]
                I1=p[i*3]*w**2/(4*(x-p[i*3+1])**2+w**2)
                if (np.any(I1<0)==True) or (True in np.isnan(I1)) or (True in np.isinf(I1)):
                    I1=float('inf')
                theta_2=2*np.degrees(np.arcsin((kalpha_2/kalpha_1)*np.sin(np.radians(p[i*3+1]/2))))            
                I2=p[i*3]*kalpha_ratio*w**2/(4*(x-theta_2)**2+w**2)
                if (np.any(I2<0)==True) or (True in np.isnan(I2)) or (True in np.isinf(I2)):
                    I2=float('inf')
                I=I+I1+I2            
            return I
            
    else:
        p0_guess=[]
        bound_inf=[]
        bound_sup=[]
        for i in range(len(p_0)):
            p0_guess.append(p_0[i][0]) #I0
            p0_guess.append(p_0[i][1]) #2theta1
            p0_guess.append(p_0[i][2]) #w
            p0_guess.append(0)          #a

            bound_inf.append(0)
            bound_inf.append(min(two_theta))
            bound_inf.append(0)
            bound_inf.append(-float('inf'))
            
            bound_sup.append(max(intensity)*2)
            bound_sup.append(max(two_theta))
            bound_sup.append(max(two_theta)-min(two_theta))
            bound_sup.append(float('inf'))
                
        def F_lorentzian(x,*p):
            I=0
            for i in range(len(p_0)):
                w=2*p[i*4+2]/(1+np.exp(p[i*4+3]*(x-p[i*4+1])))
                I1=p[i*4]*w**2/(4*(x-p[i*4+1])**2+w**2)
                if (np.any(I1<0)==True) or (True in np.isnan(I1)) or (True in np.isinf(I1)):
                    I1=float('inf')
                theta_2=2*np.degrees(np.arcsin((kalpha_2/kalpha_1)*np.sin(np.radians(p[i*4+1]/2))))            
                I2=p[i*4]*kalpha_ratio*w**2/(4*(x-theta_2)**2+w**2)
                if (np.any(I2<0)==True) or (True in np.isnan(I2)) or (True in np.isinf(I2)):
                    I2=float('inf')
                I=I+I1+I2            
            return I
            
    for Method in ('lm','trf','dogbox'):
        try:
            if Method=='lm':
                popt,pcov= curve_fit(F_lorentzian, two_theta, intensity, p0=p0_guess,method=Method)
            else:
                popt,pcov= curve_fit(F_lorentzian, two_theta, intensity, p0=p0_guess,method=Method,bounds=(bound_inf,bound_sup))
        except Exception:
            pass
        else:
            if True not in np.isinf(np.diag(pcov)):
                break
    
    for i in range(len(popt)):
        if np.isnan(popt[i])==True or np.isinf(popt[i])==True:
            popt[i]=0
        if np.isnan(pcov[i,i])==True or np.isinf(pcov[i,i])==True:
            pcov[i,i]=0
            
    peak_intensity=[];    error_peak_intensity=[]
    peak_position=[];    error_peak_position=[]
    FWHM=[];    error_FWHM=[]
    a=[]
    
    for i in range(len(p_0)):
        if peak_shape==1:
            peak_intensity.append(popt[i*3])
            peak_position.append(popt[i*3+1])
            FWHM.append(popt[i*3+2])
            a.append(0)
        
            if pcov[i*3,i*3]==0:
                error_peak_intensity.append(peak_intensity[i]*0.001)
            else:
                error_peak_intensity.append(np.sqrt(pcov[i*3,i*3]))

            if pcov[i*3+1,i*3+1]==0:
                error_peak_position.append(peak_position[i]*0.001)
            else:
                error_peak_position.append(np.sqrt(pcov[i*3+1,i*3+1]))

            if pcov[i*3+2,i*3+2]==0:
                error_FWHM.append(FWHM[i]*0.001)
            else:
                error_FWHM.append(np.sqrt(pcov[i*3+2,i*3+2]))

        else:
            peak_intensity.append(popt[i*4])
            peak_position.append(popt[i*4+1])
            FWHM.append(popt[i*4+2])
            a.append(popt[i*4+3])

            if pcov[i*4,i*4]==0:
                error_peak_intensity.append(peak_intensity[i]*0.001)
            else:
                error_peak_intensity.append(np.sqrt(pcov[i*4,i*4]))

            if pcov[i*4+1,i*4+1]==0:
                error_peak_position.append(peak_position[i]*0.001)
            else:
                error_peak_position.append(np.sqrt(pcov[i*4+1,i*4+1]))

            if pcov[i*4+2,i*4+2]==0:
                error_FWHM.append(FWHM[i]*0.001)
            else:
                error_FWHM.append(np.sqrt(pcov[i*4+2,i*4+2]))
                
    FF=[] #[['peak 1' F kalpha1,F kalpha2],['peak 2' F kalpha1,F kalpha2],...]
    for j in range(len(p_0)):
        Fi=[]
        try:
            w=2*FWHM[j]/(1+np.exp(a[j]*(np.array(two_theta)-peak_position[j])))
            F1_i=peak_intensity[j]*w**2/(4*(np.array(two_theta)-peak_position[j])**2+w**2)
            theta_2=2*np.degrees(np.arcsin((kalpha_2/kalpha_1)*np.sin(np.radians(peak_position[j]/2))))            
            F2_i=peak_intensity[j]*kalpha_ratio*w**2/(4*(np.array(two_theta)-theta_2)**2+w**2)    
        except Exception:
            F1_i=[0]*len(two_theta)
            F2_i=[0]*len(two_theta)
            pass
        Fi.append(F1_i)
        Fi.append(F2_i)

        FF.append(Fi)

    F=[] 
    F1=np.array([0]*len(two_theta))
    F2=np.array([0]*len(two_theta))
    for j in range(len(p_0)):
        F.append(np.array(FF[j][0])+np.array(FF[j][1]))
        F1=F1+np.array(FF[j][0])
        F2=F2+np.array(FF[j][1])
    Ft=F1+F2
    
    #correlation coefficient        
    mean_Ft=sum(Ft)/len(Ft)
    mean_I=sum(intensity)/len(intensity)
    sum1=sum(list((np.array(Ft)-mean_Ft)*(np.array(intensity)-mean_I)))
    sum2=sum(list((np.array(Ft)-mean_Ft)**2))
    sum3=sum(list((np.array(intensity)-mean_I)**2))
    r=sum1/np.sqrt(sum2*sum3)
    if np.isnan(r)==True:
        r=0
        
    return(peak_position,error_peak_position,peak_intensity,error_peak_intensity,FWHM,error_FWHM,Ft,F1,F2,r,a,F)
