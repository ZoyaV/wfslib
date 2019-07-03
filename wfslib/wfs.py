import h5py  # type: ignore
import numpy  # type: ignore
from skimage.feature import register_translation
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
        self._reference = 81
        self._source = None
        self._geometry = None
        self._subapertures = None

        self.__load_source(source)
        self.__load_geometry( geometry)

    def __load_source(self, source) -> None:
        if isinstance(source, str):
            #Проверка имени
            h5f = h5py.File(source,'r')
            if "data" in h5f.keys():
                self._source = h5f["data"][:]
            if "geometry" in h5f.keys():
                self._geometry = h5f["geometry"][:] 
            h5f.close() 
        if isinstance(source, h5py.File):
            #проверка имени
            if "data" in source.keys():
                self._source = source["data"][:]
            if "geometry" in source.keys():
                self._geometry = source["geometry"][:]      
                
        if isinstance(source, numpy.ndarray):
            self._source = source
      #  raise NotImplementedError()
    def __load_geometry(self, geometry: Union[numpy.ndarray, None]) -> None:
        if isinstance(self._geometry, type(None)):
            return
        if isinstance(self._geometry, type(None)) and isinstance(geometry, type(None)):
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

    def __getitem__(self, frame_number: int) -> dict:        
        self.__load_subapertures(frame_number)
        ofsets = []
        for i, sub in enumerate(self._subapertures):
            shift, _, _ = register_translation(self._subapertures[self._reference], 
                                               self._subapertures[i], 100)
            ofsets.append(shift)
        data = {"ofsets": ofsets, "subaps": self._subapertures}
        return data
    
    def add_geometry(self, geometry: numpy.ndarray) -> None:
        self._geometry = geometry
        
    def save(self, name:str) -> None:
        #FileName Warning
        with h5py.File(name, 'w') as f:
            f.create_dataset("data", data=self._source)
            f.create_dataset("geometry", data=self._geometry) 
            
    def __qualitative_sub(self, cell):
        t = 140
        arr_good = cell[cell>=t].ravel().shape[0]
        arr_bad = cell[cell<t].ravel().shape[0]
        if arr_bad*1.2 > arr_good:
            return 0
        else:
            return 1

    @property
    def reference(self) -> Union[int, None]:
        return self._reference

    @reference.setter
    def reference(self, ref_num):
        self._reference = ref_num

    @property
    def geometry(self) -> numpy.ndarray:
        return self._geometry

    def show_gometry(self) -> None:
        self.__load_subapertures(0)
        plt.figure(figsize = (8,8))         
        plt.imshow(self._source[0])
        for i in range(len(self._geometry)):
            weight = 'normal'
            if self.__qualitative_sub(self._subapertures[i]):
                color = '#f6416e'
            else:
                color = 'c'
            if i == self._reference:
                color = 'r'
                weight = 'bold'
            x0, x1, x2, x3 = self._geometry[i][1]
            y0, y1, y2, y3 = self._geometry[i][0]
            
            plt.text(x0+1, y0+11, "%s"%i, color = color, fontsize = 8, weight=weight)
            plt.plot([x0, x1], [y0, y1], 
                     [x0, x2], [y0, y2],
                     [x2, x3], [y2, y3],
                     [x3, x1], [y3, y1],color = color)
      
        plt.show()
       # raise NotImplementedError()
