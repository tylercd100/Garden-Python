#!/usr/bin/env python
import datetime

class Schedule:
	def __init__(self, id, device_id, minute, hour, day, duration):
		self.id = id
		self.device_id = device_id
		self.minute = minute
		self.hour = hour
		self.day = day
		self.duration = duration

		self.createStart(0)
		self.createEnd(0)

	def createStart(self,add):
		now = datetime.datetime.now()
		if(self.day > 0):
			#do something about specific days of the week
			day = now.day + add
		else:
			day = now.day + add
		nowweekday = now.isoweekday()
		self.start = datetime.datetime(now.year,now.month,day, self.hour)

	def createEnd(self,add):
		dur = datetime.timedelta(0,self.duration);
		self.end = self.start + dur;

	def checkTime(self):
		now = datetime.datetime.now()
		if(now > self.end):
			self.createStart(1)
			self.createEnd(1)

		if(now < self.start):
			return False
		elif(now < self.end):
			return True
		else:
			return False
		
		