#!/usr/bin/env python
import serial
import time

class Arduino:
	def __init__(self,port):
		self.connect(port)
		self.ser.flushInput()
		self.ser.flushOutput()

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
		self.write(str(pin)+','+str(value)+'|');
		time.sleep(0.1)

		
