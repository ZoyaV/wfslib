import pytest
import requests
import h5py
import matplotlib.pyplot as plt

import sys
sys.path.append('../wfslib')

from wfs import WFSData
from geometry import Geometry
import numpy as np

def test_wfsdata_cls():
    assert False


if __name__ == "__main__":
    
    #Скачиваем файл
    
#    arr = np.load("test_f_.npy")
#    g = Geometry(arr)
#    g.auto_make(diraction = 0)
#    #g.set_parametrs(border = 20)
#    g.show()
#    
#    print(g.parametrs)
    
    
#    f=open(r'file.h5',"wb") #открываем файл для записи, в режиме wb
#    ufr = requests.get("https://cloud.iszf.irk.ru/index.php/s/odHPMppnvbgUHFW/download?path=%2F&files=sunspot1300_crop.h5") #делаем запрос
#    f.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
#    f.close()
#
    wfs = WFSData('file.h5')
    p = wfs.geometry.options
    #start_point = p['start_point'][0] -1, p['start_point'][1]+2
    wfs.geometry.set_options( shift = (-1,2))
    wfs.reference = 169
    
    wfs.show_geometry()
    
    plt.imshow(wfs[0][172])    
    print(wfs[0].get_offset(167))
    
#    wfs.save('geometred_file.h5')
#    wfs_saved = WFSData('geometred_file.h5')
#    
#    wfs_saved.show_geometry()


    