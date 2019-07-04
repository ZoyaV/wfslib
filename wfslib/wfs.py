import h5py  # type: ignore
import numpy  # type: ignore
from pathlib import Path
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
        cell = self._geometry.geometry[sub_number]
        sx, ssx , sy, ssy = list(map(int,[cell[0][0], cell[0][1],
                                       cell[1][0], cell[1][2]]))           
        return self.image[sx:ssx,sy:ssy]
    def __len__(self):
        return len(_geometry.geometry)
    
    def get_offset(self, sub_number):
        return register_translation(self.__getitem__(self._reference),
                             self.__getitem__(sub_number))[0]
        
    def set_image(self, image):
        self.image = image
    

class WFSData():

    def __init__(self, source: DataSources, dataset_name = "data") -> None:
        
        self.dataset_name = dataset_name
        self._reference = 81
        self._source = None
        self.geometry = None

        self.__load_source(source)
        self.__load_geometry()
        
        self._frame = Frame(self._source[0], self.geometry, self._reference)

    def __load_source(self, source) -> None:
        if isinstance(source, str):
            if not Path(source).exists():
                raise WFSError("NameError: not file or directory with name %s."%source)
            if "h5" not in source:
                raise WFSError("TypeError: file is not a hdf5-file format type."%source)
            h5f = h5py.File(source,'r')
            if self.dataset_name in h5f.keys():
                self._source = h5f[self.dataset_name][:]
            if ("cell_width" in h5f.keys() and 
                            "border" in h5f.keys() and 
                            "start_point" in h5f.keys()) :
                cell_width = h5f["cell_width"][0]
                border = h5f["border"][0]
                start_point = h5f["start_point"][0]
                self.geometry = Geometry(image = self._source[0], 
                                         cell_width = cell_width, 
                                         border = border,
                                         start_point = start_point)
            h5f.close() 
        if isinstance(source, h5py.File):
            if self.dataset_name in source.keys():
                self._source = source[self.dataset_name][:]
            if  ("cell_width" in source.keys() and 
                            "border" in source.keys() and 
                            "start_point" in source.keys()):
                cell_width = source["cell_width"][0]
                border = source["border"][0]
                start_point = source["start_point"][0]
                self.geometry = Geometry(image = self._source[0], 
                                         cell_width = cell_width, 
                                         border = border,
                                         start_point = start_point) 
            if self.dataset_name not in source.keys():
                raise WFSError('Сan not read the file. Be sure to have the keys "date" for data WFS.')                
        if isinstance(source, numpy.ndarray):
            self._source = source

    def __load_geometry(self) -> None:
        if not isinstance(self.geometry, type(None)):
            return
        self.geometry = Geometry(self._source[0], 'auto')
        warn("WARNING: Set the geometry for the file!", UserWarning)
   
    def __iter__(self):
        raise NotImplementedError()  

    def __getitem__(self, frame_number: int) -> dict:   
        self._frame.set_image(self._source[frame_number])
        return self._frame
    
    def save(self, name:str) -> None:
        if "h5" not in name:
            warn("File name is not hdf5 file format", UserWarning)
        with h5py.File(name, 'w') as f:
            f.create_dataset(self.dataset_name, data=self._source)
            f.create_dataset("cell_width", data= numpy.asarray([self.geometry._cell_width]))
            f.create_dataset("border", data=numpy.asarray([self.geometry._border]))
            f.create_dataset("start_point", data=numpy.asarray([self.geometry._start_point]))
            

    @property
    def reference(self) -> Union[int, None]:
        return self._reference

    @reference.setter
    def reference(self, ref_num):
        self._reference = ref_num

    def show_geometry(self) -> None:
        self._frame.set_image(self._source[0])
        plt.figure(figsize = (8,8))         
        plt.imshow(self._source[0])
        for i in range(len(self.geometry.geometry)):
            weight = 'normal'
            if qualitative_sub(self._frame[i]):
                color = '#f6416e'
            else:
                color = 'c'
            if i == self._reference:
                color = 'r'
                weight = 'bold'
            x0, x1, x2, x3 = self.geometry.geometry[i][1]
            y0, y1, y2, y3 = self.geometry.geometry[i][0]
            
            plt.text(x0+1, y0+11, "%s"%i, color = color, fontsize = 8, weight=weight)
            plt.plot([x0, x1], [y0, y1], 
                     [x0, x2], [y0, y2],
                     [x2, x3], [y2, y3],
                     [x3, x1], [y3, y1],color = color)
      
        plt.show()
