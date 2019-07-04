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

    
    f=open(r'file.h5',"wb") #открываем файл для записи, в режиме wb
    ufr = requests.get("https://cloud.iszf.irk.ru/index.php/s/odHPMppnvbgUHFW/download?path=%2F&files=sunspot1300_crop.h5") #делаем запрос
    f.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
    f.close()
#
    wfs = WFSData('file.h5')
    p = wfs.geometry.options
    wfs.geometry.set_options( shift = (-1,2))
    wfs.reference = 169
    
    wfs.show_geometry()
    
    plt.imshow(wfs[0][172])    
    print(wfs[0].get_offset(167))
    
#    wfs.save('geometred_file.h5')
#    wfs_saved = WFSData('geometred_file.h5')
#    
#    wfs_saved.show_geometry()


    