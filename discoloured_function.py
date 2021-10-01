# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 10:51:41 2021

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

def dis(image,Tot_count):
    brightness = 0
    contrast = 20
    img = np.int16(image)
    img = img * (contrast/127+1) - contrast + brightness
    img = np.clip(img, 0, 255)
    img1 = np.uint8(img)
    kernel = np.ones((3,3),np.uint8)
    copy=img1.copy()

    hsv = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
    
    lower_color = np.array([0,15,10]) 
    upper_color = np.array([50,200,200])
    
    discoloured = cv2.inRange(hsv, lower_color, upper_color)
    from skimage.segmentation import clear_border
    discoloured = clear_border(discoloured)
    sure_bg = cv2.dilate(discoloured,kernel,iterations=3)
    #sure_bg = cv2.erode(sure_bg,kernel,iterations=1)
    #cv2.imshow('discoloured', discoloured)
    #cv2.imshow('sure_bg', sure_bg)
    
    contours,hierarchy = cv2.findContours(sure_bg,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    Dis_count=len(contours)
    print("Number of Discoloured Rice",Dis_count)
    print("% of Discoloured Rice",(Dis_count/Tot_count)*100)
    
    p=1
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        ROI = sure_bg[y:y+h, x:x+w]
        cv2.rectangle(copy,(x-5,y-5),(x+w+5,y+h+5),(36,255,12),1)
        rect = cv2.minAreaRect(c)             # rect = ((center_x,center_y),(width,height),angle)
# print("width & length",rect[1][0])
        points = cv2.boxPoints(rect)         # Find four vertices of rectangle from above rect
 #print("points",points)
        points = np.int0(np.around(points))     # Round the values and make it integers

    #ellipse = cv2.fitEllipse(cnt)           # ellipse = ((center),(width,height of bounding rect), angle)


    #print("count",total_count)
   # print("width",ellipse[1][0])
   # print("length",ellipse[1][1])
   # print("Aspect_Ratio (W/L)",ellipse[1][0]/ellipse[1][1])
   # print("Length/Width Ratio",ellipse[1][1]/ellipse[1][0])
        cv2.drawContours(copy,[c],0,(0,255,0),1)   # draw contours in green color
#print([cnt])
    #cv2.ellipse(img,ellipse,(0,255,0),1)        # draw ellipse in blue color
        cv2.polylines(copy,[points],True,(0,0,255),1)# draw rectangle in red color
        cv2.putText(copy, "D{}".format(p),(x+w+5,y+h+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        p+=1
        #cv2.imshow('input',copy)
     
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return copy    
cv2.waitKey(0)
cv2.destroyAllWindows()    