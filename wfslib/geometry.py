# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:48:30 2019

@author: Zoya
"""

import pickle 
import numpy as np
from _wfs import make_gridpoints, points2grid, detect_grid_lines
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from typing import Union


class Geometry():    
    def __init__(self, image: np.ndarray, make_func = 'not_auto', border = 0, 
                         cell_width = 0, start_point = [0,0]):
        self.image = image
        self._border = border
        self._cell_width = cell_width
        self._start_point = start_point
        self._cells = []
        
        if make_func.lower() == 'auto':
            self.auto_make()
        elif make_func.lower() == 'not_auto':
            if border!= 0 and cell_width!=0:
                self.__make()
            pass        
    
    def __make(self) -> None:
        points = make_gridpoints(self.image, self._cell_width, self._border, self._start_point )
        self._cells = points2grid(*points)
        return 
    
    def auto_make(self, diraction = 0) -> dict:
        parametrs = detect_grid_lines(self.image,  direction = 0)
        self._border = parametrs[-1]
        self._cell_width = parametrs[-2]
        self._start_point = parametrs[:2]
        
        self.__make()
        
        return {'border': self._border, 'cell_width': self._cell_width, 'start_point': self._start_point}
    
    def set_image(self, image: np.ndarray) -> None:
        self.image = image
        
    def set_parametrs(self, border = None, cell_width = None, 
                      start_point = None) -> None:
        if border!=None:
            self._border = border
        if cell_width!=None:
            self._cell_width = cell_width
        if start_point!=None:
            self._start_point = start_point
        
        self.__make()
        
    @property
    def geometry(self) -> np.ndarray:
        return np.asarray(self._cells)
        
    @property
    def parametrs(self) -> list:
        return  {'border': self._border, 'cell_width': self._cell_width, 'start_point': self._start_point}
    
    def show(self):        
        plt.figure(figsize = (8,8))         
        plt.imshow(self.image)
        for i in range(len(self._cells)):
            x0, x1, x2, x3 = self._cells[i][1]
            y0, y1, y2, y3 = self._cells[i][0]
            
            plt.plot([x0, x1], [y0, y1], 
                     [x0, x2], [y0, y2],
                     [x2, x3], [y2, y3],
                     [x3, x1], [y3, y1],color = 'r')
      
        plt.show()

   
        


    
    

    
    
    
        