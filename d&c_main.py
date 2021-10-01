# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 10:26:38 2021

@author: 91872
"""

'''import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import measure, color, io
from skimage.feature import peak_local_max
from scipy import ndimage as ndi
import skimage
import discoloured_function
import chalky_function

image = cv2.imread("D:/a/ANKITHA/Professional/ASPIRE/images/mix_rice.jpg")
image = cv2.resize(image, (1104, 1376))
image= image[300:1376, 0:1104]

Tot_count=45
a=discoloured_function.dis(image,Tot_count)
cv2.imshow('a',a) 
cv2.waitKey(0)
cv2.destroyAllWindows()
b=chalky_function.Chal(image, Tot_count,a)

cv2.imshow('b',b) 
cv2.waitKey(0)
cv2.destroyAllWindows()'''

import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import measure, color, io
from skimage.feature import peak_local_max
from scipy import ndimage as ndi
import skimage
import discoloured_function
import chalky_function
import clwa_function
import broken_function
#import good_function

image = cv2.imread("D:/a/ANKITHA/Professional/ASPIRE/images/mix_rice3.jpg")
image = cv2.resize(image, (1104, 1376))
image= image[300:1376, 0:1104]
cv2.imshow('original image', image)
copy = image.copy()
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#thresh = cv2.threshold(gray,10,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
#thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
LAB= cv2.cvtColor(image,cv2.COLOR_BGR2LAB)
L,A,B=cv2.split(LAB)
discoloured = cv2.inRange(B, 0, 95)
cnts = cv2.findContours(discoloured, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
p=0
Tot_count=0
count=0
count1=0
count2=0
count3=0
count4=0
count5=0
Tot_broken=0
#Tot_good=0
for c in cnts:
    
    x,y,w,h = cv2.boundingRect(c)
    ROI = discoloured[y:y+h, x:x+w]
    aa=w*h
    #print(w*h)
       
    if aa<=100:
        pass
    else:
           
        a= image[y-4:y+h+5, x-4:x+w+5]
        try:
            
           count1,count2,count3,count4,count5=clwa_function.dd(a)
           count=count1+count2+count3+count4+count5
           Tot_count+=count
           broken=broken_function.dd(a)
           Tot_broken+=broken
           #good=good_function.dd(a)
           #Tot_good+=good
        except:
            pass
        
             
        
       
        
        
        
        #cv2.imwrite('C:/Users/admin/ASPIRE/ROI_30/ROI_{}.png'.format(ROI_number), a)
        cv2.rectangle(copy,(x-5,y-5),(x+w+5,y+h+5),(36,255,12),1)
        cv2.putText(copy, "{}".format(p),(x+w+5,y+h+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 150), 2)
        p+=1
        #print("FFs",x+w,y+h)
            
        
        #cv2.imshow('ROI', a)
        key = cv2.waitKey(10)
        if key == 27: # Esc
             break
print("Tot_count=",Tot_count)
print("Tot_Broken=",Tot_broken)
#print("Tot_Good=",Tot_good)

cv2.imshow('output', copy)

print(p+1)

a=discoloured_function.dis(image,Tot_count)
cv2.imshow('a',a) 
cv2.waitKey(0)
cv2.destroyAllWindows()
b=chalky_function.Chal(image, Tot_count,a)

cv2.imshow('b',b) 
cv2.waitKey(0)
cv2.destroyAllWindows()