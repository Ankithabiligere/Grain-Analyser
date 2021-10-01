# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 16:38:01 2021

@author: 91872
"""

import cv2
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import measure, color, io
from skimage.feature import peak_local_max
from scipy import ndimage as ndi
import skimage
#img = cv2.imread("images/ROI/ROI_66.png")
#img = cv2.resize(img, (1104, 1376))
#img = img[300:1376, 0:1104]
def dd(img):
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, thresh= cv2.threshold(im_gray, 128, 192, cv2.THRESH_OTSU)
    thresh=255-thresh
    kernel = np.ones((5,5),np.uint8)
    #gradient = cv2.morphologyEx(thresh,cv2.MORPH_GRADIENT,kernel, iterations =1 )
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations =0 )
    
    from skimage.segmentation import clear_border
    opening = clear_border(opening) #Remove edge touching grains
    plt.imshow(opening, cmap='gray') #This is our image to be segmented further using watershed
    
    sure_bg = cv2.dilate(opening,kernel,iterations=10)
    plt.imshow(sure_bg, cmap='gray') #Dark region is our sure background
    
    sure_bg = cv2.erode(opening,kernel,iterations=0)
    plt.imshow(sure_bg, cmap='gray') #Dark region is our sure background
    
    dist_transform = cv2.distanceTransform(sure_bg,cv2.DIST_L2,5)
    #dist_transform=np.uint8(dist_transform)
    plt.imshow(dist_transform, cmap='gray') 
    #cv2.imshow('dist_transform',dist_transform)
    #dist_transform=255-dist_transform
    
    local_max_location = peak_local_max(dist_transform, min_distance=6, indices=True)
    local_max_boolean = peak_local_max(dist_transform, min_distance=6, indices=False)
    
    #print(local_max_boolean)
    
    markers, _ = ndi.label(local_max_boolean)
    segmented = skimage.segmentation.watershed(255-dist_transform, markers, mask=sure_bg)
    plt.imshow(sure_bg, cmap='gray')
    segmented=np.uint8(segmented)
    #cv2.imshow('segmented',segmented)
     
    fig, axes = plt.subplots(ncols=3, figsize=(9, 3), sharex=True, sharey=True)
    ax = axes.ravel()
    
    ax[0].imshow(img, cmap=plt.cm.gray)
    ax[0].set_title('Input image')
    ax[1].imshow(-dist_transform, cmap=plt.cm.gray)
    ax[1].set_title('Distance transform')
    
    ax[2].imshow(segmented, cmap=plt.cm.nipy_spectral)
    
    for a in ax:
        a.set_axis_off()
    
    fig.tight_layout()
    plt.show()
    
    
    contours,hierarchy = cv2.findContours(segmented,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    print("contours",len(contours))
    broken=0
    
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)             # rect = ((center_x,center_y),(width,height),angle)
    # print("width & length",rect[1][0])
        points = cv2.boxPoints(rect)         # Find four vertices of rectangle from above rect
     #print("points",points)
        points = np.int0(np.around(points))     # Round the values and make it integers
    
        ellipse = cv2.fitEllipse(cnt)           # ellipse = ((center),(width,height of bounding rect), angle)
    
    
        #print("count",total_count)
        print("width",ellipse[1][0])
        print("length",ellipse[1][1])
        
        cv2.drawContours(img,[cnt],0,(0,255,0),1)   # draw contours in green color
    #print([cnt])
        cv2.ellipse(img,ellipse,(0,255,0),1)        # draw ellipse in blue color
        cv2.polylines(img,[points],True,(0,0,255),1)# draw rectangle in red color
        length=(ellipse[1][1])     
        Area=(ellipse[1][0]*ellipse[1][1])
        
        if  length <22:
            broken+=1
                       
            print('Broken rice',length) 
            return broken
          
       
        else:
            pass
        
          
       
        
    
        
        
        #cv2.imshow('output',sure_bg)
        #cv2.imshow('input',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return broken
    
      
            
cv2.waitKey(0)
cv2.destroyAllWindows()