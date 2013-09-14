import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(11, GPIO.IN)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(12, GPIO.IN)
while 1:
	if GPIO.input(11) and not GPIO.input(12):
		GPIO.output(13, False)
	else:
		GPIO.output(13, True)
		
	if GPIO.input(12) and not GPIO.input(11):
		GPIO.output(15, False)
	else:
		GPIO.output(15, True)