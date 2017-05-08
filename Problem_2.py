import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt

#Read Image
img=cv2.imread('pepsi.jpg')

# Pivot co-ordinates and scale are given
x_coord = sys.argv[1]
y_coord = sys.argv[1]
scale =   sys.argv[2]

# Defining co-ordinates to create a window around the point of interest
# The window is proportional to size of original image, to maintain aspect ratio
tl_x = int(x_coord - (float(1)/float(scale) * float(1)/float(2) * img.shape[1]))
tl_y = int(y_coord - (float(1)/float(scale) * float(1)/float(2) * img.shape[0]))

# Defining the top left, and bottom right co-ordinates
br_x = int(tl_x + (float(1)/float(scale) * img.shape[1]))
br_y = int(tl_y + (float(1)/float(scale) * img.shape[0]))

# The window is adjusted, if it happens to be going out of the scope of the original image size
if (tl_x < 0):
    br_x = br_x - tl_x
    tl_x = 0
if (tl_y < 0):
    br_y = br_y - tl_y
    tl_y = 0

if (br_x > img.shape[1]):
    tl_x = tl_x - (br_x - img.shape[1])
    br_x = img.shape[1]
if (br_y > img.shape[0]):
    tl_y = tl_y - (br_y - img.shape[0])
    br_y = img.shape[0]

# The window is applied over the image to get only the required image portion 
# roi - region of interest
roi=img[tl_y:br_y, tl_x:br_x,:]

# The width and height of this roi is stored
width1=(roi.shape[1])-1
height1=(roi.shape[0])-1

# The width and height of original image is stored
width2 = img.shape[1]
height2 = img.shape[0]

# Width Ratio and Height Ratio are calculated
width_ratio=float(width1)/float(width2)
height_ratio=float(height1)/float(height2)

# A count variable is defined to keep track of number of elements stored in the array
count=0

# The new image's array is initialised
new=[]

# Every pixel of ther region of interest is traversed
# We perform bilinear interpolation for the 3 channels (B,G,R) of the image
for i in range((height2)):
    for j in range((width2)):
        x = int(width_ratio*j)
        y = int(height_ratio*i)
        x_diff = (width_ratio*j) - x
        y_diff = (height_ratio*i) -y

# The neighbouring co-ordinates are compared
# The 'if-else' conditions are added to check for the extreme co-ordinates
if (x>=(width1-1) or y>=(height1-1)):
    A_blue = roi[y][x][0]
    A_red = roi[y][x][1]
    A_green = roi[y][x][2]
else:
    A_blue = roi[y][x][0]
    A_red = roi[y][x][1]
    A_green = roi[y][x][2]

if ((x+1)>=(width1-1) or (y>=(height1-1))):
    B_blue = roi[y][x][0]
    B_red = roi[y][x][1]
    B_green = roi[y][x][2]
else:
    B_blue = roi[y+1][x][0] & 0xff
    B_red = roi[y+1][x][1]
    B_green = roi[y+1][x][2]

if (x>=(width1-1) or ((y+1)>=(height1-1))):
    C_blue = roi[y][x][0]
    C_red = roi[y][x][1]
    C_green = roi[y][x][2]
else:
    C_blue = roi[y][x+1][0] & 0xff
    C_red = roi[y][x+1][1]
    C_green = roi[y][x+1][2]

if ((x+1)>=(width1-1) or (y+1)>=(height1-1)):
    D_blue = roi[y][x][0] & 0xff
    D_red = roi[y][x][1]
    D_green = roi[y][x][2]
else:
    D_blue = roi[y+1][x+1][0] & 0xff
    D_red = roi[y+1][x+1][1]
    D_green = roi[y+1][x+1][2]

# Combining all the different channelsn into overall 3 channels
newimg_blue = (int) ( (A_blue * (1 - x_diff) * (1 - y_diff)) + (B_blue * (x_diff) * (1 - y_diff)) + (C_blue * (y_diff)*(1 - x_diff)) + (D_blue * (x_diff*y_diff)))
newimg_red = (int) ( (A_red * (1 - x_diff) * (1 - y_diff)) + (B_red * (x_diff) * (1 - y_diff)) + (C_red * (y_diff)*(1 - x_diff)) + (D_red * (x_diff*y_diff)))
newimg_green = (int) ( (A_green * (1 - x_diff) * (1 - y_diff)) + (B_green * (x_diff) * (1 - y_diff)) + (C_green * (y_diff)*(1 - x_diff)) + (D_green * (x_diff*y_diff)))

# Adding the values into the array
newrow=count/(width2)
newcol=count%(width2)
newimg = [newimg_blue,newimg_red,newimg_green]
if(newcol == 0):
    new.append([])
new[newrow].append(newimg)
count+=1

final_img=np.uint8(new)

titles = ['Original Image','Zoomed Image']
images = [img,final_img]
for i in xrange(2):
    plt.subplot(2,2,i+1),plt.imshow(images[i])
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
    plt.show()

