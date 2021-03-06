#!/usr/bin/python

import pika
import thread, time, sys, traceback	


''' USAGE:

	lidar = consume_lidar(channel_name.#, ip_of_publisher)

	EXAMPLE:
		lidar = consume_lidar('lidar.1', 'localhost')

'''

class consume_lidar():
	def __init__(self, channel_name, host_ip):
		self.id = None
		self.rpm = None
		self.data = None
		#-------------connection variables
		self.channel_name = channel_name
		self.host_ip = host_ip
		self.queue_name =  None
		self.connection = None
		self.channel = None
		#----------------------RUN
		self.run()
	
	def connect(self):
		self.connection =  pika.BlockingConnection(pika.ConnectionParameters(host=self.host_ip))
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange='astroid_data_feed',type='topic')	
		result = self.channel.queue_declare(exclusive=True, auto_delete=True, arguments={'x-message-ttl':1000})
		self.queue_name = result.method.queue
		binding_keys = self.channel_name
		self.channel.queue_bind(exchange='astroid_data_feed', queue=self.queue_name, routing_key=binding_keys)

		
	def read_lidar(self):	
		#method_frame = None
		while True:	
			if  self.connection == None or self.connection.is_open == False:
					self.connect()
			time.sleep(0.0001) # do not hog the processor power
			#print "-" * 50
			method_frame, properties, body = self.channel.basic_get(queue=self.queue_name)
			if method_frame:
				# Display the message parts
				print body
				self.channel.basic_ack(method_frame.delivery_tag)
			#else:
			#	print "no msgs read"
			#	time.sleep(.25)

	def run(self):
		self.th = thread.start_new_thread(self.read_lidar, ())
	

if __name__== "__main__":

	lidar = consume_lidar('protox2d.1', 'localhost')
	while True:
		time.sleep(1)
		#print 'signal strength:', wifi.signal_strength

