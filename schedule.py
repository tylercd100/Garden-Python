#!/usr/bin/env python
import datetime
from model import Model

class Schedule(Model):
	def __init__(self, id, cur):
		self.id = id
		self.cur = cur
		self.table = 'schedules'

		self.fetch()

	def createStart(self,add):
		now = datetime.datetime.now()# + datetime.timedelta(1);
		self.start = datetime.datetime(now.year,now.month,now.day, self.hour) + datetime.timedelta(add);

		if(self.day > 0):
			#do something about specific days of the week
			# print 'Setting up for specific day of the week'
			a = 0
			target = self.day;
			current = self.start.isoweekday()

			while(target != current):
				self.start = self.start + datetime.timedelta(1)
				current = self.start.isoweekday()
				a = a + 1;

			# print 'Added', a, 'days to get from', now.isoweekday(), 'to', self.day

	def createEnd(self,add):
		self.end = self.start + datetime.timedelta(0,self.duration)

	def checkTime(self):
		now = datetime.datetime.now()
		if not hasattr(self, 'end'):
			self.createStart(0)
			self.createEnd(0)

		if(now > self.end):
			self.createStart(1)
			self.createEnd(1)

		if(now < self.start):
			return False
		elif(now < self.end):
			return True
		else:
			return False
		
		