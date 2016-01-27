# Michael McGuirk - DT228/4 - FYP
import os
import glob
import time
import datetime
import RPi.GPIO as G
import MySQLdb
import logging
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
G.setmode(G.BCM)
G.setup(2,G.OUT)

db=MySQLdb.connect("protodb.ctyoee9uibzm.us-west-2.rds.amazonaws.com","root","pibrewing","prototemps")
print "SQL DB Connect success"
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
temp_max = 20.00
temp_min = 15.00

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c, temp_f

# Read the user defined low and high settings from the database. Return in tuple.
def read_user_temp():
	cursor.execute("SELECT temp_low_c, temp_high_c FROM current_temp")
	temps = cursor.fetchone()
	temp_low = float(temps[0])
	temp_high = float(temps[1])
	return temp_low, temp_high


while True:
	currentTime = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
	print(currentTime)
	print(read_temp())
	try:
		cursor.execute("INSERT INTO temps(tempc,tempf)VALUES(%.2f, %.2f)" % (read_temp()[0],read_temp()[1]))
		db.commit()
		user_temps = read_user_temp()
		temp_low = user_temps[0]
		temp_high = user_temps[1]
		# Need to select high and lowest from current_temp here 
	except MySQLdb.Error, e:
		print "MySQL Error: %s" % str(e)

	# Adjust relay within temperature range
	temp_c = read_temp()[0]
	if temp_c > temp_max:
		G.output(2,G.LOW)
		print "Relay is off"
	elif temp_c <= temp_max:
		G.output(2,G.HIGH)
		print "Relay is now on"
	
	# Wait 30 seconds before taking the next reading.
	time.sleep(30)

