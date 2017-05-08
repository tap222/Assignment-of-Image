import cv2
import numpy as np
import sys
import os
import matplotlib.pyplot as plt

img=cv2.imread('pepsi.jpg')
shape = img.shape

# Existing end co-ordinates of the given image
inpts = np.array(np.float32([[0,0],[shape[1]-1,0],[shape[1],shape[0]],[0,shape[0]]]))

# Giving the new input for the co-ordiantes 
outpts = np.array(np.float32([[73, 239], [356, 117], [475, 265], [187, 443]]))

# initialzie a list of coordinates that will be ordered
# such that the first entry in the list is the top-left,
# the second entry is the top-right, the third is the
# bottom-right, and the fourth is the bottom-left
rect = np.zeros((4, 2), dtype = "float32")
 
# the top-left point will have the smallest sum, whereas
# the bottom-right point will have the largest sum
s = outpts.sum(axis = 1)
rect[0] = outpts[np.argmin(s)]
rect[2] = outpts[np.argmax(s)]
 
# compute the difference between the points, the
# top-right point will have the smallest difference,
# whereas the bottom-left will have the largest difference
diff = np.diff(outpts, axis = 1)
rect[1] = outpts[np.argmin(diff)]
rect[3] = outpts[np.argmax(diff)]

# Finding minimum of all the x-coords and minimun of all the y-coords
lowx=min(rect[0][0],rect[1][0],rect[2][0],rect[3][0])
lowy=min(rect[0][1],rect[1][1],rect[2][1],rect[3][1])

# Bringing the points to scale of (0,0)
for i in range(len(outpts)):
    rect[i][0]-=lowx
    rect[i][1]-=lowy

# Finding max of x and y-coords, in new shifted scale
highx=max(rect[0][0],rect[1][0],rect[2][0],rect[3][0])
highy=max(rect[0][1],rect[1][1],rect[2][1],rect[3][1])

# Performing the transformation of image to new co-ordinates
M = cv2.getPerspectiveTransform(inpts,outpts)
fimg = cv2.warpPerspective(img,M,(highx,highy))

titles = ['Original Image','Distorted Image']
images = [img,fimg]
for i in xrange(2):
    plt.subplot(2,2,i+1),plt.imshow(images[i])
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
    plt.show()

