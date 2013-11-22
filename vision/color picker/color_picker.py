#!/usr/bin/env python
# -*- coding: utf-8 -*-
# returns HSV value of the pixel under the cursor in a video stream
# author: achuwilson
# achuwilson.wordpress.com
import cv
import time
x_co = 0
y_co = 0


def on_mouse(event,x,y,flag,param):
	global x_co
	global y_co
	global dst
	if (event==cv.CV_EVENT_LBUTTONDOWN): # here event is left mouse button double-clicked
		print x,y
		hsv = cv.CreateImage(cv.GetSize(dst), 8, 3)
		#thr = cv.CreateImage(cv.GetSize(dst), 8, 1)
		cv.CvtColor(dst, hsv, cv.CV_BGR2HSV)
		hsv_color = cv.Get2D(hsv,y,x)
		rgb_color = cv.Get2D(dst,y,x)
		print "H:",hsv_color[0],"      S:",hsv_color[1],"       V:",hsv_color[2]
		print "R:",rgb_color[2],"      B:",rgb_color[0],"       G:",rgb_color[1]


cv.NamedWindow("camera", 1)
capture = cv.CaptureFromCAM(0)
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8)
#src = cv.QueryFrame(capture)
src = cv.LoadImage('object_to_track.jpg')
cv.Smooth(src, src, cv.CV_BLUR, 3)
dst = cv.CreateImage((640, 480), 8, 3)
cv.Resize(src,  dst) 
cv.SetMouseCallback("camera",on_mouse, dst);
cv.ShowImage("camera", dst)
while True:
	src = cv.QueryFrame(capture)
	dst = cv.CreateImage((640, 480), 8, 3)
	cv.Resize(src,  dst) 
	cv.Smooth(dst, dst, cv.CV_BLUR, 3)

	cv.SetMouseCallback("camera",on_mouse, src);
	cv.ShowImage("camera", src)


	#cv.PutText(src,str(s[0])+","+str(s[1])+","+str(s[2]), (x_co,y_co),font, (55,25,255))

	if cv.WaitKey(10) == 27:
		break




