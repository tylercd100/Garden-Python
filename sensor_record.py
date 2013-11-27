#!/usr/bin/env python
from model import Model
import datetime

class SensorRecord(Model):
	def __init__(self, cur, sensor_id, type, value):
		self.cur = cur
		self.sensor_id = sensor_id
		self.type = type
		self.value = value
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.table = 'sensor_records'

