from time import sleep
import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(11, GPIO.IN)
GPIO.setup(12, GPIO.IN)
sleeptime = 0.05
while 1:
     if GPIO.input(11):
          sleeptime = sleeptime + 0.01
     if GPIO.input(12):
          sleeptime = sleeptime - 0.01
          
     GPIO.output(13, False)
     sleep(sleeptime)
     GPIO.output(13, True)
     sleep(sleeptime)

     GPIO.output(15, False)
     sleep(sleeptime)
     GPIO.output(15, True)
     sleep(sleeptime)

     GPIO.output(16, False)
     sleep(sleeptime)
     GPIO.output(16, True)
     sleep(sleeptime)

	 
