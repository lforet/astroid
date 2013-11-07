#!/usr/bin/python
"""

SUMMARY:
	This library gets wifi signal strength to a given SSID and publishes to rabbitmq channel. 
	
	Call with the name of wifi SSID.
	
	publishes signal strength in form of a string 0-3 characters.	

EXAMPLE USAGE:
	wlist = WiFi_Scanner('isotope11_wireless')
"""

import dbus
import time
import thread
import pika

class WiFi_Scanner():
	def __init__(self, ssid):
		self.NM = 'org.freedesktop.NetworkManager'
		self.has_nm = True
		self.strength = None
		self.ssid = ssid
		self.aps = []
		try:
			self.bus = dbus.SystemBus()
			nm = self.bus.get_object(self.NM, '/org/freedesktop/NetworkManager')
			self.devlist = nm.GetDevices(dbus_interface = self.NM)	
			#-------------connection variables
			self.channel_name = 'wifi.1'
			self.connection = None
			self.channel = None
			#----------------------RUN
			self.run()	  
		except:
			self.has_nm = False	

		
	
	def dbus_get_property(self, prop, member, proxy):
		return proxy.Get(self.NM+'.' + member, prop, dbus_interface = 'org.freedesktop.DBus.Properties')

	def repopulate_ap_list(self):
		apl = []
		res = []
		for i in self.devlist:
		    tmp = self.bus.get_object(self.NM, i)
		    if self.dbus_get_property('DeviceType', 'Device', tmp) == 2:
		        apl.append(self.bus.get_object(self.NM, i).GetAccessPoints(dbus_interface = self.NM+'.Device.Wireless'))
		for i in apl:
		    for j in i:
		        res.append(self.bus.get_object(self.NM, j))
		return res

	def update(self):
		self.aps = []
		if self.has_nm:
			for i in self.repopulate_ap_list():
				try:
					ssid = self.dbus_get_property('Ssid', 'AccessPoint', i)
					ssid = "".join(["%s" % k for k in ssid])
					ss = self.dbus_get_property('Strength', 'AccessPoint', i);
					mac = self.dbus_get_property('HwAddress', 'AccessPoint', i);
					#self.aps.append({"mac":str(mac), "ssid": unicode(ssid), "ss": float(ss)})
					self.aps.append([str(unicode(ssid)), int(ss)])
				except:
					pass
	
	def signal_strength(self):
			to_return = -1
			self.update()
			#filter(lambda x: 'abc' in x,lst)
			for i in self.aps:
				if i[0] == self.ssid: 
					to_return = i[1]
			self.publish(str(to_return))
			self.strength = to_return
			print to_return
			#return to_return
	
	def loop(self):
		while True:
			self.signal_strength()
			time.sleep(.1)
	
	def run(self):
		self.connect()
		print self.ssid
		self.th = thread.start_new_thread(self.loop, ())

	def connect(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange='astroid_data_feed',type='topic')	
		#self.channel.queue_declare(queue='mobot_wifi', auto_delete=True, arguments={'x-message-ttl':100})
		#self.channel.queue_bind(queue='mobot_wifi', exchange='mobot_data_feed', auto_delete=True, arguments={'x-message-ttl':1000})
	
	def publish(self, data):
			self.channel.basic_publish(exchange='astroid_data_feed', routing_key=self.channel_name,  body=data, properties=pika.BasicProperties(expiration=str(1000)))


if __name__ == "__main__":
	wlist = WiFi_Scanner('isotope11_wireless')
	i = 0
	while True:
		time.sleep(.1)
		#print wlist.strength, i
		#i += 1
	
	
