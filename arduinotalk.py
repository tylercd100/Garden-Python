import serial
from time import sleep
import RPi.GPIO as GPIO
import math

outputPins = [13,15,16]
cursor = 0;

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

for pin in outputPins:
	GPIO.setup(pin, GPIO.OUT)

GPIO.setup(11, GPIO.IN)
GPIO.setup(12, GPIO.IN)

sleeptime = 0.05

ser = serial.Serial('/dev/ttyACM0', 9600)

while 1:
	msg = ser.readline()
	if(len(msg) > 0):
		print msg
		GPIO.output(outputPins[cursor], True)
		cursor = cursor + 1
		if(cursor >= len(outputPins)):
			cursor = 0
		GPIO.output(outputPins[cursor], False)
		ser.write(str(cursor+1))
	