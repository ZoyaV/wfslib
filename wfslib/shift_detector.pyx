# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:00:47 2020

@author: mi
"""

import numpy as np
cimport numpy as np

DTYPE = np.float64

cpdef tuple translation(np.ndarray ref1, np.ndarray ref2):
    cdef int x, y, xmax, ymax
    xmax = ref1.shape[0]
    ymax = ref1.shape[1]
    cdef np.ndarray s = np.zeros([xmax, ymax], dtype=DTYPE)
    cdef np.ndarray ref1fft = np.fft.fft2(ref1)
    cdef np.ndarray ref2fft = np.conjugate(np.fft.fft2(ref2))    
    s = np.abs(np.fft.ifft2( ref1fft * ref2fft))
    x, y = np.where(s == np.min(s))
    return x,y