#!/usr/bin/python

import sys
sys.path.append( "libs/" )
sys.path.append( "lidar/" )
sys.path.append( "camera/" )
sys.path.append( "wifi/" )


import cv2
from threading import *
import easygui as eg
from identify_device_on_ttyport import *
#from video_consume import *
from video_publish import *
from wifi_publish import *
import time

ROBOT_IP = 'localhost'
Camera1 = None
#Cam1 = None

if __name__== "__main__":

	publish_video(0, 320, 240)
	wifi = WiFi_Scanner()

	

	while True:
		time.sleep(1)

