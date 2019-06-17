import h5py  # type: ignore
import numpy  # type: ignore
from typing import Union

DataSources = Union[str, h5py.File, numpy.ndarray]


class WFSError(Exception):
    pass


class WFSData():

    def __init__(self, source: DataSources) -> None:
        self._reference = None
        self._source = None
        self._geometry = None

        self.__load_source()
        self.__load_geometry()

    def __load_source(self) -> None:
        raise NotImplementedError()

    def __load_geometry(self) -> None:
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, frame_number: int) -> numpy.ndarray:
        raise NotImplementedError()

    @property
    def reference(self) -> Union[int, None]:
        return self._reference

    @reference.setter
    def reference(self, ref_num):
        self._reference = ref_num

    @property
    def geometry(self) -> dict:
        raise NotImplementedError()

    def show_gometry(self) -> None:
        raise NotImplementedError()
