#!/usr/bin/env python

from PIL import Image
import numpy as np
from PIL import ImageStat
import mahotas
import numpy as np
import cv
import matplotlib.pyplot as plt
from multiprocessing import Process
import time
import os

def plot_rgb_histogram(img):
	# RGB Hitogram
	# This script will create a histogram image based on the RGB content of
	# an image. It uses PIL to do most of the donkey work but then we just
	# draw a pretty graph out of it.
	#
	# May 2009,  Scott McDonough, www.scottmcdonough.co.uk
	#

	import Image, ImageDraw

	imagepath = "mZXN_1979"  # The image to build the histogram of


	histHeight = 120            # Height of the histogram
	histWidth = 256             # Width of the histogram
	multiplerValue = 1        # The multiplier value basically increases
		                    # the histogram height so that love values
		                    # are easier to see, this in effect chops off
		                    # the top of the histogram.
	showFstopLines = True       # True/False to hide outline
	fStopLines = 5


	# Colours to be used
	backgroundColor = (51,51,51)    # Background color
	lineColor = (102,102,102)       # Line color of fStop Markers 
	red = (255,60,60)               # Color for the red lines
	green = (51,204,51)             # Color for the green lines
	blue = (0,102,255)              # Color for the blue lines

	##################################################################################


	#img = Image.open(imagepath)
	hist = img.histogram()
	histMax = max(hist)                                    # comon color
	xScale = float((histWidth))/len(hist)                     # xScaling
	yScale = float((histHeight))/histMax     # yScaling 


	im = Image.new("RGBA", ((histWidth*multiplerValue), (histHeight*multiplerValue)), backgroundColor)   
	draw = ImageDraw.Draw(im)

	# Draw Outline is required
	if showFstopLines:    
	    xmarker = histWidth/fStopLines
	    x =0
	    for i in range(1,fStopLines+1):
		draw.line((x, 0, x, histHeight), fill=lineColor)
		x+=xmarker
	    draw.line((histWidth-1, 0, histWidth-1, 200), fill=lineColor)
	    draw.line((0, 0, 0, histHeight), fill=lineColor)

	# Draw the RGB histogram lines
	x=0; c=0;
	for i in hist:
	    if int(i)==0: pass
	    else:
		color = red
		if c>255: color = green
		if c>511: color = blue
		draw.line((x, histHeight, x, histHeight-(i*yScale)), fill=color)        
	    if x>255: x=0
	    else: x+=1
	    c+=1

	# Now save and show the histogram    
	im.save('histogram.png', 'PNG')
	#im.show()
	return im

###########################################################
def image2array(img):
	"""given an image, returns an array. i.e. create array of image using numpy """
	return np.asarray(img)

###########################################################

def array2image(arry):
	"""given an array, returns an image. i.e. create image using numpy array """
	#Create image from array
	return Image.fromarray(arry)

###########################################################

def PILtoCV(PIL_img, channels):
	cv_img = cv.CreateImageHeader(PIL_img.size, cv.IPL_DEPTH_8U, channels)
	cv.SetData(cv_img, PIL_img.tostring())
	return cv_img

###########################################################

def CVtoPIL(img):
	"""converts CV image to PIL image"""
	cv_img = cv.CreateMatHeader(cv.GetSize(img)[1], cv.GetSize(img)[0], cv.CV_8UC1)
	#cv.SetData(cv_img, pil_img.tostring())
	pil_img = Image.fromstring("L", cv.GetSize(img), img.tostring())
	return pil_img
###########################################################
def PIL2array(img):
    return np.array(img.getdata(),
                    np.uint8).reshape(img.size[1], img.size[0], 3)

def array2PIL(arr, size):
    mode = 'RGBA'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)


def CV2array(img):
		return np.asarray(img[:,:])

def array2CV(img):
		return cv.fromarray(img)

###########################################################
def CalcHistogram(img):
	#calc histogram of green band
	bins = np.arange(0,256)
	hist1 = image2array(img)
	H, xedges = np.histogram(np.ravel(hist1), bins=bins, normed=False)
	return H	

def WriteMeterics(image, classID, data_filename):
	
	if len(image.getbands()) == 3:
		#write class data to file
		f_handle = open(data_filename, 'a')
		f_handle.write(str(classID))
		f_handle.write(', ')
		f_handle.close()
		#calculate LBP histogram on raw image
		np_img = np.array(image)
		lbp1 = mahotas.features.lbp(np_img, 1, 8, ignore_zeros=False)
		#print lbp1.ndim, lbp1.size
		print "LBP Histogram: ", lbp1
		print "LBP Length:", len(lbp1)
		f_handle = open(data_filename, 'a')
		for i in range(len(lbp1)):
			f_handle.write(str(lbp1[i]))
			f_handle.write(" ")
		f_handle.write(',')
		f_handle.close()
		print "Image has multiple color bands...Splitting Bands...."
		Red_Band, Green_Band, Blue_Band = image.split()
		print "Calculating Histogram for I3 pixels of image..."
		I3_Histogram = CalcHistogram(Green_Band)

		#gaussian_numbers = normal(size=1000)
		plt.hist(I3_Histogram, bins=32)
		plt.title("I3 Histogram")
		plt.xlabel("Value")
		plt.ylabel("Frequency")
		#plt.show(block=False)
		plt.savefig("out.png")
		plt.clf()
		cv_image = cv.LoadImage("out.png")
		cv.ShowImage("I3 Histogram", cv_image)
		cv.MoveWindow ('I3 Histogram',705 ,50 )
		time.sleep(.1)
		cv.WaitKey(100)
				
		#p = Process(target=plot_graph, args=([I3_Histogram],))
		#p.start()
		#p.join()

		#save I3 Histogram to file in certain format
		print "saving I3 histogram to dictionary..."
		f_handle = open(data_filename, 'a')
		for i in range(len(I3_Histogram)):
			f_handle.write(str(I3_Histogram[i]))
			f_handle.write(" ")
		f_handle.write(',')
		f_handle.close()
		#calculate RGB histogram on raw image
		rgb_histo = image.histogram()
		print "saving RGB histogram to dictionary..."
		f_handle = open(data_filename, 'a')
		for i in range(len(rgb_histo)):
			f_handle.write(str(rgb_histo[i]))
			f_handle.write(" ")
		f_handle.write(',')
		f_handle.close()	
	
		#calculate I3 meterics
		I3_sum =    ImageStat.Stat(image).sum
		I3_sum2 =   ImageStat.Stat(image).sum2
		I3_median = ImageStat.Stat(image).median
		I3_mean =   ImageStat.Stat(image).mean
		I3_var =    ImageStat.Stat(image).var
		I3_stddev = ImageStat.Stat(image).stddev
		I3_rms =    ImageStat.Stat(image).rms
		print "saving I3 meterics to dictionary..."
		f_handle = open(data_filename, 'a')

		print "sum img1_I3: ",    I3_sum[1]
		print "sum2 img1_I3: ",   I3_sum2[1]
		print "median img1_I3: ", I3_median[1]
		print "avg img1_I3: ",    I3_mean[1]
		print "var img1_I3: ",    I3_var[1]
		print "stddev img1_I3: ", I3_stddev[1]
		print "rms img1_I3: ",    I3_rms[1]
		#print "extrema img1_I3: ", ImageStat.Stat(img1_I3).extrema
		#print "histogram I3: ", len(img1_I3.histogram())

		f_handle.write(str(I3_sum[1]))
		f_handle.write(",")
		f_handle.write(str(I3_sum2[1]))
		f_handle.write(",")
		f_handle.write(str(I3_median[1]))
		f_handle.write(",")
		f_handle.write(str(I3_mean[1]))
		f_handle.write(",")
		f_handle.write(str(I3_var[1]))
		f_handle.write(",")
		f_handle.write(str(I3_stddev[1]))
		f_handle.write(",")
		f_handle.write(str(I3_rms[1]))
		#f_handle.write(",")
		f_handle.write('\n')
		f_handle.close()
	else:
		print "image not valid for processing: ", filename1
		time.sleep(5)
	return

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

###########################################################

def resize_img(original_img, scale_percentage):
	#print original_img.height, original_img.width, original_img.nChannels
	#resized_img = cv.CreateMat(original_img.rows * scale_percentage , original.cols * scale_percenta, cv.CV_8UC3)
	resized_img = cv.CreateImage((cv.Round(original_img.width * scale_percentage) , cv.Round(original_img.height * scale_percentage)), original_img.depth, original_img.nChannels)
	cv.Resize(original_img, resized_img)
	return(resized_img)
	
###########################################################


