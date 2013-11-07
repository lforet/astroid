#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2, math
import numpy as np
import sys
import colorsys


class ColourTracker:
	def __init__(self, lower_RGB, upper_RGB):
		cv2.namedWindow("ColourTrackerWindow", cv2.CV_WINDOW_AUTOSIZE)
		self.capture = cv2.VideoCapture(0)
		self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320) 
		self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
		self.scale_down = 1
		self.lower_HSV = self.scale_hsv(colorsys.rgb_to_hsv(self.norm(lower_RGB[0]), self.norm(lower_RGB[1]), self.norm(lower_RGB[2])) ) 
		self.upper_HSV = self.scale_hsv(colorsys.rgb_to_hsv(self.norm(upper_RGB[0]), self.norm(upper_RGB[1]), self.norm(upper_RGB[2])) ) 
		print self.lower_HSV , self.upper_HSV
		
	def run(self):
		while True:
			f, orig_img = self.capture.read()
			orig_img = cv2.flip(orig_img, 1)

            #blur the source image to reduce color noise 
            #cv.Smooth(img, img, cv.CV_BLUR, 3);
			img = cv2.GaussianBlur(orig_img, (3,3), 0)

			img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)

			img = cv2.resize(img, (len(orig_img[0]) / self.scale_down, len(orig_img) / self.scale_down))
			color_lower = np.array(self.lower_HSV,np.uint8)
			#color_lower = np.array([0,180,0],np.uint8)
			color_upper = np.array(self.upper_HSV,np.uint8)
			print color_lower, color_upper
			#print self.lower_HSV , self.upper_HSV
			red_binary = cv2.inRange(img, color_lower, color_upper)
 
			#print red_binary 
			dilation = np.ones((15, 15), "uint8")
			red_binary = cv2.dilate(red_binary, dilation)
			contours, hierarchy = cv2.findContours(red_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			max_area = 0
			largest_contour = None
			for idx, contour in enumerate(contours):
				area = cv2.contourArea(contour)
				if area > max_area:
					max_area = area
					largest_contour = contour
			if not largest_contour == None:
				moment = cv2.moments(largest_contour)
				if moment["m00"] > 1000 / self.scale_down:
					rect = cv2.minAreaRect(largest_contour)
					rect = ((rect[0][0] * self.scale_down, rect[0][1] * self.scale_down), (rect[1][0] * self.scale_down, rect[1][1] * self.scale_down), rect[2])
					box = cv2.cv.BoxPoints(rect)
					box = np.int0(box)
					cv2.drawContours(orig_img,[box], 0, (0, 0, 255), 2)
					cv2.imshow("ColourTrackerWindow", orig_img)
					if cv2.waitKey(20) == 27 or cv2.waitKey(20) == 1048603:
						cv2.destroyWindow("ColourTrackerWindow")
						self.capture.release()
						break

	def norm(self, x):
		return (x/255.0)

	def scale_hsv(self, hsv):
		return ([(hsv[0]*180),(hsv[1]*255),(hsv[2]*255)])

def norm( x):
	return (x/255.0)

def scale_hsv( hsv):
	return ([(hsv[0]*180),(hsv[1]*255),(hsv[2]*255)])
if __name__ == "__main__":

	upper_RGB = [50,140,120]
	print scale_hsv(colorsys.rgb_to_hsv(norm(upper_RGB[0]), norm(upper_RGB[1]), norm(upper_RGB[2])) ) 
	upper_RGB = [0,255,0]
	print scale_hsv(colorsys.rgb_to_hsv(norm(upper_RGB[0]), norm(upper_RGB[1]), norm(upper_RGB[2])) ) 
	
	sys.exit()

	colour_tracker = ColourTracker([50,140,120], [60,180,130])
	colour_tracker.run()


