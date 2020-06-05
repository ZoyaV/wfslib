import h5py  # type: ignore
import numpy  # type: ignore
from pathlib import Path
from warnings import warn
from ._wfs import qualitative_sub
from .shift_detector_numba import translations
from skimage.feature import register_translation
from skimage.transform import rotate
from typing import Union
from .geometry import Geometry
from skimage.transform import rotate

import pickle
import matplotlib.pyplot as plt
DataSources = Union[str, h5py.File, numpy.ndarray]


    

class WFSError(Exception):
    pass

class Frame():
    def __init__(self, image, geometry, reference, mask = None, qualitative_function = None):
        self._geometry = geometry
        self.image = image
        self.reference = reference
        self.qualitative_function = qualitative_function if qualitative_function else qualitative_sub
        self.mask = mask

        
    def __getitem__(self, sub_number: int) -> numpy.ndarray: 
        if not isinstance(self.mask, type(None)):
            cell = self._geometry.geometry[self.mask][sub_number]
        else:
             cell = self._geometry.geometry[sub_number]
        sx, ssx , sy, ssy = list(map(int,[cell[0][0], cell[0][1],
                                       cell[1][0], cell[1][2]]))           
        return self.image[sx:ssx,sy:ssy]
    
    def __len__(self):
        if not isinstance(self.mask, type(None)):
            return len(self._geometry.geometry[self.mask])
        else:
            return len(self._geometry.geometry)
    
    def cell_quality(self, i:int)->bool:
        cell = self._geometry.geometry[i]
        sx, ssx , sy, ssy = list(map(int,[cell[0][0], cell[0][1],
                                       cell[1][0], cell[1][2]]))
        return self.qualitative_function(self.image[sx:ssx,sy:ssy], 
                               numpy.std(self.image),
                               numpy.mean(self.image))
        
    
    def get_offset(self, sub_number):        
        return register_translation(self.__getitem__(self.reference),
                             self.__getitem__(sub_number))[0]
        
    def set_image(self, image):
        self.image = rotate(image, -self._geometry._rotate, resize=False, center=None, order=1,
                 mode='constant', cval=0, clip=True, preserve_range=False)
    
    def offsets(self, dformat = 'row'):
        offsets = []
        
        for i in range(len(self._geometry.geometry)):
             ofst = list(self.get_offset(i))
             offsets.append([-ofst[0], -ofst[1]])
        offsets = numpy.asarray(offsets)
        if dformat == 'row':
            return offsets
        elif dformat == 'imat':
            return numpy.append(offsets[:,0],offsets[:,1])
    
    def __get_all_subaperturs(self):
        subs = []
        for i in range(len(self._geometry.geometry)):
             subs.append(self[i])
        ref_sub = self[self.reference]
        return numpy.asarray(subs), ref_sub
    
    def qoffsets(self):
        subs, ref_sub = self.__get_all_subaperturs()
        offsets = translations(len(subs), numpy.asarray(subs), ref_sub)
        return numpy.asarray(sorted(offsets, key = lambda a: a[0]))[:,1:]
    

class WFSData():

    def __init__(self, source: DataSources, dataset_name = "data", qualitative_function = None) -> None:
        
        self.dataset_name = dataset_name
        self._reference = 81
        self._source = None
        self.geometry = None
        self.h5f_stream = None        
        self._qualitative_function = qualitative_function if qualitative_function else qualitative_sub
        
        self.__load_source(source)
        self.__load_geometry()
        
        
        self._mask = False
        self._frame = Frame(self._source[0], self.geometry, self._reference,
                                        qualitative_function = self._qualitative_function)
        self.quality_mask = []
        

    def __load_source(self, source) -> None:
        if isinstance(source, str):
            if not Path(source).exists():
                raise WFSError("NameError: not file or directory with name %s."%source)
            if "h5" not in source:
                raise WFSError("TypeError: file is not a hdf5-file format type."%source)
            self.h5f_stream = h5py.File(source,'r')
            if self.dataset_name in  self.h5f_stream.keys():
                print(len( self.h5f_stream[self.dataset_name].shape))
                if len( self.h5f_stream[self.dataset_name].shape)>2:
                    self._source = self.h5f_stream[self.dataset_name]
                else:
                    self._source = numpy.expand_dims(self.h5f_stream[self.dataset_name], axis=0)
            #plt.imshow(self._source[0])
            if ("cell_width" in self.h5f_stream.keys() and 
                            "border" in self.h5f_stream.keys() and 
                            "start_point" in self.h5f_stream.keys()) :
                cell_width = self.h5f_stream["cell_width"][0]
                border = self.h5f_stream["border"][0]
                start_point = self.h5f_stream["start_point"][0]
                self.geometry = Geometry(image = self._source[0], 
                                         cell_width = cell_width, 
                                         border = border,
                                         start_point = start_point)
          #  h5f.close() 
        elif isinstance(source, h5py.File):
            if self.dataset_name in source.keys():
                self._source = source[self.dataset_name]
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
        elif isinstance(source, numpy.ndarray):
            self._source = source
            if len(source.shape) == 2:
                self._source =  self._source.reshape(1,self._source.shape[0], self._source.shape[1])
        else:
            raise WFSError("I am so sorry! I cant't open file with this format.")      
    
    def close_stream(self):
        self.h5f_stream.close()
        
    def __load_geometry(self) -> None:
        if not isinstance(self.geometry, type(None)):
            return
        self.geometry = Geometry(self._source[0], 'auto')
        warn("WARNING: Set the geometry for the file!", UserWarning)
   
    def __iter__(self):
        raise NotImplementedError()  

    def __getitem__(self, frame_number: int) -> dict: 
#         if self._mask == True:
#             self._frame.mask = self.quality_mask
#         else:
#             self._frame.mask = None
        self._frame.set_image(self._source[frame_number])
        return self._frame
    
    def save(self, name=None) -> None:
        data_name = name if name is not None else self.dataset_name
        if "h5" not in data_name:
            warn("File name is not hdf5 file format", UserWarning)        
        with h5py.File(data_name, 'a') as f:           
            #f.create_dataset(self.dataset_name, data=self._source)
            f.create_dataset("cell_width", data= numpy.asarray([self.geometry._cell_width]))
            f.create_dataset("border", data=numpy.asarray([self.geometry._border]))
            f.create_dataset("start_point", data=numpy.asarray([self.geometry._start_point]))
            
    @property
    def qualitative_function(self):
        return self._qualitative_function 
    
    @qualitative_function.setter
    def qualitative_function(self, qualitative_function):
        self._qualitative_function = qualitative_function
        self._frame.qualitative_function = qualitative_function
        self.quality_mask = self.__get_quality_mask()
    
    @property
    def reference(self) -> Union[int, None]:
        return self._reference

    @reference.setter
    def reference(self, ref_num):
        self._reference = ref_num
        self._frame.reference = self._reference
        
    @property
    def good_only(self):
        return self._mask
    
    @good_only.setter
    def good_only(self, state) -> bool:
        self._mask = state
        if self._mask:
            self.quality_mask = self.__get_quality_mask()
        self.geometry.mask = self.quality_mask
        return 
    
    def __get_quality_mask(self):
        geometry = self.geometry.geometry
        mask = numpy.zeros(geometry.shape[0])
        mask = mask.astype(bool)
        for i in range(len(geometry)):
             if self._frame.cell_quality(i):
                 mask[i] = True 
             else:
                 mask[i] = False
        return mask

    def show_geometry(self, show_type = "numered") -> None:
        self._frame.set_image(self._source[0])
        plt.figure(figsize = (10,10))   
        img_to_show = rotate(self._source[0], -self.geometry._rotate, resize=False, center=None, order=1,
                 mode='constant', cval=0, clip=True, preserve_range=False) 
        plt.imshow(img_to_show)
        plt.title(show_type+" image")
        sx = 1
        sy = 11
       # if self._mask:
          #  geometry = self.geometry.geometry[self.quality_mask]
      #  else:
        geometry = self.geometry.geometry
        for i in range(len(geometry)):

            weight = 'normal'
            fontsize = 12
            if self._mask or self._frame.cell_quality(i):
                color = '#f6416e'
            else:
                color = 'c'
            if i == self._reference:
                color = 'r'
                weight = 'bold'
            x0, x1, x2, x3 = geometry[i][1]
            y0, y1, y2, y3 = geometry[i][0]
            
            text = ""
            if show_type == "numered":
                text = "%d"%i
            elif show_type == "offsets":
                ofst = self._frame.get_offset(i)
                text = "%.1f,  %.1f"% (-ofst[0], -ofst[1])
                fontsize = 10
                sx = 2
                sy = 12
                
            plt.text(x0+sx, y0+sy, text, color = color, fontsize = fontsize, weight=weight)
            plt.plot([x0, x1], [y0, y1], 
                     [x0, x2], [y0, y2],
                     [x2, x3], [y2, y3],
                     [x3, x1], [y3, y1],color = color)
      
        plt.show()
        
   
