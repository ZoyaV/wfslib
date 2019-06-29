import h5py  # type: ignore
import numpy  # type: ignore
from typing import Union

DataSources = Union[str, h5py.File, numpy.ndarray]


    

class WFSError(Exception):
    pass


class WFSData():

    def __init__(self, source: DataSources, 
                     geometry: Union[numpy.ndarray, None]) -> None:
        self._reference = 0
        self._source = None
        self._geometry = None
        self._frames = None

        self.__load_source(source)
        self.__load_geometry(source, geometry)

    def __load_source(self, source) -> None:
        if type(source) == str:
            pass        
        if type(source) == h5py.File:
            key = source.keys()[0]
            self._source = source[key][:]
            if "geometry" in source.keys():
                self._geometry = source["geometry"][:]                
        if type(self._source) == numpy.ndarray:
            pass
      #  raise NotImplementedError()

    def __load_geometry(self, geometry: Union[numpy.ndarray, None]) -> None:
        if self._geometry != None:
            return
        if self._geometry == None and geometry == None:
            #Предупреждение, нет геометрии для файла!
            #Или расчет геометрии автоматом
            pass
        self._geometry = geometry        
      #  raise NotImplementedError()
      
    def __get_cell(self, num:int)->numpy.ndarray:
        cell = self._geometry[num]
        sx, ssx , sy, ssy = list(map(int,[cell[0][0], cell[0][1],
                                       cell[1][0], cell[1][2]]))    
        img_cell = self._source[self.reference][sx:ssx,sy:ssy]
        return img_cell
      
    def __load_frames(self)->None:
        self._frames = []
        for i in range(len(self._geometry)): 
            self._frames.append(self.get_cell(i)) 
        self._frames = numpy.asarray(self._frames)

    def __iter__(self):
        raise NotImplementedError()        
   

    def __getitem__(self, frame_number: int) -> dict:        
        main = self._frames[frame_number]
        
        return {'target_frame':main, 
                'other_frames': numpy.delete(self._frames, frame_number)}
    
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
