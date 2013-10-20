#!/usr/bin/env python

import serial
#'/dev/ttyACM'+str(_id)
class Arduino:
	def __init__(self,port):
		self.connect(port)

	def write(self,data):
		self.ser.write(data);

	def readline(self):
		return self.ser.readline();

	def inWaiting(self):
		return self.ser.inWaiting();

	def connect(self,port):
		self.ser = serial.Serial(port, 9600)

	def send(self,pin,value):
		print 'Sending Ardiuno pin '+str(pin)+' as '+str(value)
		self.write(str(pin)+','+str(value))

		