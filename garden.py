#!/usr/bin/env python

import datetime
import time
import serial
import MySQLdb
from arduino import Arduino
from device import Device
from schedule import Schedule
from condition import Condition
from sensor import Sensor
from sensor_record import SensorRecord

def daemonize():
	import os, sys

	if os.fork() > 0:
	    os._exit(0)

	sys.stdin = open("/dev/null", "r")
	sys.stdout = open("/dev/null", "w")
	sys.stderr = open("/var/log/bookshelfgarden/error.log", "w")

def printToFile(f,str):
	now = datetime.datetime.now()
	print now.strftime("%Y-%m-%d %H:%M")+": "+str
	l = open(f,'a')
	l.write(now.strftime("%Y-%m-%d %H:%M")+": "+str + '\n')
	l.close()

def fetchDevices():
	cur.execute("SELECT id FROM devices;")
	res = []
	i = 0
	results = cur.fetchall()
	for row in results:
		res.append(Device(row[0], cur));
		i = i + 1
	return res

def fetchSchedules():
	cur.execute("SELECT id FROM schedules;")
	res = []
	i = 0
	results = cur.fetchall()
	for row in results:
		res.append(Schedule(row[0], cur));
		i = i + 1
	return res

def fetchConditions():
	cur.execute("SELECT id FROM conditions;")
	res = []
	i = 0
	results = cur.fetchall()
	for row in results:
		res.append(Condition(row[0], cur));
		i = i + 1
	return res

def fetchSensors():
	cur.execute("SELECT id FROM sensors;")
	res = []
	i = 0
	results = cur.fetchall()
	for row in results:
		res.append(Sensor(row[0], cur));
		i = i + 1
	return res

def checkSchedulesAndConditions():#Check devices to change states
	for device in devices:
		s_on = False
		c_on = False
		hasCondition = False
		hasSchedule = False
		for condition in conditions:
			if(device.id == condition.device_id):
				hasCondition = True
				if(condition.check()):
					c_on = True
		for schedule in schedules:
			if(device.id == schedule.device_id):
				hasSchedule = True
				if(schedule.checkTime()):
					s_on = True
					break;

		hasCondition = not hasCondition
		hasSchedule = not hasSchedule

		on = (s_on or hasSchedule) and (c_on or hasCondition);

		if(device.state != on):
			# print 'Device', device.id, 'is', on
			device.toggle(cur)
			

def checkConditions():#Check devices to change states
	for device in devices:
		on = False
		for schedule in schedules:
			if(device.id == schedule.device_id):
				if(schedule.checkTime()):
					on = True
					break;
		if(device.state != on):
			device.toggle(cur)

def sendStates():
	#attach arduino to each device
	#print 'Attaching'
	for device in devices:
		device.sendState()

def attach():
	#attach arduino to each device
	#print 'Attaching'
	for device in devices:
		device.arduino = arduino
		for condition in conditions:
			if condition.device_id == device.id:
				condition.device = device
				#print 'Attached device to condition'
		for schedule in schedules:
			if schedule.device_id == device.id:
				schedule.device = device
				#print 'Attached device to schedule'

	for condition in conditions:
		for sensor in sensors:
			if(condition.sensor_id == sensor.id):
				condition.sensor = sensor
				#print 'Attached sensor1 to condition'
			if(condition.comp_sensor_id == sensor.id):
				condition.comp_sensor = sensor
				#print 'Attached sensor2 to condition'

def checkTime():
	ans = False
	now = datetime.datetime.now()
	# printToFile(logFile,str(now.hour) +', '+ str(hours[0]) +', '+ str(hours[1]))
	
	for (s, e) in hours:
		# printToFile(logFile,str(s) +', '+ str(e))
		if (now.hour >= s and now.hour < e):
		# if (now.minute % 2):
			ans = True 
		
	# printToFile(logFile, str(ans))
	return ans



daemonize()

logFile = '/var/log/bookshelfgarden/log.log' #+now.strftime("%Y-%m-%dT%H.%M")+'.log'

l = open(logFile,'w')
l.write('')
l.close()

sleeptime = 5

printToFile(logFile,'Starting Bookshelf')

#arduino
#arduino = Arduino('/dev/ttyACM0')
time.sleep(2)
printToFile(logFile,'Success Connecting to arduino')

#mysql
db = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="joshua22",db="garden")
cur = db.cursor()
printToFile(logFile,'Success Connecting to MySQL Database')

loopcount = 0
while True:
	loopcount+=1
	print"-------------------- Loop",loopcount,"--------------------"
	#fetch things
	devices = fetchDevices()
	schedules = fetchSchedules()
	conditions = fetchConditions()
	sensors = fetchSensors()

	#attach things
	attach()

	#if this is the first loop send defaults to the arduino
	if loopcount == 1:
		sendStates()
		arduino.ser.flush()

	#ever 15 minutes update the sensor records table
	if loopcount % (15*60) == 0:
		for sensor in sensors:
			sr = SensorRecord(cur,sensor.id,sensor.type,sensor.value)
	        sr.saveNew(['sensor_id','type','value','created_at','updated_at'])

	#check arduino messages
	while arduino.inWaiting() and loopcount > 0:
		msg = arduino.readline().replace('\r','').replace('\n','').split('|');
		if(msg[0] == '!0'):
			print 'Regular MSG'
		elif(msg[0] == '!1'):#Temperature MSG
			print msg
			pin = msg[1]
			temperature = msg[2]
			for sensor in sensors:
				if sensor.pin == int(pin) and sensor.type == "temperature":
					sensor.value = float(temperature)
					sensor.save();
		elif(msg[0] == '!2'):#Humidity MSG
			print msg
			pin = msg[1]
			humidity = msg[2]
			for sensor in sensors:
				if sensor.pin == int(pin) and sensor.type == "humidity":
					sensor.value = float(humidity)
					sensor.save();
		elif(msg[0][:1] == '!'):
			print 'Unknown MSG ID', msg[0], msg[1:]
		else:
			print msg

		#printToFile(logFile,'Message from Arduino:"'++'"')

	#check schedule times
	checkSchedulesAndConditions()
	db.commit()
	time.sleep(sleeptime)


# Grow lights can only be on for 12 hours
# if its within schedule check conditions
#
#




# 	try:
# 		while arduino.inWaiting():
# 			printToFile(logFile,'Message from Arduino:"'+arduino.readline()+'"')

# 		timeIsOk = checkTime()
# 		if (timeIsOk != prevtimeIsOk): 
# 			printToFile(logFile,'timeIsOk changed to '+str(timeIsOk))
# 			prevtimeIsOk = timeIsOk
# 			printToFile(logFile,'Sending to Arduino: '+str(int(timeIsOk)))
# 			arduino.write(str(int(timeIsOk)))

# 		time.sleep(sleeptime)
# 	except IOError: #serial.serialutil.SerialException, 
# 		ser.close()
# 		printToFile(logFile,'Lost connection to /dev/ttyACM'+str(_id))
# 		printToFile(logFile,'Retrying...')
# 		while True:
# 			try:
# 				ser = serial.Serial('/dev/ttyACM'+str(_id), 9600)
# 			except serial.serialutil.SerialException:
# 				_id = _id + 1;
# 				if(_id >= 10):
# 					_id = 0
# 					time.sleep(2)
# 			else:
# 				printToFile(logFile,'Connected to /dev/ttyACM'+str(_id))
# 				prevtimeIsOk = prevtimeIsOk = -10
# 				printToFile(logFile,'Sleeping for 2 seconds...')
# 				time.sleep(2)
# 				printToFile(logFile,'Ready!')
# 				break;
# 	# except IOError:
# 	# 	# ser.close()
# 	# 	printToFile(logFile,'I got an IOERROR')
	



# # def readBuffer():
# # 	while ser.inWaiting():
# # 		msgId = ser.readline()
# # 		if(msgId[:1] == 'i'):
# # 			sensor = ser.readline()
# # 			val = ser.readline()
# # 			print msgId, sensor, val

# # 			now = datetime.datetime.now()
# # 			t = now.strftime("%Y-%m-%dT%H:%M:%S")

# # 			# cur.execute("INSERT INTO sensors (time, sensor, value) VALUES (%s,%s,%s)",(t, sensor, val))
# # 			# db.commit() 
		
# # 		else:
# # 			print 'idk '+msgId
# # 			# print 'checking the time'
# # 			# now = datetime.datetime.now()
# # 			# if(now.minute % 2 == 0):
# # 			# 	ser.write('1')
# # 			# else:
# # 			# 	ser.write('0')
