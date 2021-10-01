# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 11:06:58 2021

@author: 91872
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import measure, color, io
from skimage.feature import peak_local_max
from scipy import ndimage as ndi
import skimage

def Chal(image,Tot_count,a):
    brightness = 0
    contrast = 38
    img = np.int16(image)
    img = img * (contrast/127+1) - contrast + brightness
    img = np.clip(img, 0, 255)
    img1 = np.uint8(img)
    kernel = np.ones((3,3),np.uint8)
    copy=img1.copy()

    hsv = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
    
    lower_color = np.array([0,0,255]) 
    upper_color = np.array([0,0,255])
    
    cha = cv2.inRange(hsv, lower_color, upper_color)
    from skimage.segmentation import clear_border
    cha = clear_border(cha)
    sure_bg = cv2.erode(cha,kernel,iterations=1)
    sure_bg = cv2.dilate(sure_bg,kernel,iterations=1)
    #cv2.imshow('chalky', cha)
    #cv2.imshow('sure_bg', sure_bg)
    
    contours,hierarchy = cv2.findContours(sure_bg,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    chalky_count=len(contours)
    print("Number of Chalky Rice",chalky_count)
    print("% of Chalky Rice",(chalky_count/Tot_count)*100)
    
    p=1
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        ROI = sure_bg[y:y+h, x:x+w]
        cv2.rectangle(a,(x-5,y-5),(x+w+5,y+h+5),(36,255,12),1)
        cv2.putText(a, "C{}".format(p),(x+w+5,y+h+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        p+=1
        #cv2.imshow('aa',a)
     
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return a    
cv2.waitKey(0)
cv2.destroyAllWindows()    