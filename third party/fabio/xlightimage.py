# coding: utf-8
#
#    Project: X-ray image reader
#             https://github.com/silx-kit/fabio
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#  Permission is hereby granted, free of charge, to any person
#  obtaining a copy of this software and associated documentation files
#  (the "Software"), to deal in the Software without restriction,
#  including without limitation the rights to use, copy, modify, merge,
#  publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so,
#  subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be
#  included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.


"""X-Light sofware output image

"""
# Get ready for python3:
from __future__ import with_statement, print_function, division

__authors__ = ["PHAM Tu Quoc Sang"]
__contact__ = "sang.phamtuquoc@gmail.com"
__license__ = "MIT"
__copyright__ = "Institut Jean Lamour"
__date__ = "25/01/2019"

import logging
logger = logging.getLogger(__name__)
import numpy
from .fabioimage import FabioImage, OrderedDict
import numpy


class XlightImage(FabioImage):
    """FabIO image class for Images for XXX detector

    Put some documentation here
    """

    DESCRIPTION = "Name of the file format"

    DEFAULT_EXTENSIONS = []

    HEADERS_KEYS = ["Phi",
                    "Chi",
                    "Omega",
                    "2theta",
                    "Wavelength",
                    "Distance",
                    "NRow",
                    "NCol",
                    "Center Row",
                    "Center Col"]

    def __init__(self, *arg, **kwargs):
        """
        Generic constructor
        """
        FabioImage.__init__(self, *arg, **kwargs)

    def _readheader(self, infile):
        """
        Read and decode the header of an image:

        :param infile: Opened python file (can be stringIO or bipped file)
        """
        # list of header key to keep the order (when writing)
        f_open = open(infile, "r") 
        for i in range(15):
            f_info_line=f_open.readline()
            f_info=f_info_line.split("=")
            if "Phi" in f_info[0]:
                self.header["Phi"]=f_info[1]
            if "Chi" in f_info[0]:
                self.header["Chi"]=f_info[1]
            if "Omega" in f_info[0]:
                self.header["Omega"]=f_info[1]
            if "2theta" in f_info[0]:
                self.header["2theta"]=f_info[1]
            if "Wavelength" in f_info[0]:
                self.header["Wavelength"]=f_info[1]      
            if "Distance" in f_info[0]:
                self.header["Distance"]=f_info[1]  
            if "NRow" in f_info[0]:
                self.header["NRow"]=f_info[1]
                self.dim1=int(f_info[1])
            if "NCol" in f_info[0]:
                self.header["NCol"]=f_info[1]
                self.dim2=int(f_info[1])
            if "Center Row" in f_info[0]:
                self.header["Center Row"]=f_info[1]  
            if "Center Col" in f_info[0]:
                self.header["Center Col"]=f_info[1]  

    def read(self, fname, frame=None):
        """
        Try to read image

        :param fname: name of the file
        :param frame: number of the frame
        """
        f_open = open(fname, "r")  
        for i in range(15):
            f_info_line=f_open.readline()
            f_info=f_info_line.split("=")
            if "NRow" in f_info[0]:
                dim1=int(f_info[1])
            if "NCol" in f_info[0]:
                dim2=int(f_info[1])
        
        intensity_2D=[]
        for i in range(dim1):
            f_data=f_open.readline()
            intensity_2D.append(numpy.fromstring(f_data,dtype=float, sep=" "))

        self.data=numpy.array(intensity_2D)
        # Nota: dim1, dim2, bytecode and bpp are properties defined by the dataset
        return self


xlightimage = XlightImage
