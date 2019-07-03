import pytest
import requests
import h5py
import matplotlib.pyplot as plt

import sys
sys.path.append('../wfslib')

from wfs import WFSData
from geometry import Geometry

def test_wfsdata_cls():
    assert False


if __name__ == "__main__":
    
    #Скачиваем файл
    f=open(r'file4.h5',"wb") #открываем файл для записи, в режиме wb
    ufr = requests.get("https://cloud.iszf.irk.ru/index.php/s/odHPMppnvbgUHFW/download?path=%2F&files=sunspot1300_crop.h5") #делаем запрос
    f.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
    f.close()
    
    #Загружаем данные
    h5f = h5py.File('file4.h5','r')
    frame0 = h5f["data"][:][0]
    
    #Настройка геометрии 
    geom = Geometry(frame0, 'not_auto')
    p = geom.auto_make()
    start_point = p['start_point'][0] -2, p['start_point'][1]+2
    geom.set_parametrs( start_point = start_point)
    geom.show()
    
    #Класс WFSData
    wfs = WFSData(source = h5f, geometry = geom.geometry)
  #  wfs.save('datageom.h5')
    wfs.reference = 126
    wfs.show_gometry()
   # print(wfs.reference)
#
    plt.figure(figsize = (10, 10))
    plt.subplot(1,4,1)
    plt.imshow(wfs[0][4])
#    ofset = list(wfs[0]['ofsets'][4])
#    plt.title('%d - Ofset: %.1f,%.1f'%(4, ofset[0],ofset[1]))
    
    plt.subplot(1,4,2)
    plt.imshow(wfs[0][11])
#    ofset = list(wfs[0][11])
#    plt.title('%d - Ofset: %.1f,%.1f'%(11, ofset[0],ofset[1]))
    
    plt.subplot(1,4,3)
    plt.imshow(wfs[0][180])
#    ofset = list(wfs[0][180])
#    plt.title('%d - Ofset: %.1f,%.1f'%(180, ofset[0],ofset[1]))
    
    plt.subplot(1,4,4)
    plt.imshow(wfs[0][187])
#    ofset = list(wfs[0]['ofsets'][187])
#    plt.title('%d - Ofset: %.1f,%.1f'%(187, ofset[0],ofset[1]))
    
    plt.tight_layout()
    plt.show()
    
    h5f.close()
    
    print(wfs[0].get_offset(187))

  #  wfs_new = WFSData('datageom.h5','r')
   # wfs_new.show_gometry()
    #plt.imshow(wfs_new[5][45])

    