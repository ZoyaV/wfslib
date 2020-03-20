# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 20:05:33 2020

@author: mi
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import gaussian
from random import randint


class WFSGenerationError(Exception):
    pass

def drow_circle(r, offset = [0,0], sigma = 1):
    
    width, height = r*2, r*2
    img = np.zeros((width, height))
    X = np.arange(width).reshape(width,1)
    Y = np.arange(height).reshape(1,height)

    mask_2 = ((X - offset[0]- width//2) ** 2 + (Y  -offset[1]- height//2)**2) < (1)**2
    img[mask_2] = 1    
    img_smooth = gaussian(img, sigma)
    
   ## print(sum(img_smooth[0,:]+img_smooth[:,0]+img_smooth[-1,:]+img_smooth[:,-1]))
    if sum(img_smooth[0,:]+img_smooth[:,0]+img_smooth[-1,:]+img_smooth[:,-1])>2:
        raise WFSGenerationError("Light goes beyond the cell!")    
    return img_smooth


def generate_offsets(width, height, deviant = 5 ):
    
    offsets = np.zeros((width, height, 2))
    for i in range(width):
        for j in range(height):
            x = randint(-deviant,deviant)
            y = randint(-deviant,deviant)
            offsets[i,j,:]= np.asarray([x,y])
    return offsets

def draw_subs(offsets, R, border, sigma = 12):
    countw, counth = offsets.shape[:2]
    
    width = (R*2 + border) * countw
    height = (R*2 + border) * counth
    img = np.zeros((width, height))
    
    for i in range(countw):
        for j in range(counth):
            ci = i*(R*2+border) + border//2
            cj = j*(R*2+border) + border//2
            circle_pattern = drow_circle(R, offsets[i,j], sigma = sigma)
            img[ci:ci+R*2,cj:cj+R*2] = circle_pattern.copy()
            
    return img                   
            
    
if __name__ == "__main__":
    
    R = 100
    border = 10
    sigma = 10
    offsets = generate_offsets(8, 8)
    img = draw_subs(offsets, R, border, sigma = sigma)

#            
    try:
        print("kek")
        plt.figure(figsize = (10,10))
        plt.imshow(img)
    except:
        print("lol")
        pass
#        
        
