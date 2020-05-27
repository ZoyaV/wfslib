# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:52:51 2020

@author: mi
"""



from numba import jit, njit, objmode, prange
from numba.typed import List

import numpy as np

@njit
def translation(ref1, ref2):
    s = np.zeros_like(ref1)    
    with objmode(s='intp[:,:]'):
        s = np.abs(np.fft.ifft2(np.fft.fft2(ref1) * np.conjugate(np.fft.fft2(ref2))))
    with objmode(arr='intp[:]'):
        arr = np.asarray(np.where(s == np.min(s))).ravel()
    return [ref1.shape[1]//2 - arr[0], ref1.shape[1]//2  - arr[1]]

@jit(nopython=True, parallel=True)
def translations(size:int, subs:np.ndarray, ref:np.ndarray):     
    offsets = List()
    x = 0
    y = 0
    for i in prange(size):          
        x, y = translation(subs[i], ref)
        offsets.append((x,y))
    return offsets