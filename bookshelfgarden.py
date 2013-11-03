#!/usr/bin/env python

import datetime
import time
import serial
import MySQLdb
from arduino import Arduino
from device import Device
from schedule import Schedule

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
	cur.execute("SELECT id, pin, state, max_on FROM devices;")
	res = []
	i = 0
	results = cur.fetchall()
	for row in results:
		res.append(Device(row[0],row[1],row[2],row[3]));
		i = i + 1
	return res

def fetchSchedules():
	cur.execute("SELECT id, device_id, minute, hour, day, duration FROM schedules;")
	res = []
	i = 0
	results = cur.fetchall()
	for row in results:
		res.append(Schedule(row[0],row[1],row[2],row[3],row[4],row[5]));
		i = i + 1
	return res

def checkSchedules():#Check devices to change states
	for device in devices:
		on = False
		for schedule in schedules:
			if(device.id == schedule.device_id):
				if(schedule.checkTime()):
					on = True
					break;
		if(device.state != on):
			device.toggle(cur)

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
arduino = Arduino('/dev/ttyACM0')
time.sleep(2)
printToFile(logFile,'Success Connecting to arduino')

#mysql
db = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="joshua22",db="garden")
cur = db.cursor()
printToFile(logFile,'Success Connecting to MySQL Database')

#fetch things
devices = fetchDevices()
schedules = fetchSchedules()

#attach arduino to each device
for device in devices:
	device.arduino = arduino
	device.sendState()
	time.sleep(0.05)

loopcount = 0
while True:
	loopcount+=1
	# print '------------------------ Loop '+str(loopcount)+' ------------------------'

	#check for messages from the arduino
	while arduino.inWaiting():
		printToFile(logFile,'Message from Arduino:"'+arduino.readline()+'"')

	#fetch things
	devices = fetchDevices()
	schedules = fetchSchedules()

	#attach arduino to each device
	for device in devices:
		device.arduino = arduino

	#check schedule times
	checkSchedules()
	db.commit()
	time.sleep(sleeptime)




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
