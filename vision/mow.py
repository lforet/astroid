#-------------------------------------------------------------------------------
# Name:        Mown grass edge detector
# Purpose:	   Detect and display the edge between cut and uncut regions of grass
#
# Author:      Alex Louden
#
# Created:     15/11/2012
# Copyright:   (c) Alex 2012
#
# Requirements:	matplotlib, numpy, OpenCV
#-------------------------------------------------------------------------------

import os, cv2
from glob import glob
import matplotlib.pyplot as plt
import numpy as np

# OpenCV uses 0-180 for hue values - green is ~50
min_green = np.array([30,50,50])
max_green = np.array([70,256,250])

kernel5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
kernel10 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
kernel20 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))

def main(filename):
	# Load image
	for fn in glob(filename):
		img = cv2.imread(fn)

	cv2.imshow(filename, img)

	# Blur it
	img_blur = cv2.GaussianBlur(img, (5, 5), 0)
##	cv2.imshow(filename + ' blur', img_blur)

	# Convert to HSV
 	img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)

	# Show HSV histograms
	draw_hist(img_hsv)

	# Get just green sections
	img_green_bw = cv2.inRange(img_hsv, min_green, max_green)
##	cv2.imshow(filename + ' green bw', img_green_bw)

    # Close binary image
	img_green_bw = cv2.morphologyEx(img_green_bw, cv2.MORPH_CLOSE, kernel5)
##	cv2.imshow(filename + ' green bw closed', img_green_bw)

	# Erode a little (remove black borders)
	img_green_bw = cv2.morphologyEx(img_green_bw, cv2.MORPH_ERODE, kernel10)
##	cv2.imshow(filename + ' green bw eroded', img_green_bw)

	# Blur original image more
	blursize = 35 # (Must be odd number)
	img_blur_2 = cv2.GaussianBlur(img, (blursize, blursize), 0)
##	cv2.imshow(filename + ' blur more', img_blur_2)

	# Apply to blurred image
	img_green = cv2.bitwise_and(img_blur_2, img_blur_2, mask=img_green_bw)
	cv2.imshow(filename + ' green applied ', img_green)
	cv2.imwrite(filename.split('.')[0] + 'step1.jpg', img_green)

	# Convert to HSV
	img_hsv = cv2.cvtColor(img_green, cv2.COLOR_BGR2HSV)

	draw_hue(img_hsv)

	# Find minima in hue/frequency histogram
	hue_mid = find_hue_mid(img_hsv)

	# Extract image for either side of hue midpoint
	min_hue = np.array([1,0,0])
	lower_hue = np.array([hue_mid,256,256])
	upper_hue = np.array([hue_mid+1,0,0])
	max_hue = np.array([256,256,256])

	img_lower_hue_bw = cv2.inRange(img_hsv, min_hue, lower_hue)
	img_upper_hue_bw = cv2.inRange(img_hsv, upper_hue, max_hue)

##	cv2.imshow(filename + ' lower hue', img_lower_hue_bw)
##	cv2.imshow(filename + ' upper hue', img_upper_hue_bw)

	# In range mask (add)
	img_valid_mask = cv2.bitwise_or(img_lower_hue_bw, img_upper_hue_bw)

	cv2.imshow(filename + ' valid area', img_valid_mask)

	# Tidy lower hue
	img_lower_hue_bw = cv2.morphologyEx(img_lower_hue_bw, cv2.MORPH_OPEN, kernel10)
	img_lower_hue_bw = cv2.morphologyEx(img_lower_hue_bw, cv2.MORPH_CLOSE, kernel10)
	img_lower_hue_bw = cv2.morphologyEx(img_lower_hue_bw, cv2.MORPH_CLOSE, kernel20)
	cv2.imshow(filename + ' lower hue', img_lower_hue_bw)
	cv2.imwrite(filename.split('.')[0] + 'step2-lower_hue.jpg', img_lower_hue_bw)

    # Tidy upper hue
	img_upper_hue_bw = cv2.morphologyEx(img_upper_hue_bw, cv2.MORPH_OPEN, kernel10)
	img_upper_hue_bw = cv2.morphologyEx(img_upper_hue_bw, cv2.MORPH_CLOSE, kernel10)
	img_upper_hue_bw = cv2.morphologyEx(img_upper_hue_bw, cv2.MORPH_CLOSE, kernel20)
	cv2.imshow(filename + ' upper hue', img_upper_hue_bw)
	cv2.imwrite(filename.split('.')[0] + 'step2-upper_hue.jpg', img_upper_hue_bw)

	# Dilate, intersect
	img_upper_hue_bw_d = cv2.morphologyEx(img_upper_hue_bw, cv2.MORPH_DILATE, kernel5)
	img_lower_hue_bw_d = cv2.morphologyEx(img_lower_hue_bw, cv2.MORPH_DILATE, kernel5)
	img_edge = cv2.bitwise_and(img_upper_hue_bw_d, img_lower_hue_bw_d)

	cv2.imshow(filename + ' edge', img_edge)
	cv2.imwrite(filename.split('.')[0] + 'step3-edge.jpg', img_edge)

	edge_indexes = np.where(img_edge)

	# Red image
	img_out = img.copy()
	img_out[edge_indexes] = [0,0,255]

	cv2.imshow(filename + ' output', img_out)

	cv2.imwrite(filename.split('.')[0] + 'output.jpg', img_out)

	wait()

def wait():
	cv2.waitKey()
	cv2.destroyAllWindows()

def draw_hist(img):
	fig = plt.figure()
	ax = fig.add_subplot(3,1,1)
	ax.set_title('H')
	hist_hue = cv2.calcHist([img], [0], None, [180], [0,180])
	ax.plot(hist_hue)

	ax = fig.add_subplot(3,1,2)
	ax.set_title('S')
	hist_hue = cv2.calcHist([img], [1], None, [256], [0,255])
	ax.plot(hist_hue)

	ax = fig.add_subplot(3,1,3)
	ax.set_title('V')
	hist_hue = cv2.calcHist([img], [2], None, [256], [0,255])
	ax.plot(hist_hue)

	plt.show()

def draw_hue(img):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_title('H')
	hist_hue = cv2.calcHist([img], [0], None, [99], [1,100])
	ax.plot(hist_hue)
	plt.show()

def find_hue_mid(img):
	hist_hue = cv2.calcHist([img], [0], None, [99], [1,100])
	hist_hue = np.array([i[0] for i in hist_hue.tolist()])
	b = (np.diff(np.sign(np.diff(hist_hue))) > 0).nonzero()[0] + 1
	print b
	# Find non-zero min
	idx = min([(i,hist_hue[i]) for i in b if hist_hue[i] > max(hist_hue)/100], key=lambda x: x[1])
	print idx
	return idx[0]

if __name__ == '__main__':
	os.chdir('G:\Projects\GrassMow')
	main('half-mown1.jpg')
##	main('half-mown2.jpg')
##	main('half-mown3.jpg')
##	main('half-mown4.jpg')

	cv2.destroyAllWindows()
