from time import sleep
import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
# GPIO.setup(15, GPIO.OUT)
# GPIO.setup(16, GPIO.OUT)
while 1:
     GPIO.output(11, False)
     sleep(1)
     GPIO.output(11, True)
     sleep(1)

     # GPIO.output(15, False)
     # sleep(1)
     # GPIO.output(15, True)
     # sleep(1)

     # GPIO.output(16, False)
     # sleep(1)
     # GPIO.output(16, True)
     # sleep(1)

	 
