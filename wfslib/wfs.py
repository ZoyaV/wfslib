import h5py  # type: ignore
import numpy  # type: ignore
import glob
from warnings import warn
from  _wfs import qualitative_sub
from skimage.feature import register_translation
from typing import Union
from geometry import Geometry

import pickle
import matplotlib.pyplot as plt
DataSources = Union[str, h5py.File, numpy.ndarray]


    

class WFSError(Exception):
    pass

class Frame():
    def __init__(self, image, geometry, reference):
        self.image = image
        self._geometry = geometry
        self._reference = reference
        
    def __getitem__(self, sub_number: int) -> numpy.ndarray: 
        cell = self._geometry[sub_number]
        sx, ssx , sy, ssy = list(map(int,[cell[0][0], cell[0][1],
                                       cell[1][0], cell[1][2]]))           
        return self.image[sx:ssx,sy:ssy]
    
    def get_offset(self, sub_number):
        return register_translation(self.__getitem__(self._reference),
                             self.__getitem__(sub_number))[0]
        
    def set_image(self, image):
        self.image = image
    

class WFSData():

    def __init__(self, source: DataSources, 
                     geometry: Union[numpy.ndarray, None]) -> None:
        self._reference = 81
        self._source = None
        self._geometry = None
        self._subapertures = None

        self.__load_source(source)
        self.__load_geometry( geometry)
        
        self._frame = Frame(self._source[0], self._geometry, self._reference)

    def __load_source(self, source) -> None:
        if isinstance(source, str):
            if source not in glob.glob("*"):
                raise WFSError("NameError: not file or directory with name %s."%source)
            if "h5" not in source:
                raise WFSError("TypeError: file is not a hdf5-file format type."%source)
            h5f = h5py.File(source,'r')
            if "data" in h5f.keys():
                self._source = h5f["data"][:]
            if "geometry" in h5f.keys():
                self._geometry = h5f["geometry"][:] 
            h5f.close() 
        if isinstance(source, h5py.File):
            if "data" in source.keys():
                self._source = source["data"][:]
            if "geometry" in source.keys():
                self._geometry = source["geometry"][:]   
            if "data" not in source.keys():
                raise WFSError('Сan not read the file. Be sure to have the keys "date" for data WFS.')                
        if isinstance(source, numpy.ndarray):
            self._source = source

    def __load_geometry(self, geometry: Union[numpy.ndarray, None]) -> None:
        if not isinstance(self._geometry, type(None)):
            return
        if isinstance(self._geometry, type(None)) and isinstance(geometry, type(None)):
            raise WFSError('No geometry for the file.') 
        self._geometry = geometry  
   
    def __iter__(self):
        raise NotImplementedError()  

    def __getitem__(self, frame_number: int) -> dict:   
        self._frame.set_image(self._source[frame_number])
        return self._frame
    
    def add_geometry(self, geometry: numpy.ndarray) -> None:
        self._geometry = geometry
        
    def save(self, name:str) -> None:
        if "h5" not in name:
            warn("File name is not hdf5 file format", UserWarning)
        with h5py.File(name, 'w') as f:
            f.create_dataset("data", data=self._source)
            f.create_dataset("geometry", data=self._geometry) 
            

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
#        self.__load_subapertures(0)
        self._frame.set_image(self._source[0])
        plt.figure(figsize = (8,8))         
        plt.imshow(self._source[0])
        for i in range(len(self._geometry)):
            weight = 'normal'
            if qualitative_sub(self._frame[i]):
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
