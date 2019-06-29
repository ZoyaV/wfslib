# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:48:30 2019

@author: Zoya
"""

import pickle 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines


def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

class Geometry():
    
    def __init__(self, image, make_func = 'not_auto', border = 0, 
                         cell_width = 0, start_point = [0,0]):
        self.image = image
        self._border = border
        self._cell_width = cell_width
        self._start_point = start_point
        self._cells = []
        
        if make_func.lower() == 'auto':
            self.auto_make()
        elif make_func.lower() == 'not_auto':
            pass
        
    def auto_make(self, diraction = 0):
        parametrs = self.__detect_grid_lines(diraction)
        self._border = parametrs[-1]
        self._cell_width = parametrs[-2]
        self._start_point = parametrs[:2]
        
        points = self.__make_gridpoints()
        self._cells = self.__points2grid(*points)
        
        return {'border': self._border, 'cell_width': self._cell_width, 'start_point': self._start_point}
    
    def set_image(self, image):
        self.image = image
        
    def set_parametrs(self, border = None, cell_width = None, start_point = None):
        if border!=None:
            self._border = border
        if cell_width!=None:
            self._cell_width = cell_width
        if start_point!=None:
            self._start_point = start_point
        
        points = self.__make_gridpoints()
        self._cells = self.__points2grid(*points)
        
    @property
    def geometry(self):
        return np.asarray(self._cells)
        
    @property
    def parametrs(self):
        return [self._border, self._cell_width, self._start_point]
    
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

    def __clear_extremums(self, maxes):
        main_points = []
        last_point = 0
        mean_point = []
    
        for point in maxes:
            if (point-1) == last_point:
                mean_point.append(point)
            else:            
                if len(mean_point)!=0:
                    main_points.append((np.max(mean_point)))
                mean_point = []
            last_point = point
        return main_points
    
    def __detect_start_point(self, p1, p2, p3):
        diff1 = p3 - p2
        diff2 = p2 - p1
        
        if diff1 > diff2:
            return p3
        else:
            return p2
        
    def __get_cell_parametrs(self, lines):
        d1 = 0  
        d2 = 0
        d =[]
        
        for i in range(2,len(lines),2):
            d.append(abs(lines[i] - lines[i-1]))
        d1 = np.median(d)
        d = []
        for i in range(1,len(lines),2):
            d.append(abs(lines[i] -lines[i-1])) 
        d2 = np.median(d)
    
        return {"cell_width":max(d2,d1), "border":min(d2,d1)} 
    
    def __detect_grid_lines(self, direction = 0):
        h_line = np.median(self.image, 0)
        w_line = np.median(self.image, 1)
        
        diff_h = np.diff(moving_average(h_line, 4))
        h_maxes = np.where(abs(diff_h)>np.mean(np.abs(diff_h)))
        h_maxes = self.__clear_extremums(h_maxes[0])
    
        diff_w = np.diff(moving_average(w_line, 4))
        w_maxes = np.where(abs(diff_w)>np.mean(np.abs(diff_w))) 
        w_maxes = self.__clear_extremums(w_maxes[0])

        start_point_h = int(self.__detect_start_point(h_maxes[1],h_maxes[2],h_maxes[3]))
        start_point_w = int(self.__detect_start_point(w_maxes[1],w_maxes[2],w_maxes[3]))
        
        if direction == 0:
            params = self.__get_cell_parametrs(w_maxes[1:] + h_maxes[1:])
        if direction == 1:
            params = self.__get_cell_parametrs(w_maxes[1:] )
        if direction == 2:
            params = self.__get_cell_parametrs(h_maxes[1:] )
            
        width = params["cell_width"]
        border = params["border"]        
#        'start_h': start_point_h, 'start_w': start_point_w, 'width_lines': w_maxes, 'height_lines': h_maxes, 
#               'cell_width':width, 'border':border
        return [start_point_h, start_point_w,  
                w_maxes, h_maxes, 
                width, border]
        
    def __make_gridpoints(self):
        x, y = self._start_point
        X = []
        Y = []
     
        for i in range(int(x), 0, -int(self._cell_width+self._border)):
            X.append(i)
            X.append(i+self._border)
        X.pop(-2)
        X = X[::-1]
        
        for i in range(int(x), self.image.shape[0], int(self._cell_width+self._border)):
            if i == int(x):
                continue
            X.append(i)
            X.append(i+self._border)

        X.pop(-1)
        X = sorted(X)
        
        for i in range(int(y), 0, -int(self._cell_width+self._border)):
            Y.append(i)
            Y.append(i+self._border)
        Y.pop(-2)
        Y = Y[::-1]
        
        for i in range(int(y), self.image.shape[1], int(self._cell_width+self._border)):
            if i == int(y):
                continue
            Y.append(i)
            Y.append(i+self._border)
            
        Y.pop(-1)
        Y = sorted(Y)
        return (X,Y)
    
    def __points2grid(self, x_points, y_points):    
        cell = []
        cells = []
        
        for i in range(0,len(x_points),2):
            for j in range(0,len(y_points),2):
                cell = [(x_points[i], x_points[i+1],x_points[i],x_points[i+1]),
                        (y_points[j],y_points[j], y_points[j+1],y_points[j+1])]
                cells.append(cell)
        
        return cells    
        

if __name__ == "__main__":
    with open('test.pkl','rb') as f:
         image = pickle.load(f)
    geom = Geometry(image, 'not_auto')
    p = geom.auto_make()
    start_point = p['start_point'][0] -2, p['start_point'][1]
    geom.set_parametrs( start_point = start_point)
    geom.show()
    
    

    
    
    
        