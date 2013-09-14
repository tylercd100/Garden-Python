import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

while 1:
	msg = ser.readline()
	if(len(msg) > 0):
		print msg
		ser.write('5')
	