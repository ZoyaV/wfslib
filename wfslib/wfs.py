import h5py  # type: ignore
import numpy  # type: ignore
from typing import Union
from geometry import Geometry

import pickle
import matplotlib.pyplot as plt
DataSources = Union[str, h5py.File, numpy.ndarray]


    

class WFSError(Exception):
    pass


class WFSData():

    def __init__(self, source: DataSources, 
                     geometry: Union[numpy.ndarray, None]) -> None:
        self._reference = 0
        self._source = None
        self._geometry = None
        self._subapertures = None

        self.__load_source(source)
        self.__load_geometry( geometry)

    def __load_source(self, source) -> None:
        if type(source) == str:
            pass        
        if type(source) == h5py.File:
            key = list(source.keys())[0]
            self._source = source[key][:]
            if "geometry" in source.keys():
                self._geometry = source["geometry"][:]                
        if type(self._source) == numpy.ndarray:
            pass
      #  raise NotImplementedError()

    def __load_geometry(self, geometry: Union[numpy.ndarray, None]) -> None:
        if self._geometry != None:
            return
        if type(self._geometry) == type(None) and type(geometry) == type(None):
            #Предупреждение, нет геометрии для файла!
            #Или расчет геометрии автоматом
            pass
        self._geometry = geometry        
      #  raise NotImplementedError()
      
    def __get_cell(self, sub_number:int, frame_number)->numpy.ndarray:
        cell = self._geometry[sub_number]
        sx, ssx , sy, ssy = list(map(int,[cell[0][0], cell[0][1],
                                       cell[1][0], cell[1][2]]))    
        img_cell = self._source[frame_number][sx:ssx,sy:ssy]
        return img_cell
      
    def __load_subapertures(self, frame_number)->None:
        self._subapertures = []
        for i in range(len(self._geometry)): 
            self._subapertures.append(self.__get_cell(i, frame_number)) 
        self._subapertures = numpy.asarray(self._subapertures)

    def __iter__(self):
        raise NotImplementedError()  

    def __getitem__(self, frame_number: int) -> numpy.ndarray:        
        self.__load_subapertures(frame_number)
        return self._subapertures
    
    def add_geometry(self, geometry: numpy.ndarray) -> None:
        self._geometry = geometry
        
    def save(self, name:str) -> None:
        #FileName Warning
        with h5py.File(name, 'w') as f:
            f.create_dataset("source", data=self._source)
            f.create_dataset("geometry", data=self._geometry)        

    @property
    def reference(self) -> Union[int, None]:
        return self._reference

    @reference.setter
    def reference(self, ref_num):
        self._reference = ref_num
        self.__load_frames()

    @property
    def geometry(self) -> numpy.ndarray:
        return self._geometry

    def show_gometry(self) -> None:
        raise NotImplementedError()
#
#if __name__ == "__main__":
#    with open('test.pkl','rb') as f:
#         image = pickle.load(f)
#    geom = Geometry(image, 'not_auto')
#    p = geom.auto_make()
#    start_point = p['start_point'][0] -2, p['start_point'][1]
#    geom.set_parametrs( start_point = start_point)
#    
#    h5f = h5py.File('file2.h5','r')
#    
#    wfs = WFSData(source = h5f, geometry = geom.geometry)    
#    arr = h5f["data"][:]
#    
#    wfs.save("first_test.h5")
#    h5f.close()
#    
#    plt.imshow(wfs[0][34])
#    #geom.show()
    