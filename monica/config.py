import json
import requests
import os
import sys

_ROOT = os.path.expanduser('~')

if not os.path.exists(os.path.join(_ROOT, ".monica/")):
	os.makedirs(os.path.join(_ROOT, ".monica/"))

def configure():
	try:
		configuration_file = open(os.path.join(_ROOT, ".monica/config.json"), "w")
		api_key = raw_input("What is your api_key?[672c3d5b9645db8dd7266626856cd015]") or '672c3d5b9645db8dd7266626856cd015'
		budget = raw_input("What is your budget(per person/in your currency)?[100]") or 100
		try:
			budget = float(budget)
		except:
			budget = 100
			print "Couldn't parse number. Going with default!"
		lat = raw_input("What is your latitude?[28.61]") or '28.61'
		lon = raw_input("What is your longitude?[77.20]") or '77.20'
		url = "https://developers.zomato.com/api/v2.1/cities?lat=%s&lon=%s" %(lat, lon)
		city_id = False
		headers = {'Accept' : 'application/json', 'user_key': api_key, 'User-Agent': 'curl/7.35.0'}
		try:
			response = requests.get(url, headers = headers)
			if response.status_code == 200:
				data = response.json()
				if data['status'] == 'success':
					city_id = data['location_suggestions'][0]['id']
			elif response.status_code == 403:
				print 'Invalid API Key'
		except:
			print 'Something went wrong while parsing the city!'
			sys.exit()
		if city_id:
			configuration = {"budget" : budget, "lat": lat, "lon": lon, "api_key": api_key, 'city_id': city_id}
			configuration_file.write(json.dumps(configuration))
		else:
			print 'Your city isnt supported'
			sys.exit()
	except:
		print "Something went wrong! Try Again?"
		sys.exit()

try:
	flag = True
	config = json.loads(open(os.path.join(_ROOT, ".monica/config.json"), "r").read())
except:
	print "no config file found"
	flag = False
	configure()
	config = json.loads(open(os.path.join(_ROOT, ".monica/config.json"), "r").read())
