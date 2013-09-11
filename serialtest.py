import serial
import time

ser = serial.Serial('ttyUSB0'. 38400, timeout = 1)

ser.write("01 0D \r")

speed_hex = ser.readline().split(' ')
speed = float(int('0x'+speed_hex[3], 0))
print 'Speed: ', speed, 'km/h'