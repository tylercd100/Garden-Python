#!/usr/bin/env python

class Device:
	def __init__(self, id, pin, state, max_on):
		self.id = id
		self.pin = pin
		self.state = state
		self.max_on = max_on

	def toggle(self,cur):
		self.state = -self.state + 1
		cur.execute("UPDATE devices SET state = '%d' WHERE id = '%s'" % (self.state,self.id))
		self.sendState();
		print 'Device '+str(self.id)+' changed state to '+str(self.state)

	def sendState(self):
		self.arduino.send(self.pin,self.state);
		