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
from read_file.image_2D.image_correction_xpad_soleil import image_correction_xpad_soleil
#from read_file.image_2D.image_correction_new import image_correction_new

def image_correction(header,data):
    if "SOLEIL" in header[0] and "diffabs" in header[1]:
        data=image_correction_xpad_soleil(data)
    #elif "xxxx" in header[i] and "yyyy" in header[j]: #use header to identify your format
        #data=image_correction_new(data)

    return(data)
