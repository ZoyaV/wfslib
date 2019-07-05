import pytest

import numpy as np
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as st_arrays

from geometry import Geometry
from wfs import WFSData


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
