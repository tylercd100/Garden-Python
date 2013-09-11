import serial
import time

ser = serial.Serial('ttyUSB0'. 38400, timeout = 1)
sleeptime = 1

while true
	ser.write("01 0C \r")

	speed_hex = ser.readline().split(' ')
	speed = float(int('0x'+speed_hex[3], 0))
	print 'RPM: ', speed, ''
	time.sleep(sleeptime)