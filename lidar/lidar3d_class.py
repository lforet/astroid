#!/usr/bin/python


import thread, time, sys, traceback
import serial
from math import *

class mobot_lidar3d ():
	def __init__(self, com_port, baudrate, resolution):
		# serial port
		self.com_port = com_port
		self.baudrate = baudrate
		self.ser = serial.Serial(self.com_port, self.baudrate)
		#self.data = []
		self.x_degree = 0
		self.y_degree = 0
		self.dist = 0
		self.quality = 0
		self.rpm = 0
		self.resolution = resolution
		self.clockwise = True
		#self.th = thread.start_new_thread(self.run, ())
	
	def run(self):
		while True:
			if (self.ser.isOpen() == False):
				self.ser = serial.Serial(self.com_port, self.baudrate)
		#		print "reconnecting serial port", self.com_port, self.baudrate
				#self.ser = serial.Serial(self.com_port, self.baudrate)
		#		print self.ser
			#time.sleep(.000001)
			#self.read_lidar()
			
	def read_lidar(self):
			#print "reading lidar"
			data = []
			self.x_degree = 0
			self.y_degree = 0
			self.dist = 0
			try:
				temp_data = self.ser.readline()
				temp_data = temp_data.strip('\r\n')
				data = temp_data.split(',')
				return data
				#return dist_data
			except :
				#time.sleep(3)
				#del self.ser
				#print "reconnecting serial port", self.com_port, self.baudrate
				#self.ser = serial.Serial(self.com_port, self.baudrate)
				traceback.print_exc(file=sys.stdout)
		#self.y_degree += self.resolution
		#if self.y_degree > 360:
		#	self.y_degree = 0
		#	if self.clockwise == True:
		#		self.x_degree += self.resolution
		#	else:
		#		self.x_degree -= self.resolution
		#	if self.x_degree > 180:
		#		self.clockwise = False
		#	if self.x_degree < 0:
		#		self.clockwise = True
	
		#self.dist = random.randint(950,1000)
		#self.dist = 1000
		#self.quality = random.randint(0,100)
		#self.rpm = random.randint(281 ,295)

		#temp_data = []
		#while len(temp_data) < 360:	
			#print temp_data, i
			#raw_input("enter")
		#if len (temp_data ) == 360: self.data = sorted(temp_data)

    
