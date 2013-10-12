#!/usr/bin/env python

def daemonize():
	import os, sys

	if os.fork() > 0:
	    os._exit(0)

	sys.stdin = open("/dev/null", "r")
	sys.stdout = open("/dev/null", "w")
	sys.stderr = open("/dev/null", "w")

def printToFile(f,str):
	now = datetime.datetime.now()
	print now.strftime("%Y-%m-%d %H:%M")+": "+str
	l = open(f,'a')
	l.write(now.strftime("%Y-%m-%d %H:%M")+": "+str + '\n')
	l.close()

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

import datetime
import time
import serial
import MySQLdb

daemonize()

hours = [(7, 11), (11,21)]
sleeptime = 0.2
timeIsOk = True
prevtimeIsOk = True

_id = 0;

now = datetime.datetime.now()

logFile = '/var/log/bookshelfgarden/log.log' #+now.strftime("%Y-%m-%dT%H.%M")+'.log'

l = open(logFile,'w')
l.write('')
l.close()

printToFile(logFile,'Starting Bookshelf')
checkTime()
printToFile(logFile,'Connecting...')

while True:
	try:
		ser = serial.Serial('/dev/ttyACM'+str(_id), 9600)
	except serial.serialutil.SerialException:
		_id = _id + 1;
		if(_id >= 10):
			_id = 0
			time.sleep(2)
	else:
		printToFile(logFile,'Connected to /dev/ttyACM'+str(_id))
		break;

# db = MySQLdb.connect(host="localhost", # your host, usually localhost
#                      user="root", # your username
#                       passwd="joshua22", # your password
#                       db="garden") # name of the data base

# cur = db.cursor()


#send to arduino
# printToFile(logFile,'Sending to Arduino: '+str(int(timeIsOk)))
# ser.write(str(int(timeIsOk)))

printToFile(logFile,'Sleeping for 2 seconds...')
time.sleep(2)
printToFile(logFile,'Ready!')

timeIsOk = checkTime()
prevtimeIsOk = timeIsOk
printToFile(logFile,'Sending to Arduino: '+str(int(timeIsOk)))
ser.write(str(int(timeIsOk)))
time.sleep(sleeptime)

while True:
	try:
		if(ser):
			while ser.inWaiting():
				# ser.flushInput()
				printToFile(logFile,'Message from Arduino:"'+ser.readline()+'"')

		timeIsOk = checkTime()
		if (timeIsOk != prevtimeIsOk): 
			printToFile(logFile,'timeIsOk changed to '+str(timeIsOk))
			prevtimeIsOk = timeIsOk
			printToFile(logFile,'Sending to Arduino: '+str(int(timeIsOk)))
			ser.write(str(int(timeIsOk)))

		time.sleep(sleeptime)
	except IOError: #serial.serialutil.SerialException, 
		ser.close()
		printToFile(logFile,'Lost connection to /dev/ttyACM'+str(_id))
		printToFile(logFile,'Retrying...')
		while True:
			try:
				ser = serial.Serial('/dev/ttyACM'+str(_id), 9600)
			except serial.serialutil.SerialException:
				_id = _id + 1;
				if(_id >= 10):
					_id = 0
					time.sleep(2)
			else:
				printToFile(logFile,'Connected to /dev/ttyACM'+str(_id))
				prevtimeIsOk = prevtimeIsOk = -10
				printToFile(logFile,'Sleeping for 2 seconds...')
				time.sleep(2)
				printToFile(logFile,'Ready!')
				break;
	# except IOError:
	# 	# ser.close()
	# 	printToFile(logFile,'I got an IOERROR')
	



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
