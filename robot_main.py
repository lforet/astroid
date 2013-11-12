#!/usr/bin/python

import sys
sys.path.append( "libs/" )
sys.path.append( "lidar/" )
sys.path.append( "video/" )
sys.path.append( "wifi/" )


import cv2
import thread
#import easygui as eg
from identify_device_on_ttyport import *
#from video_consume import *
import video_publish
import wifi_publish
#from wifi_consume import *
import protox2d_publish 


import time

ROBOT_IP = 'localhost'
Camera1 = None
#Cam1 = None

if __name__== "__main__":

	#publish video from camera on /dev/ttyUSB0
	video_publish.publish_video(0, 320, 240)

	#pulish wifi signal strength
	wifi = wifi_publish.WiFi_Scanner('isotope11_wireless')

	#publish LIDAR
	lidar = protox2d_publish.protox2d('A1')
	while True:
		#time.sleep(3)
		data = lidar.read_lidar()
		print data, len(data)	


	while True:
		time.sleep(1)

