# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import serial
import time
from pynmea import nmea
from django.shortcuts import render
import string
import math
from loki import loki
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def location(request):
	if request.method == 'POST':
		bound_lat = request.POST.get('bound_lat')
		bound_lon = request.POST.get('bound_lon')
		bound_radius = request.POST.get('bound_radius')
		polling = request.POST.get('polling')		
		flag = request.POST.get('flag')
		if flag == None:
			flag = "0"
		data = loki(bound_lat, bound_lon, bound_radius, polling, flag)
		print polling
		print "json data " + data
		return HttpResponse(data)
		
	else:
		return HttpResponse("Insufficient Data")
	

