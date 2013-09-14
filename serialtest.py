import serial
import time
import string
import MySQLdb

sleeptime = 0.2;
ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="joshua22", # your password
                      db="obdii") # name of the data base


def interpret_result(code):
    """Internal use only: not a public interface"""
    # Code will be the string returned from the device.
    # It should look something like this:
    # '41 11 0 0\r\r'
    
    # 9 seems to be the length of the shortest valid response
    if len(code) < 7:
        raise "BogusCode"
     
    # get the first thing returned, echo should be off
    # print(code)
    # code = string.split(code, "\r")
    code = code.replace(' ','');
    code = code.splitlines();
    # print(code)
    code = code[1]
    
    #remove whitespace
    code = string.split(code)
    code = string.join(code, "")
     

    if code[:6] == "NODATA": # there is no such sensor
        return 0

   	if code[:5] == "ERROR": # there is no such sensor
		return 0
    # first 4 characters are code from ELM
    code = code[4:]
    # print(code)
    return code

def get_result():
    """Internal use only: not a public interface"""
#	print "start reading"
    if ser:
        buffer = ""
        while 1:
            c = ser.read(1)
            if c == '>' and len(buffer) > 0:
                break
            else:
                buffer = buffer + c
        return buffer
#	    print "done"
    return None

def send_code(code):
	ser.write(code+' \r')
	result = get_result()
	val = interpret_result(result)
	val = float(int('0x'+val, 0 ))
	return val


cur = db.cursor() 
if ser:
	print('opened port')
	while True:
		print('writing')
		speed = send_code("01 0D")*0.62137
		rpm = send_code("01 0C")/4
		fuel = send_code("01 2F")*100/255
		print 'fuel',fuel,'rpm',rpm,'speed',speed,'mph'
		print '------------------------------------------'
		
		cur.execute("INSERT INTO cars (fuel, rpm, speed, time) VALUES (%s,%s,%s,%s)",(fuel,rpm,speed,time.time()))
		db.commit() 
		time.sleep(0.1)
else:
	print('error opening port')	