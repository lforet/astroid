#!/usr/bin/python

import sys
sys.path.append( "libs/" )
sys.path.append( "lidar/" )
sys.path.append( "camera/" )
sys.path.append( "wifi/" )

import cv, cv2
from threading import *
import easygui as eg
from video_consume import *
from video_publish import *
from wifi_consume import *
import time
import matplotlib.pyplot as plt
from matplotlib import mpl
from wifi_graph import *
from img_processing_tools import *

ROBOT_IP = '192.168.1.190'
Camera1 = None
#Cam1 = None

def snap_shot(img, filename):
	"""grabs a frame from camera feed"""
	#capture from camera at location 0
	#now = time.time()
	#global webcam1
	try:
		#have to capture a few frames as it buffers a few frames..
		#for i in range (5):
			#ret, img = webcam1.read()		 
		#print "time to capture 5 frames:", (time.time()) - now
		cv2.imwrite(filename, img)
		#img1 = Image.open(filename)
		#img1.thumbnail((320,240))
		#img1.save(filename)
		#print (time.time()) - now
	except:
		print "could not save frame from video feed"
	return 


class display_video(Thread):
	def __init__(self, Robot_IP):
		self.frame = None
		self.camera = None
		self.IP = Robot_IP
		Thread.__init__(self)

	def run(self):
		#cv2.namedWindow('Video', cv.CV_WINDOW_AUTOSIZE)
		#cv.NamedWindow("Video")
		self.camera = consume_video('video.0', self.IP)
		#sys.exit()
		while True:
			#time.sleep(0.1)
			try:
				#print "receiving video feed data: ", len(self.camera.frame)
				cv2.imshow('Video', self.camera.frame)
				cv.WaitKey(10)
			except:
				print "no video feed"
				time.sleep(.5)
				pass

if __name__== "__main__":

	wifi = consume_wifi('wifi.1', ROBOT_IP)
	
	cv2.namedWindow('Video', cv.CV_WINDOW_AUTOSIZE)
	
	wifi = consume_wifi('wifi.1', '192.168.1.190')
	graph_wifi  = wifi_graph(wifi)
			
	reply =""
	eg.rootWindowPosition = "+60+375"
	
	while True:

		if reply == "SnapShot":
			snap_shot(Camera1.camera.frame, 'temp.png')	

		if reply == "Enable Video":
			if Camera1 == None:
				Camera1 = display_video(ROBOT_IP)
				print Camera1
				Camera1.daemon= True
				Camera1.start()
			else:
				print Camera1.frame

		if reply == "Quit":
			#print "stopping mobot..."
			##motor.forward(0)
			#time.sleep(.1)
			#del mobot_disp	
			#motor.terminate()
			#sonar.terminate()
			print "Quitting...."
			sys.exit(-1)
		
		if Camera1 == None:
			reply =	eg.buttonbox(title='ASTROID Basestation', image='temp.png', choices=('Enable Video', 'Quit'), root=None)
		else:
			reply =	eg.buttonbox(title='ASTROID Basestation', image='temp.png', choices=('SnapShot', 'Quit'), root=None)


