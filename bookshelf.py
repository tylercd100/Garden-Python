import datetime
import time
import serial
import MySQLdb

hours = 7, 21
sleeptime = 1

# print
# print "Current date and time using str method of datetime object:"
# print str(now)

# print
# print "Current date and time using instance attributes:"
# print "Current year: %d" % now.year
# print "Current month: %d" % now.month
# print "Current day: %d" % now.day
# print "Current hour: %d" % now.hour
# print "Current minute: %d" % now.minute
# print "Current second: %d" % now.second
# print "Current microsecond: %d" % now.microsecond

# print
# print "Current date and time using strftime:"
# print now.strftime("%Y-%m-%d %H:%M")

ser = serial.Serial('/dev/ttyACM0', 9600)
# db = MySQLdb.connect(host="localhost", # your host, usually localhost
#                      user="root", # your username
#                       passwd="joshua22", # your password
#                       db="garden") # name of the data base

# cur = db.cursor()
count = 0;

def checkTime():
	ans = False
	now = datetime.datetime.now()
	# print now.hour, now.minute, now.second
	if (now.hour >= hours[0] and now.hour < hours[1]):
		ans = True 
	return ans

while True:
	timeIsOk = checkTime()
	# print int(timeIsOk)
	count+=1
	ser.write(str(int(timeIsOk)))
	while ser.inWaiting():
		ser.readline()
	time.sleep(sleeptime)





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