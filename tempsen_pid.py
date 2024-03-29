# Michael McGuirk - D13123389
# DT228/4 - Final Year Project
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
previous_error = 0

# PID to manage temperature overshoots.
def pid(currrent_temp, set_point):
	dt = 60
	Kp = 0.2
	Kd = 10
	Ki = 1

	error = set_point - current_temp
	derivator = (error - previous_error)/dt
	output = Kp*error  + Kd*derivator

	print "PID Output: " + str(output)
	previous_error = error
	return output

# Read raw temperature data from the sensor
# Open the w1_slave file and read the data.

##################################################
# read_temp_raw and read_temp function source:
# Title: Adafruit's Raspberry Pi Lesson 11. DS18B20 Temperature Sensing
# Author: Simon Monk
# URL: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware
##################################################
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

# Checking for overshoot and undershoot, 
# passing overshoot to PID controller to define target temperature
def check_overshoot(current_temp, batch_upper_limit, set_point):
	global peak_temp
	if peak_temp < current_temp:
		peak_temp = current_temp 
		target_temp = set_point + pid(current_temp,set_point)
		#target_temp = desired_mean_temp - (batch_upper_limit / current_temp)
		print "New target temp: " + str(target_temp)

def check_undershoot(current_temp, batch_lower_limit, set_point):
	global peak_temp
	if peak_temp > current_temp:
		peak_temp = current_temp
		target_temp = set_point + pid(current_temp,set_point)
		#target_temp = desired_mean_temp + (current_temp / batch_lower_limit)
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

	# Temperatre too high
	if current_temp_c > target_temp:
		G.output(heat,G.HIGH)
		G.output(cool,G.LOW)
		if current_temp_c > user_temp_high:
			print "Check Overage"
			check_overshoot(current_temp_c, user_temp_high, desired_mean_temp)

		print "Relay: Off"

	elif current_temp_c < target_temp:
		G.output(heat,G.LOW)
		G.output(cool,G.HIGH)
		if current_temp_c < user_temp_low:
			print "Check Underage"
			check_undershoot(current_temp_c, user_temp_low, desired_mean_temp)

		print "Relay: On"
	
	# Wait 60 seconds before taking the next reading.
	time.sleep(60)
