import numpy as np

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def clear_extremums(maxes):
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
    
    for i in range(2,len(lines),2):
        d.append(abs(lines[i] - lines[i-1]))
    d1 = np.median(d)
    d = []
    for i in range(1,len(lines),2):
        d.append(abs(lines[i] -lines[i-1])) 
    d2 = np.median(d)

    return {"cell_width":max(d2,d1), "border":min(d2,d1)} 

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
    
    if direction == 0:
        params = get_cell_parametrs(w_maxes[1:] + h_maxes[1:])
    if direction == 1:
        params = get_cell_parametrs(w_maxes[1:] )
    if direction == 2:
        params = get_cell_parametrs(h_maxes[1:] )
        
    width = params["cell_width"]
    border = params["border"]        
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