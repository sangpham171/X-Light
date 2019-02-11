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

def image_correction_xpad_soleil(data):
    shape=data.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(6):
                col_correct=80*(k+1)
                moyen=(data[i][j][col_correct+1]+data[i][j][col_correct-2])/2
                data[i][j][col_correct]=moyen
                data[i][j][col_correct-1]=moyen

    for i in range(shape[0]):
        for j in range(shape[2]):
            moyen=(data[i][118][j]+data[i][121][j])/2
            data[i][119][j]=moyen
            data[i][120][j]=moyen

    for i in range(shape[0]):
        moyen_1=(data[i][94][284]+data[i][97][287])/2
        moyen_2=(data[i][124][269]+data[i][127][272])/2
        for j in range(2):
            for k in range(2):      
                data[i][95+j][285+k]=moyen_1
                data[i][125+j][270+k]=moyen_2

    for i in range(shape[0]):
        for j in range(120):
            data[i][j][48]=(data[i][j][47]+data[i][j][49])/2
            data[i][239-j][511]=(data[i][239-j][510]+data[i][239-j][512])/2
            data[i][239-j][528]=(data[i][239-j][527]+data[i][239-j][529])/2
                
    return(data)
