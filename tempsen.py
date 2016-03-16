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

# Setup the GPIO Connection for Relay 1 & 2
heat = 2
cool = 3
G.setmode(G.BCM)
G.setup(heat,G.OUT)
G.setup(cool,G.OUT)

# DB Connection
db=MySQLdb.connect("protodb.ctyoee9uibzm.us-west-2.rds.amazonaws.com","root","pibrewing","prototemps")
print "SQL DB Connect success"
cursor = db.cursor()
cursor.execute("SELECT VERSION()")

max_temp = 0
min_temp = 0
target_temp = 0
peak_temp = 0

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
	user_temp_low = "{0:.2f}".format(temps[0])
	user_temp_high = "{0:.2f}".format(temps[1])
	current_batch_id = temps[2]
	return user_temp_low, user_temp_high, current_batch_id

def check_overage(current_temp, batch_upper_limit):
	global peak_temp
	if peak_temp < current_temp:
		peak_temp = current_temp 
		target_temp = desired_mean_temp - (batch_upper_limit / current_temp)
		print "New target temp: " + str(target_temp)

def check_underage(current_temp, batch_lower_limit):
	global peak_temp
	if peak_temp > current_temp:
		peak_temp = current_temp
		target_temp = desired_mean_temp + (current_temp / batch_lower_limit)
		print "New target temp: " + str(target_temp)



while True:
	currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
	print(currentTime)
	print(read_temp())
	try:
		db.ping(True)
		user_temps = read_user_temp()
		user_temp_low = float(user_temps[0])
		user_temp_high = float(user_temps[1])
		current_batch_id = user_temps[2]

		desired_mean_temp = (user_temp_low + user_temp_high) / 2
		if target_temp == 0:
			target_temp = desired_mean_temp


		insert_temps = """INSERT INTO temps(tempc,tempf,timestp, batch_id_id)VALUES(%s, %s, %s, %s)"""
		update_current_temp = """UPDATE current_temp SET tempc=%s,tempf=%s,timestp=%s where temp_id=1"""
		
		cursor.execute(insert_temps, (read_temp()[0],read_temp()[1],currentTime,current_batch_id))

		cursor.execute(update_current_temp, (read_temp()[0],read_temp()[1],currentTime))
		db.commit()
		
	except MySQLdb.Error, e:
		print "MySQL Error: %s" % str(e)

	# Adjust relay within temperature range
	current_temp_c = read_temp()[0]
	print "Target temperature: " + str(target_temp)

	if current_temp_c > target_temp:
		G.output(heat,G.LOW)
		G.output(cool,G.High)
		if current_temp_c > user_temp_high:
			print "Check Overage"
			check_overage(current_temp_c, user_temp_high)

		print "Relay: Off"

	elif current_temp_c < target_temp:
		G.output(heat,G.HIGH)
		G.output(cool,G.LOW)
		if current_temp_c < user_temp_low:
			print "Check Underage"
			check_underage(current_temp_c, user_temp_low)

		print "Relay: On"
	
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

