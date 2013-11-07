#!/usr/bin/python

import sys
sys.path.append( "libs/" )
sys.path.append( "lidar/" )
sys.path.append( "camera/" )
sys.path.append( "wifi/" )

import cv2
from threading import *
import easygui as eg
from video_consume import *
from video_publish import *
from wifi_consume import *
import time

ROBOT_IP = 'localhost'
Camera1 = None
#Cam1 = None

class display_video(Thread):
	def __init__(self):
		self.frame = None
		Thread.__init__(self)

	def run(self):
		#print "hi"
		#time.sleep(5)
		cv2.namedWindow('Camera1', cv.CV_WINDOW_AUTOSIZE)
		camera = consume_video('video.0', 'localhost')
		while True:
			#time.sleep(0.1)
			try:
				#print "receiving video feed data: ", len(camera.frame)
				self.frame = camera.frame 
				cv2.imshow('Camera1', camera.frame)
				cv.WaitKey(10)
			except:
				print "no video feed"
				time.sleep(0.5)
				pass

if __name__== "__main__":

	video1 = None

	#publish_video(0, 320, 240)

	#Camera1 = display_video()
	#Camera1.daemon= True
	#Camera1.start()

	#wifi = consume_wifi('wifi.1', '192.168.1.180')

	reply =""
	eg.rootWindowPosition = "+60+375"
	while True:

		if reply == "Enable Video":
			
			if Camera1 == None:
				Camera1 = display_video()
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

		reply =	eg.buttonbox(title='ASTROID Basestation', choices=('Enable Video', 'Quit'), root=None)


