# Michael McGuirk - D13123389 - DT228/4 - FYP
# 13/03/16
import os
import glob
import time
import datetime
import RPi.GPIO as G
import MySQLdb
import logging

# Enable 1-Wire GPIO and Temperature Support
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Set location of the file where Raw data from the temperature sensor is stored.
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Setup the GPIO Connection for Relay 1
G.setmode(G.BCM)
G.setup(2,G.OUT)

# DB Connection
db=MySQLdb.connect("protodb.ctyoee9uibzm.us-west-2.rds.amazonaws.com","root","pibrewing","prototemps")
print "SQL DB Connect success"
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
temp_max = 20.00
temp_min = 15.00

max_temp = 0
min_temp = 0
target_temp = 0

# Read raw temperature data from the sensor
# Open the w1_slave file and read the data.
def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

# Parse raw temperature data
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
	cursor.execute("SELECT temp_low_c, temp_high_c, current_batch_id_id FROM current_temp")
	temps = cursor.fetchone()
	temp_low = "{0:.2f}".format(temps[0])
	#temp_low = float(temps[0])
	temp_high = "{0:.2f}".format(temps[1])
	#temp_high = float(temps[1])
	#batch_id = int(temps[2])
	batch_id = temps[2]
	return temp_low, temp_high, batch_id


while True:
	currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
	print(currentTime)
	print(read_temp())
	try:
		db.ping(True)
		user_temps = read_user_temp()
		temp_low = float(user_temps[0])
		temp_high = float(user_temps[1])
		batch_id = user_temps[2]
		#print " -- " + temp_low + " -- " + temp_high

		desired_mean_temp = (temp_low + temp_high) / 2
		if target_temp == 0:
			target_temp = desired_mean_temp


		insert_temps = """INSERT INTO temps(tempc,tempf,timestp, batch_id_id)VALUES(%s, %s, %s, %s)"""
		update_current_temp = """UPDATE current_temp SET tempc=%s,tempf=%s,timestp=%s where temp_id=1"""
		
		cursor.execute(insert_temps, (read_temp()[0],read_temp()[1],currentTime,batch_id))

		cursor.execute(update_current_temp, (read_temp()[0],read_temp()[1],currentTime))
		db.commit()
		
	except MySQLdb.Error, e:
		print "MySQL Error: %s" % str(e)

	# Adjust relay within temperature range
	temp_c = read_temp()[0]
	print "Target temperature: " + str(target_temp)

	if temp_c > target_temp:
		G.output(2,G.LOW)
		print "Relay is off"

	elif temp_c < target_temp:
		G.output(2,G.HIGH)
		print "Relay is now on"
	
	# Wait 60 seconds before taking the next reading.
	time.sleep(60)


# while True:
# 	#currentTime = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
# 	currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
# 	print(currentTime)
# 	print(read_temp())
# 	try:
# 		db.ping(True)
# 		user_temps = read_user_temp()
# 		temp_low = user_temps[0]
# 		temp_high = user_temps[1]
# 		batch_id = user_temps[2]
# 		insert_temps = """INSERT INTO temps(tempc,tempf,timestp, batch_id_id)VALUES(%s, %s, %s, %s)"""
# 		update_current_temp = """UPDATE current_temp SET tempc=%s,tempf=%s,timestp=%s where temp_id=1"""
		
# 		cursor.execute(insert_temps, (read_temp()[0],read_temp()[1],currentTime,batch_id))

# 		cursor.execute(update_current_temp, (read_temp()[0],read_temp()[1],currentTime))
# 		db.commit()
		
# 	except MySQLdb.Error, e:
# 		print "MySQL Error: %s" % str(e)

# 	# Adjust relay within temperature range
# 	temp_c = read_temp()[0]
# 	if temp_c > temp_high:
# 		G.output(2,G.LOW)
# 		print "Relay is off"
# 	elif temp_c <= temp_high:
# 		G.output(2,G.HIGH)
# 		print "Relay is now on"
	
# 	# Wait 60 seconds before taking the next reading.
# 	time.sleep(60)

