#!/usr/bin/env python
from model import Model

class Sensor(Model):
	def __init__(self, id, cur):
		self.id = id
		self.cur = cur
		self.table = 'sensors'

		self.fetch()