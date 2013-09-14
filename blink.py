from time import sleep
import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(0, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
while 1:
     GPIO.output(0, False)
     sleep(1)
     GPIO.output(0, True)
     sleep(1)

     GPIO.output(3, False)
     sleep(1)
     GPIO.output(3, True)
     sleep(1)

     GPIO.output(4, False)
     sleep(1)
     GPIO.output(4, True)
     sleep(1)

	 
