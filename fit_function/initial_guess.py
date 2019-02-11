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

def initial_guess(intensity,two_theta,peaks_position,peaks_position_limit,peaks_width,init_guess):
    peaks_intensity_pre=[]
    peaks_position_pre=[]
    FWMH_pre=[]
    
    if init_guess==1:
        try:
            for i in range(len(peaks_position)):
                #peak index limit
                peak_index_left_limit=(np.abs(np.asarray(two_theta)-(peaks_position[i]-peaks_position_limit[i]))).argmin()
                peak_index_right_limit=(np.abs(np.asarray(two_theta)-(peaks_position[i]+peaks_position_limit[i]))).argmin()
                #peak max
                min_index_limit=min(peak_index_left_limit,peak_index_right_limit)
                max_index_limit=max(peak_index_left_limit,peak_index_right_limit)
                
                peak_max_index=min_index_limit+np.asarray(intensity[min_index_limit:max_index_limit]).argmax()
                intensity_max=intensity[peak_max_index]
                #list index >90% peak max
                peak_index_list=[]
                for j in range(min_index_limit,max_index_limit):
                    if intensity[j]>=intensity_max*0.9:
                        peak_index_list.append(j)
                #peak index preliminery
                peak_index_pre=int(sum(peak_index_list)/len(peak_index_list))
                #preak intensity and position preliminary
                peaks_position_pre.append(two_theta[peak_index_pre])
                peaks_intensity_pre.append(intensity[peak_index_pre])
                #FWHM preliminary
                MH=intensity_max/2
                MH_index_left=min_index_limit+(np.abs(np.asarray(intensity[min_index_limit:peak_index_pre+1])-MH)).argmin()
                MH_index_right=peak_index_pre-1+(np.abs(np.asarray(intensity[peak_index_pre-1:max_index_limit])-MH)).argmin()
                FWMH_pre.append(two_theta[MH_index_right]-two_theta[MH_index_left])
        except Exception:
            for i in range(len(peaks_position)):
                peak_index=(np.abs(np.asarray(two_theta)-peaks_position[i])).argmin()
                peaks_intensity_pre.append(intensity[peak_index])
                peaks_position_pre.append(peaks_position[i])
                FWMH_pre.append(peaks_width[i])
           
    else:
        for i in range(len(peaks_position)):
            peak_index=(np.abs(np.asarray(two_theta)-peaks_position[i])).argmin()
            peaks_intensity_pre.append(intensity[peak_index])
            peaks_position_pre.append(peaks_position[i])
            FWMH_pre.append(peaks_width[i])
            
    p0_guess=[]
    for i in range(len(peaks_position)):
        p0=[]
        p0.append(peaks_intensity_pre[i])
        p0.append(peaks_position_pre[i])
        p0.append(FWMH_pre[i])
        p0_guess.append(p0)
            
    return(p0_guess)
