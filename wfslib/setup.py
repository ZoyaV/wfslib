# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:22:22 2020

@author: mi
"""

from distutils.core import setup,Extension
from Cython.Build import cythonize
import numpy


setup(
    ext_modules=cythonize("shift_detector.pyx"),
    include_dirs=[numpy.get_include()]
)    

setup(
    ext_modules=[
        Extension("shift_detector", ["shift_detector.c"],
                  include_dirs=[numpy.get_include()]),
    ],
)

# Or, if you use cythonize() to make the ext_modules list,
# include_dirs can be passed to setup()

