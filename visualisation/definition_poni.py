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
from tkinter.messagebox import *
def definition_poni():
    mess=("- Pixel size 1: Deprecated. Pixel size of the fist dimension of the detector,  in meter.\n"+
          "- Pixel size 2: Deprecated. Pixel size of the second dimension of the detector,  in meter.\n"+
          "- Distance: sample - detector plan (orthogonal distance, not along the beam), in meter.\n"+
          "- Poni 1: coordinate of the point of normal incidence along the detector's first dimension, in meter\n"+
          "- Poni 2: coordinate of the point of normal incidence along the detector's second dimension, in meter\n"+
          "- Rotation 1: first rotation from sample ref to detector's ref, in radians\n"+
          "- Rotation 2: second rotation from sample ref to detector's ref, in radians\n"+
          "- Rotation 3: third rotation from sample ref to detector's ref, in radians\n"+
          "- Wavelength: Wave length used in meter")
    showinfo(title="Definition",message=mess)
    mainloop()
