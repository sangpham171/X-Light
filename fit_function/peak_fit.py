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
from fit_function.Pearson_vii_fit import Pearson_vii_fit
from fit_function.Pseudo_Voigt_fit import Pseudo_Voigt_fit
from fit_function.Voigt_fit import Voigt_fit
from fit_function.Gaussian_fit import Gaussian_fit
from fit_function.Lorentzian_fit import Lorentzian_fit
import traceback
from tkinter.messagebox import *

def peak_fit(data_y_net,data_x_limit,kalpha_1,kalpha_2,kalpha_ratio,p0_guess,peak_shape,function_fit):
    try:
        if float(function_fit)==1:
            peak_fit_result=Pearson_vii_fit(data_y_net,data_x_limit,kalpha_1,kalpha_2,kalpha_ratio,p0_guess,peak_shape)
        if float(function_fit)==2:
            peak_fit_result=Pseudo_Voigt_fit(data_y_net,data_x_limit,kalpha_1,kalpha_2,kalpha_ratio,p0_guess,peak_shape)
        if float(function_fit)==3:
            peak_fit_result=Voigt_fit(data_y_net,data_x_limit,kalpha_1,kalpha_2,kalpha_ratio,p0_guess,peak_shape)
        if float(function_fit)==4:
            peak_fit_result=Gaussian_fit(data_y_net,data_x_limit,kalpha_1,kalpha_2,kalpha_ratio,p0_guess,peak_shape)
        if float(function_fit)==5:
            peak_fit_result=Lorentzian_fit(data_y_net,data_x_limit,kalpha_1,kalpha_2,kalpha_ratio,p0_guess,peak_shape)
    except Exception as e:
        showinfo(title="Warning",message=str(e)+"\n"+"\n"+str(traceback.format_exc()))
        return()
    return(peak_fit_result)
             
