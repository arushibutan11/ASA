# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import serial
import time
from pynmea import nmea
from django.shortcuts import render
import string
import math
from alert import alert
import json
from django.http import HttpResponse
def loki (bound_lat, bound_lon, bound_radius):	

	#Calculate Current Coordinates
	port = serial.Serial("/dev/ttyAMA0",9600, timeout=3.0)
	gpgga = nmea.GPGGA()
	gprmc = nmea.GPRMC()

	while True:
		rcvd = port.readline()
		if rcvd[0:6] == '$GPRMC':
			gprmc.parse(rcvd)
			if gprmc.data_validity == 'V':
				print "No Location Found"
				location = {"latitude": 28.66, "longitude": 77.23}
				data=json.dumps(location)
				return (json.dumps(location))
				

			else: 
				gprmc.parse(rcvd)
				latitude = gprmc.lat
				try:
					latitude = float(latitude)
				except ValueError:
					print "Lat Value Error" + latitude
				lat_direction = gprmc.lat_dir
				try:
					longitude = float(gprmc.lon)
				except ValueError:
					print "Longitude Value Error" + longitude
				lon_direction = gprmc.lon_dir

			
				gps_time = float(gprmc.timestamp)
				gps_hour = int(gps_time/10000.0)
				gps_min = gps_time%10000.0
				gps_sec = gps_min%100.0
				gps_min = int(gps_min/100.0)
				gps_sec = int(gps_sec)

				lat_deg = int(latitude/100.0) 
				lat_min = latitude - (lat_deg*100)
				lat_dec_deg = lat_deg + (lat_min/60)
			
				lon_deg = int(longitude/100.0)
				lon_min = longitude - (lon_deg*100)
				lon_dec_deg = lon_deg + (lon_min/60)
				lon_sec = lon_min%100.0
				lon_min = int(lon_min/100.0)
				location = {"latitude": str(lat_dec_deg) + str(lat_direction), "longitude": str(lon_dec_deg) + str(lon_direction)}
				print "Time: "+str(gps_hour)+":"+str(gps_min)+":"+str(gps_sec)
				print "Latitude: " + str(lat_dec_deg) + str(lat_direction)
				print "Longitude: " + str(lon_dec_deg) + str(lon_direction)
				bound_lat = 28.6655775
				bound_lon = 77.232728
				bound_radius = 160
				latitude = 28.664227
				longitude = 77.232989
				earth_radius = 6371*1000
				dLat = (latitude - bound_lat)*math.pi/180
				dLon = (longitude - bound_lon)*math.pi/180
				latitude = latitude*math.pi/180
				bound_lat = bound_lat*math.pi/180
				val = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2)*math.sin(dLon/2)*math.cos(bound_lat)*math.cos(latitude)
				ang = 2*math.atan2(math.sqrt(val), math.sqrt(1-val))
				distance = earth_radius*ang
				#Send Latitude Longitude 
				if distance>bound_radius:
					print "Patient Lost"
					s = alert()		

				
				data=json.dumps(location)
				return (json.dumps(location))
				#Calculate dist between bound_coord and current location
		'''else:
			location = {"latitude": 28.66, "longitude": 77.23}
			data=json.dumps(location)  
			print "Nothing works"
			return (json.dumps(location))'''		