import pytest

import numpy as np
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as st_arrays

from wfslib.geometry import Geometry
from wfslib.wfs import WFSData
import numpy as np
import time

def main():
    
    #Скачиваем файл      
#    f=open(r'file.h5',"wb") #открываем файл для записи, в режиме wb
#    ufr = requests.get("https://cloud.iszf.irk.ru/index.php/s/odHPMppnvbgUHFW/download?path=%2F&files=sunspot1300_crop.h5") #делаем запрос
#    f.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
#    f.close()
##
    wfs = WFSData('one_frame.h5', dataset_name = "image")
    p = wfs.geometry.options
    wfs.geometry.set_options( shift = (-1,2))
    wfs.reference = 87
    wfs.show_geometry(show_type = "offsets")
    a = time.time()
    wfs.offsets()
    b = time.time()
    print(b-a)
#    plt.imshow(wfs[0][172])    
    print(wfs[0].get_offset(167))
    
    #wfs.save('geometred_file.h5')
#    wfs_saved = WFSData('geometred_file.h5')
#    
#    wfs_saved.show_geometry()

if __name__ == "__main__":
    main()


# def test_wfsdata_cls(load_examples):
#     data = load_examples
#
#     for _ in range(len(data)):
#         image = data[data.files[_]]
#
#         geom = Geometry(image, 'auto')
#
#         wfs = WFSData(source=image)
#
#         # wfs.save(sourse)
#         wfs.reference = 1
#
#         offset = list(wfs[0]['ofsets'][4])
#         assert offset != None
