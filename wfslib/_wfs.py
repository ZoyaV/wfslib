import pywt
import numpy as np
from collections import Counter
import math


def rotate2d(point,origin,degrees):
    """
    A rotation function that rotates a point around a point
    to rotate around the origin use [0,0]
    """
    x = point[0] - origin[0]
    yorz = point[1] - origin[1]
    newx = (x*math.cos(math.radians(degrees))) - (yorz*math.sin(math.radians(degrees)))
    newyorz = (x*math.sin(math.radians(degrees))) + (yorz*math.cos(math.radians(degrees)))
    newx += origin[0]
    newyorz += origin[1] 

    return int(newx+(0.5)*(newx/abs(newx))), int(newyorz+(0.5)*(newyorz/abs(newyorz)))

def qualitative_sub(cell, std, max_val):
        return np.max(cell) > std

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def get_interval(extremums):
    extremums = sorted(extremums)
    widths = []
    for i in range(1,len(extremums)):
        widths.append(extremums[i]-extremums[i-1])
    return widths

def get_extrememums(signal, shifting = 10):
    sort_sig =moving_average(sorted(signal), shifting)

    std = np.std(sort_sig)
    std_max = np.mean([std, np.max(sort_sig)])
    std_min = np.mean([-std, np.min(sort_sig)])
    return std_max, std_min
        
def clear_extremums(maxes):
        main_points = []
        last_point = 0
        mean_point = []
    
        for point in maxes:
            if (point-1) == last_point:
                mean_point.append(point)
            else:            
                if len(mean_point)!=0:
                    main_points.append((np.max((mean_point))))
                mean_point = []
            last_point = point
        return main_points
    
def detect_start_point( p1, p2, p3):
    diff1 = p3 - p2
    diff2 = p2 - p1
    
    if diff1 > diff2:
        return p3
    else:
        return p2
    
def get_cell_parametrs(lines):
    d1 = 0  
    d2 = 0
    d =[]
    lines = sorted(list(set(lines)))

    for i in range(2,len(lines),2):
        d.append(abs(lines[i] - lines[i-1]))
    d1 = np.median(d)
    d = []
    for i in range(1,len(lines),2):
        d.append(abs(lines[i] -lines[i-1]))
    d2 = np.median(d)

    return {"cell_width":max(d2,d1), "border":min(d2,d1)} 


def chose_optimal_interval(cd, end = 3): 
    cur_lvl = len(cd)-1
    zoom = 2
    max_interval = []
    min_interval = []
    while cur_lvl != end:
        std_max,  std_min= get_extrememums(cd[cur_lvl], 15)
        mask1 = list(np.where(cd[cur_lvl] > std_max)[0])
        mask2 = list(np.where(cd[cur_lvl] < std_min)[0])
        I = np.asarray(get_interval(mask1 + mask2)) #все найденные интервалы 
        
        if len(set(I))<8:
            std = np.std(I)
            max_intervals = np.where(I>std)[0]
            big_width = np.mean(I[I>std])
    
            c = []

            for i in range(1,len(max_intervals)): #нахождение минимального интервала
                c+= [sum(I[max_intervals[i-1]+1:max_intervals[i]])]
            min_width = np.median(c)
            max_interval.append(big_width*zoom)
            min_interval.append(min_width*zoom)
          #  print(big_width*zoom, min_width*zoom)
        else:
            pass
        zoom*=2
        cur_lvl-=1
    return (max_interval, min_interval)   


def grid_cell_parametrs(img_grid):
    w = pywt.Wavelet('db2')
    max_lvl = pywt.dwt_max_level(len(img_grid), w.dec_len)-1
    coeffs = pywt.wavedec(np.mean(img_grid,axis = 0), 'db2', level = max_lvl)   
    ca, cd = coeffs[0],coeffs[1:]  
    max_interval_h, min_interval_h = chose_optimal_interval(cd)
    
    w = pywt.Wavelet('db2')
    max_lvl = pywt.dwt_max_level(len(img_grid), w.dec_len)
    coeffs = pywt.wavedec(np.mean(img_grid,axis = 1), 'db2', level = max_lvl)   
    ca, cd = coeffs[0],coeffs[1:]  
    max_interval_w, min_interval_w = chose_optimal_interval(cd)
    
    max_interval = max_interval_h + max_interval_w
    min_interval = min_interval_h + min_interval_w
    
    max_v = Counter(max_interval).most_common(1)[0]
    min_v = Counter(min_interval).most_common(1)[0]
    
    if min_v[1]==1:
        min_v = np.median(min_interval)
    else:
        min_v = min_v[0]
    if max_v[1]==1:
        max_v = np.median(max_interval)
    else:
        max_v = max_v[0]
    return max_v, min_v


def detect_grid_lines(image,  direction = 0):
    h_line = np.median(image, 0)
    w_line = np.median(image, 1)
    
    diff_h = np.diff(moving_average(h_line, 4))
    h_maxes = np.where(abs(diff_h)>np.mean(np.abs(diff_h)))
    h_maxes = clear_extremums(h_maxes[0])

    diff_w = np.diff(moving_average(w_line, 4))
    w_maxes = np.where(abs(diff_w)>np.mean(np.abs(diff_w))) 
    w_maxes = clear_extremums(w_maxes[0])

    start_point_h = int(detect_start_point(h_maxes[1],h_maxes[2],h_maxes[3]))
    start_point_w = int(detect_start_point(w_maxes[1],w_maxes[2],w_maxes[3]))
    
    width, border = grid_cell_parametrs(image)
        
#        'start_h': start_point_h, 'start_w': start_point_w, 'width_lines': w_maxes, 'height_lines': h_maxes, 
#               'cell_width':width, 'border':border
    return [start_point_h, start_point_w,  
            w_maxes, h_maxes, 
            width, border]
    
def make_gridpoints(image, cell_width, border, start_point ):
    x, y = start_point
    X = []
    Y = []
 
    for i in range(int(x), 0, -int(cell_width+border)):
        X.append(i)
        X.append(i+border)
    X.pop(-2)
    X = X[::-1]
    
    for i in range(int(x), image.shape[0], int(cell_width+border)):
        if i == int(x):
            continue
        X.append(i)
        X.append(i+border)

    X.pop(-1)
    X = sorted(X)
    
    for i in range(int(y), 0, -int(cell_width+border)):
        Y.append(i)
        Y.append(i+border)
    Y.pop(-2)
    Y = Y[::-1]
    
    for i in range(int(y), image.shape[1], int(cell_width+border)):
        if i == int(y):
            continue
        Y.append(i)
        Y.append(i+border)
        
    Y.pop(-1)
    Y = sorted(Y)
    return (X,Y)

def points2grid(x_points, y_points):    
    cell = []
    cells = []
    
    for i in range(0,len(x_points),2):
        for j in range(0,len(y_points),2):
            cell = [(x_points[i], x_points[i+1],x_points[i],x_points[i+1]),
                    (y_points[j],y_points[j], y_points[j+1],y_points[j+1])]
            cells.append(cell)
    
    return cells    

def rotate(cells, origin, degrees):
    for i in range(len(cells)):
        cell = list(zip(*cells[i]))
        X = []
        Y = []
        for j in range(len(cell)):
            x,y = rotate2d(cell[j],origin,degrees)
            X.append(x)
            Y.append(y)
        cells[i] = [tuple(X), tuple(Y)]
    return cells