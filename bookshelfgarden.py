#!/usr/bin/env python

def daemonize():
	import os, sys

	if os.fork() > 0:
	    os._exit(0)
	# os.setsid()
	sys.stdin.flush()
	sys.stdout.flush()
	sys.stderr.flush()
	null = os.open('/var/log/bookshelfgarden/log.log', os.O_RDWR)
	enull = os.open('/var/log/bookshelfgarden/error.log', os.O_RDWR)
	os.dup2(null, sys.stdin.fileno())
	os.dup2(null, sys.stdout.fileno())
	os.dup2(enull, sys.stderr.fileno())
	os.close(null)
	os.close(enull)

	
	# #os.setsid()

	# sys.stdin = open("/dev/null", "r")
	# sys.stdout = open("/var/log/bookshelfgarden/log.log", "w")
	# sys.stderr = open("/var/log/bookshelfgarden/error.log", "w") 

	# sin = sys.stdin.fileno()
	# sout = sys.stdout.fileno()
	# serr = sys.stderr.fileno()

	# pid = os.fork()
	# if pid != 0:
	# 	os._exit(0)

	# sys.stdout = ox.fdopen(sout,'w');
	

import datetime
import time
import serial
import MySQLdb

daemonize()

hours = 7, 23
sleeptime = 5
timeIsOk = False
prevtimeIsOk = False

_id = 0;

print 'Starting Bookshelf'
print 'Connecting...'
while True:
	try:
		ser = serial.Serial('/dev/ttyACM'+str(_id), 9600)
	except serial.serialutil.SerialException:
		_id = _id + 1;
		if(_id >= 10):
			_id = 0
			time.sleep(2)
	else:
		print 'connected to /dev/ttyACM'+str(_id)
		break;

# db = MySQLdb.connect(host="localhost", # your host, usually localhost
#                      user="root", # your username
#                       passwd="joshua22", # your password
#                       db="garden") # name of the data base

# cur = db.cursor()
count = 0;

def checkTime():
	ans = False
	now = datetime.datetime.now()
	if (now.hour >= hours[0] and now.hour < hours[1]):
		ans = True 
	else:
		ans = False

	return ans


while True:
	try:
		while ser.inWaiting():
			ser.flushInput()

		timeIsOk = checkTime()
		if (timeIsOk != prevtimeIsOk): 
			now = datetime.datetime.now()
			print now.strftime("%Y-%m-%d %H:%M")+': timeIsOk changed to '+str(timeIsOk)
			prevtimeIsOk = timeIsOk

		count+=1
		ser.write(str(int(timeIsOk)))
		
		time.sleep(sleeptime)
	except serial.serialutil.SerialException:
		ser.close()
		print 'Lost connection to /dev/ttyACM'+str(_id)
		print 'Retrying...'
		while True:
			try:
				ser = serial.Serial('/dev/ttyACM'+str(_id), 9600)
			except serial.serialutil.SerialException:
				_id = _id + 1;
				if(_id >= 10):
					_id = 0
					time.sleep(2)
			else:
				print 'connected to /dev/ttyACM'+str(_id)
				break;
	



# def readBuffer():
# 	while ser.inWaiting():
# 		msgId = ser.readline()
# 		if(msgId[:1] == 'i'):
# 			sensor = ser.readline()
# 			val = ser.readline()
# 			print msgId, sensor, val

# 			now = datetime.datetime.now()
# 			t = now.strftime("%Y-%m-%dT%H:%M:%S")

# 			# cur.execute("INSERT INTO sensors (time, sensor, value) VALUES (%s,%s,%s)",(t, sensor, val))
# 			# db.commit() 
		
# 		else:
# 			print 'idk '+msgId
# 			# print 'checking the time'
# 			# now = datetime.datetime.now()
# 			# if(now.minute % 2 == 0):
# 			# 	ser.write('1')
# 			# else:
# 			# 	ser.write('0')
