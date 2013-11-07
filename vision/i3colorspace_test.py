import os
import Image
import cv2
import numpy as np
from skimage import exposure



def array2PIL(arr, size):
    mode = 'RGBA'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)


def rgbToI3(r, g, b):
	"""Convert RGB color space to I3 color space
	@param r: Red
	@param g: Green
	@param b: Blue
	return (I3) integer 
	"""
	i3 = ((2*g)-r-b)/2	 
	return i3

def rgb2I3 (img):
	"""Convert RGB color space to I3 color space
	@param r: Red
	@param g: Green
	@param b: Blue
	return (I3) integer 
	"""
	xmax = img.size[0]
	ymax = img.size[1]
	#make a copy to return
	returnimage = Image.new("RGB", (xmax,ymax))
	imagearray = img.load()
	for y in range(0, ymax, 1):					
		for x in range(0, xmax, 1):
			rgb = imagearray[x, y]
			i3 = ((2*rgb[1])-rgb[0]-rgb[2]) / 2
			#print rgb, i3
			returnimage.putpixel((x,y), (0,i3,0))
	return returnimage

def PIL2array(img):
    return np.array(img.getdata(),
                    np.uint8).reshape(img.size[1], img.size[0], 3)

now = cv2.getTickCount()

img  = cv2.imread('images/temp.jpg')
#print img.shape
#img2 = rgb2I3(array2PIL(img, ([ img.shape[1], img.shape[0] ]) ))
# create a CLAHE object (Arguments are optional).
#clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#cl1 = clahe.apply(img)
cl1 = exposure.equalize_adapthist(img, ntiles_x=8, ntiles_y=8, clip_limit=0.01, nbins=256)

cv2.imwrite('clahe_2.jpg',cl1)
#cv2.imwrite('images/temp_i3_a.jpg', PIL2array(img2))
print cv2.getTickCount() - now
#now = cv2.getTickCount()
#os.system('convert images/temp.jpg -colorspace OHTA -channel G -separate -background black -combine +channel images/temp_i3_b.jpg')
# Seperate the channels you want to keep,
# then combine using a background color to set the other channels

'''
print PIL2array(img2)[0][0]
print '*' * 10    
img2 = cv2.imread('images/temp.jpg')
img4 = cv2.imread('images/temp_i3_a.jpg')
print img[0][0]

print img2[0][0]
img3 = np.copy(img2)
img3[:,:,0] = 0
img3[:,:,2] = 0
#print img2[0][0]
#img3[:,:,1] = img2[:,:,0]*[2]
#print img3
img3[:,:,1] =  ( (img2[:,:,1]*[2] ) - [img2[:,:,0]] - [img2[:,:,2]] ) / [2]
print img3.shape, img3[0][0]
cv2.imwrite('images/temp_i3_c.jpg', img3)
print cv2.getTickCount() - now
'''



