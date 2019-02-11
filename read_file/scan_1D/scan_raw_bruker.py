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
from os import SEEK_SET
import struct

def clean_str_1(val):
    val=val.replace("b'","")
    i=0
    while i<len(val):
        try:
            if val[i]=="\\" and val[i+1]=="x":
                val=val.replace(str(val[i:i+4]),"")
            else:
                i=i+1
        except IndexError:
            pass
    val=val.replace("'","")
    val=val.replace("@","")
    val=val.replace("$","")
    val=val.replace("?","")
    val=val.replace("<","")
    val=val.split("\\n")
    val=val[0]
    return(val)

def clean_str_2(val):
    val=val.replace("(","")
    val=val.replace(")","")
    val=val.replace(",","")
    return(val)

def read_raw_bruker(f,self):
    f_open = open(f, "rb")

    f_open.seek(0, SEEK_SET)
    version = clean_str_1(str(f_open.read(8)))
    if version == "RAW1.01":
        read_raw_101(f_open,self)

    if version == "RAW4.00":
        read_raw_400(f_open,self)


def read_raw_101(f,self):
    kalpha1=float('NaN')
    kalpha2=float('NaN')
    kalpha_ratio=0
    
    file_info=[]

    f.seek(0, SEEK_SET)
    file_info.append("_VERSION = "+clean_str_1(str(f.read(8))))
    
    f.seek(12, SEEK_SET)
    scan_count=float(clean_str_2(str(struct.unpack("I", f.read(4)))))
    file_info.append("_NUMBER_OF_SCANS = "+str(scan_count))

    f.seek(16, SEEK_SET)
    file_info.append("_DATEMEASURED = "+clean_str_1(str(f.read(20))))

    f.seek(36, SEEK_SET)
    file_info.append("_USER = "+clean_str_1(str(f.read(20))))

    f.seek(108, SEEK_SET)
    file_info.append("_SITE = "+clean_str_1(str(f.read(20))))

    f.seek(326, SEEK_SET)
    file_info.append("_SAMPLE = "+clean_str_1(str((f.read(20)))))

    f.seek(606, SEEK_SET)
    file_info.append("_ANODE= "+clean_str_1(str(f.read(4))))

    f.seek(616, SEEK_SET)
    file_info.append("_WL = "+clean_str_2(str(struct.unpack("d", f.read(8)))))

    f.seek(624, SEEK_SET)
    kalpha1=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
    file_info.append("_WL1 = "+str(kalpha1))

    f.seek(632, SEEK_SET)
    kalpha2=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
    file_info.append("_WL2 = "+str(kalpha2))

    f.seek(640, SEEK_SET)
    file_info.append("_WL3 = "+clean_str_2(str(struct.unpack("d", f.read(8)))))

    f.seek(648, SEEK_SET)
    kalpha_ratio=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
    file_info.append("_WLRATIO = "+str(kalpha_ratio))

    self.file_info.append(file_info)

    self.k_alpha.append(kalpha1)
    self.k_alpha.append(kalpha2)
    self.k_alpha.append(kalpha_ratio)
    
    scan_start=712
    for i in range(int(scan_count)):
        range_info=[]
        chi=float('NaN')
        phi=float('NaN')
        omega=float('NaN')
        twotheta=float('NaN')

        f.seek(scan_start+4, SEEK_SET)
        step_count=int(clean_str_2(str(struct.unpack("I", f.read(4)))))
        range_info.append("_STEPCOUNT = "+ str(step_count))
        
        f.seek(scan_start + 8, SEEK_SET)
        omega=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
        range_info.append("_OMEGA = "+ str(omega))

        f.seek(scan_start + 16, SEEK_SET)
        twotheta=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
        range_info.append("_2THETA = "+str(twotheta))

        f.seek(scan_start + 24, SEEK_SET)
        chi=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
        range_info.append("_CHI= " +str(chi))

        f.seek(scan_start + 32, SEEK_SET)
        phi=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
        range_info.append("_PHI = " +str(phi))

        f.seek(scan_start + 40, SEEK_SET)
        range_info.append("_X = "+ clean_str_2(str(struct.unpack("d", f.read(8)))))

        f.seek(scan_start + 48, SEEK_SET)
        range_info.append("_Y = "+ clean_str_2(str(struct.unpack("d", f.read(8)))))

        f.seek(scan_start + 56, SEEK_SET)
        range_info.append("_Z = "+ clean_str_2(str(struct.unpack("d", f.read(8)))))

        f.seek(scan_start + 176, SEEK_SET)
        step_size=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
        range_info.append("_STEPSIZE = "+str(step_size))

        self.range_info.append(range_info)

        self.chi.append(chi)
        self.phi.append(phi)
        self.omega.append(omega)
        self.twotheta.append(twotheta)
        
        step_start=scan_start+344

        data_x=[]
        data_y=[]
        for j in range(step_count):
            f.seek(step_start+j*4, SEEK_SET)
            data_x.append(twotheta+j*step_size)
            data_y.append(float(clean_str_2(str(struct.unpack("f", f.read(4))))))

        self.data_x.append(data_x)
        self.data_y.append(data_y)

        scan_start=step_start+step_count*4

def read_raw_400(f,self):
    kalpha1=float('NaN')
    kalpha2=float('NaN')
    kalpha_ratio=0
    
    file_info=[]

    f.seek(0, SEEK_SET)
    file_info.append("_VERSION = "+clean_str_1(str(f.read(8))))

    f.seek(12, SEEK_SET)
    file_info.append("_DATEMEASURED = "+clean_str_1(str(f.read(20))))
    
    f.seek(40, SEEK_SET)
    scan_count=float(clean_str_2(str(struct.unpack("I", f.read(4)))))
    file_info.append("_NUMBER_OF_SCANS = "+str(scan_count))

    i=40
    val=''
    while val!="USER":
        i=i+1
        f.seek(i, SEEK_SET)
        val=clean_str_1(str(f.read(4)))
    f.seek(i+24, SEEK_SET)
    file_info.append("_USER = "+clean_str_1(str(f.read(24))))

    while val!="SAMPLEID":
        i=i+1
        f.seek(i, SEEK_SET)
        val=clean_str_1(str(f.read(8)))
    f.seek(i+24, SEEK_SET)
    file_info.append("_SAMPLE = "+clean_str_1(str((f.read(24)))))

    while val!="UTF":
        i=i+1
        f.seek(i, SEEK_SET)
        val=clean_str_1(str(f.read(3)))
    f.seek(i+24, SEEK_SET)
    file_info.append("_UTF = "+clean_str_1(str((f.read(24)))))

    while val!="CREATOR":
        i=i+1
        f.seek(i, SEEK_SET)
        val=clean_str_1(str(f.read(7)))

    f.seek(i+24, SEEK_SET)
    file_info.append("_CREATOR= "+clean_str_1(str((f.read(24)))))

    while val!="CREATOR_VERSION":
        i=i+1
        f.seek(i, SEEK_SET)
        val=clean_str_1(str(f.read(15)))
    f.seek(i+24, SEEK_SET)
    file_info.append("_CREATOR_VERSION= "+clean_str_1(str((f.read(24)))))

    f.seek(i+104, SEEK_SET)
    file_info.append("_WL = "+clean_str_2(str(struct.unpack("d", f.read(8)))))

    f.seek(i+112, SEEK_SET)
    kalpha1=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
    file_info.append("_WL1 = "+str(kalpha1))

    f.seek(i+120, SEEK_SET)
    kalpha2=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
    file_info.append("_WL2 = "+str(kalpha2))

    f.seek(i+128, SEEK_SET)
    file_info.append("_WL3 = "+clean_str_2(str(struct.unpack("d", f.read(8)))))

    f.seek(i+136, SEEK_SET)
    kalpha_ratio=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
    file_info.append("_WLRATIO = "+str(kalpha_ratio))

    f.seek(i+148, SEEK_SET)
    file_info.append("_ANODE= "+clean_str_1(str(f.read(2))))

    f.seek(i+172, SEEK_SET)
    step_count=int(float(clean_str_2(str(struct.unpack("I", f.read(4))))))
    file_info.append("_STEPCOUNT = "+str(step_count))

    f.seek(i+240, SEEK_SET)
    file_info.append("_2THETA = "+str(clean_str_2(str(struct.unpack("d", f.read(8))))))

    f.seek(i+248, SEEK_SET)
    step_size=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
    file_info.append("_STEPSIZE = "+str(step_size))

    f.seek(i+263, SEEK_SET)
    file_info.append("_STEP_MODE = "+clean_str_1(str(f.read(1))))
    
    f.seek(i+268, SEEK_SET)
    file_info.append("_MV = "+clean_str_2(str(struct.unpack("f", f.read(4)))))

    f.seek(i+272, SEEK_SET)
    file_info.append("_MA = "+clean_str_2(str(struct.unpack("f", f.read(4)))))
    
    while val!="PSD_DISCRIM":
        i=i+1
        f.seek(i, SEEK_SET)
        val=clean_str_1(str(f.read(11)))

    f.seek(i+24, SEEK_SET)
    file_info.append("_PSD_DISCRIM = "+clean_str_1(str(f.read(24))))

    self.file_info.append(file_info)

    self.k_alpha.append(kalpha1)
    self.k_alpha.append(kalpha2)
    self.k_alpha.append(kalpha_ratio)

    j=700
    for i in range(int(scan_count)):
        range_info=[]
        chi=float('NaN')
        phi=float('NaN')
        omega=float('NaN')
        twotheta=float('NaN')

        while val!="2Theta":
            j=j+1
            f.seek(j, SEEK_SET)
            val=clean_str_1(str(f.read(6)))
        i_2theta=j
        f.seek(i_2theta+44, SEEK_SET)
        twotheta=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
        range_info.append("_2THETA = "+str(twotheta))

        j=j+5
        while val!="Theta":
            j=j+1
            f.seek(j, SEEK_SET)
            val=clean_str_1(str(f.read(5)))
        i_omega=j
        f.seek(i_omega+44, SEEK_SET)
        omega=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
        range_info.append("_OMEGA = "+ str(omega))

        while val!="Chi":
            j=j+1
            f.seek(j, SEEK_SET)
            val=clean_str_1(str(f.read(3)))
        i_chi=j
        f.seek(i_chi+44, SEEK_SET)
        chi=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
        range_info.append("_CHI= " +str(chi))

        while val!="Phi":
            j=j+1
            f.seek(j, SEEK_SET)
            val=clean_str_1(str(f.read(3)))
        i_phi=j
        f.seek(i_phi+44, SEEK_SET)
        phi=float(clean_str_2(str(struct.unpack("d", f.read(8)))))
        range_info.append("_PHI = " +str(phi))

        self.range_info.append(range_info)

        self.chi.append(chi)
        self.phi.append(phi)
        self.omega.append(omega)
        self.twotheta.append(twotheta)

        twotheta_start=i_phi+356

        data_x=[]
        data_y=[]
        for k in range(step_count):
            f.seek(twotheta_start+k*4, SEEK_SET)
            data_x.append(twotheta+k*step_size)
            data_y.append(float(clean_str_2(str(struct.unpack("f", f.read(4))))))

        self.data_x.append(data_x)
        self.data_y.append(data_y)

        j=twotheta_start+step_count*4
