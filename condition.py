#!/usr/bin/env python
from model import Model

class Condition(Model):
	def __init__(self, id, cur):
		self.id = id
		self.cur = cur
		self.table = 'conditions'

		self.fetch()

	def check(self):
		result = False
		if(self.type == 'value'):
			if hasattr(self, 'sensor'):
				val1 = self.sensor.value
				val2 = self.value
		if(self.type == 'sensor'):
			if hasattr(self, 'sensor') and hasattr(self, 'comp_sensor'):
				val1 = self.sensor.value
				val2 = self.comp_sensor.value

		if 'val1' in locals():
			if self.operator == '<':
				if(val1 < val2):
					result = True
			elif self.operator == '==':
				if(val1 == val2):
					result = True
			elif self.operator == '>':
				if(val1 > val2):
					result = True

		# print 'Condition', self.id, result
		return result
		
		