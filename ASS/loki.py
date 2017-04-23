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

def loki (bound_lat, bound_lon, bound_radius, polling, flag):	

	port = serial.Serial("/dev/ttyAMA0",9600, timeout=1.0)
	gprmc = nmea.GPRMC()
	print "Bound Latitude: " + bound_lat
	print "Bound Longitude: " + bound_lon
	print "Bound Radius: " + bound_radius
	print "Patient Status Flag: " + flag
	
	try:
		bound_lat = float(bound_lat)
	except ValueError:
		print "Lat Value Error" + bound_lat
	try:
		bound_lon = float(bound_lon)
	except ValueError:
		print "Lon Value Error" + bound_lon	
	try:
		bound_radius = float(bound_radius)
	except ValueError:
		print "Rad Value Error" + bound_radius
	
	while True:
		rcvd = port.readline()
		if rcvd[0:6] == '$GPRMC':
			gprmc.parse(rcvd)
			if gprmc.data_validity == 'V':
				print "No Location Found"
				location = {"latitude": "28.6647183333", "longitude": "77.2320366667", "flag": flag}
				data=json.dumps(location)
				return (json.dumps(location))
				

			else: 
				gprmc.parse(rcvd)
				latitude = gprmc.lat
				try:					
					latitude = float(latitude)				
				except ValueError:
					print "Lat Value Error " + latitude
				lat_direction = gprmc.lat_dir
				longitude = gprmc.lon
				try:
					longitude = float(longitude)
				except ValueError:
					print "Longitude Value Error " + longitude
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

				latitude = lat_dec_deg
				longitude = lon_dec_deg

				print "Current Latitude: " + str(latitude) + str(lat_direction)
				print "Current Longitude: " + str(longitude) + str(lon_direction)
				print "Time: "+str(gps_hour)+":"+str(gps_min)+":"+str(gps_sec)

				earth_radius = 6371*1000     
				dLat = (latitude - bound_lat)*math.pi/180.0
				dLon = (longitude - bound_lon)*math.pi/180.0
				latitude_rad = latitude*math.pi/180.0
				bound_lat_rad = bound_lat*math.pi/180.0
				val = math.sin(dLat/2.0) * math.sin(dLat/2.0) + math.sin(dLon/2.0)*math.sin(dLon/2.0)*math.cos(bound_lat_rad)*math.cos(latitude_rad)
				ang = 2*math.atan2(math.sqrt(val), math.sqrt(1.0-val))
				distance = earth_radius*ang
				print "Distance from Bound Location: " + str(distance)

				#Send Latitude Longitude 
				if distance>bound_radius and polling=="yes" and flag == "0":
					flag = "1"
					print "Patient outside Boundary"
					s = alert()
				elif distance<=bound_radius and polling=="yes" and flag=="1":
					flag = "0"
					print "Patient back in Boundary"
				location = {"latitude": str(lat_dec_deg), "longitude": str(lon_dec_deg), "flag": flag }				
				data=json.dumps(location)
				return (json.dumps(location))

		'''else:
			location = {"latitude": "28.6647183333", "longitude": "77.2320366667"}
			location = {"latitude": "28.5534601", "longitude": "77.2425807"}
			data=json.dumps(location)  
			print "Nothing works"
			return (json.dumps(location))'''		