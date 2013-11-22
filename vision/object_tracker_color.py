#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  cv, cv2, math
import numpy as np


class ColourTracker:
	def __init__(self):
		cv2.namedWindow("ColorTrackerWindow" , cv2.CV_WINDOW_AUTOSIZE)
		cv2.namedWindow("threshold")
		self.capture = cv2.VideoCapture(0)
		#self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320) 
		#self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
		self.scale_down = 1
		self.sensitivity = 500
		self.frame = None
		self.hsv = None
		self.hue_high = 91
		self.hue_low = 90
		self.sat_high = 126
		self.sat_low = 125
		self.val_high = 126
		self.val_low = 125	
		self.lower_HSV = np.array([self.hue_low, self.sat_low, self.val_low])
		self.upper_HSV = np.array([self.hue_high, self.sat_high, self.val_high])
		print self.lower_HSV , self.upper_HSV

	def on_mouse(self, event,x,y,flag,param):
		if (event==cv.CV_EVENT_LBUTTONDOWN): 
			print x,y
			hsv_color = self.hsv[y][x]
			rgb_color = self.frame[y][x]
			print "H:",hsv_color[0],"      S:",hsv_color[1],"       V:",hsv_color[2]
			print "R:",rgb_color[2],"      B:",rgb_color[0],"       G:",rgb_color[1]
			if hsv_color[0] > self.hue_high: self.hue_high = hsv_color[0] 
			if hsv_color[0] < self.hue_low: self.hue_low = hsv_color[0] 
			if hsv_color[1] > self.sat_high: self.sat_high = hsv_color[1]
			if hsv_color[1] < self.sat_low: self.sat_low = hsv_color[1]
			if hsv_color[2] > self.val_high: self.val_high = hsv_color[2]
			if hsv_color[2] < self.val_low: self.val_low = hsv_color[2]
			self.lower_HSV = np.array([self.hue_low, self.sat_low, self.val_low], np.uint8)
			self.upper_HSV = np.array([self.hue_high, self.sat_high, self.val_high],np.uint8)
			print self.lower_HSV, self.upper_HSV

		if (event==cv.CV_EVENT_MBUTTONDOWN):
			#on middle mouse button reset all values
			print "resetting values"
			self.hue_high = 91
			self.hue_low = 90
			self.sat_high = 126
			self.sat_low = 125
			self.val_high = 126
			self.val_low = 125
			print self.lower_HSV , self.upper_HSV
			self.lower_HSV = np.array([self.hue_low, self.sat_low, self.val_low])
			self.upper_HSV = np.array([self.hue_high, self.sat_high, self.val_high])


	def run(self):
		cv.SetMouseCallback("ColorTrackerWindow",self.on_mouse);
		while True:
			f, self.frame = self.capture.read()
			
			#flip image to give correct prospective
			self.frame = cv2.flip(self.frame, 1)

			#scale
			cv2.resize(self.frame, (len(self.frame[0]) / self.scale_down, len(self.frame) / self.scale_down))

            #blur the source image to reduce color noise 
   			self.frame = cv2.blur(self.frame,(5,5))
			#self.frame = cv2.GaussianBlur(self.frame, (5,5), 0)

			# convert to hsv and find range of colors
			self.hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)
			#print self.hsv, self.lower_HSV, self.upper_HSV
			thresh = cv2.inRange(self.hsv ,self.lower_HSV , self.upper_HSV )
 
			
			dilation = np.ones((15, 15), "uint8")
			thresh  = cv2.dilate(thresh , dilation)

			# find contours in the threshold image
			#contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

			# finding contour with maximum area and store it as best_cnt
			#max_area = 0
			#best_cnt = 1
			#for cnt in contours:
			#	area = cv2.contourArea(cnt)
			#	if area > max_area:
			#	    max_area = area
			#	    best_cnt = cnt

			# finding centroids of best_cnt and draw a circle there
			#M = cv2.moments(best_cnt)
			#cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
			#cv2.circle(self.frame,(cx,cy),5,255,-1)

			contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			max_area = 0
			largest_contour = None
			for idx, contour in enumerate(contours):
				area = cv2.contourArea(contour)
				if area > max_area:
					max_area = area
					largest_contour = contour

			if not largest_contour == None:
				moment = cv2.moments(largest_contour)
				if moment["m00"] > self.sensitivity / self.scale_down:
					rect = cv2.minAreaRect(largest_contour)
					rect = ((rect[0][0] * self.scale_down, rect[0][1] * self.scale_down), (rect[1][0] * self.scale_down, rect[1][1] * self.scale_down), rect[2])
					box = cv2.cv.BoxPoints(rect)
					box = np.int0(box)
					cv2.drawContours(self.frame,[box], 0, (0, 0, 255), 2)


			cv2.imshow("ColorTrackerWindow", self.frame)
			cv2.imshow("threshold", thresh)
			# Clean up everything before leaving
			if cv2.waitKey(20) == 27 or cv2.waitKey(20) == 1048603:
				cv2.destroyWindow("ColorTrackerWindow")
				self.capture.release()
				break

if __name__ == "__main__":

	colour_tracker = ColourTracker()
	colour_tracker.run()


