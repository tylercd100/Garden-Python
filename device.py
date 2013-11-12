#!/usr/bin/env python
from model import Model

class Device(Model):
	def __init__(self, id, cur):
		self.id = id
		self.cur = cur
		self.table = 'devices'

		self.fetch()

	def toggle(self,cur):
		if(self.state == -1 or self.state == 0):
			self.state = 1
		else:
			self.state = 0
		cur.execute("UPDATE devices SET state = '%d' WHERE id = '%s'" % (self.state,self.id))
		self.sendState();
		print 'Device '+str(self.id)+' changed state to '+str(self.state)

	def sendState(self):
		#print 'Sending to arduino',self.pin,self.state
		if hasattr(self, 'arduino'):
			self.arduino.send(self.pin,self.state);
		