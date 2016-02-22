r"""

monica helps you order food from the terminal

Usage:
  monica surprise
  monica <restaurant-name>
  monica search <restaurant name>
  monica trending
  monica budget <per-person-cost>
  monica cuisine (chinese | indian | ..)
  monica config

Options:
  -h --help   Show this screen.
  --version   Show version.

"""
import requests
from docopt import docopt
from tabulate import tabulate
from pyshorteners import Shortener

__version__ = '0.0.2'

headers = {'Accept': 'application/json','User-Agent': 'curl/7.35.0','user_key': config['api']}
google_api_key = 'AIzaSyA76APOb611GHyJS_7ly_l-0Btvr798LcE'
shortener = Shortener('GoogleShortener', api_key=google_api_key)
shortenerTinyUrl = Shortener('TinyurlShortener')


def url_shorten(url):
	try:
		short_url = shortener.short(url)	
		return short_url
	except:
		try:
			shortenerTinyUrl.short(url)
		except:
			return "Not Found"


def restaurant(resid):
	try:
		url = 'https://developers.zomato.com/api/v2.1/restaurant?res_id=' + str(resid)
		r = requests.get(url,headers=headers)
		print r.status_code
		restaurants = []
		if r.status_code != 200:
			print r.status_code
			print "Oops! Something went wrong! \n A lot many restaurants wait for you!!"
			return
		res = r.json()
		rest = {}
		rest['id'] = res['id']
		rest['name'] = res['name']
		rest['budget'] = float(res['average_cost_for_two'])/2	
		rest['menu'] = url_shorten(res['menu_url'])			
		rest['rating'] = res['user_rating']['aggregate_rating']
		rest['address'] = res['location']['address'][:40]
		restaurants.append(rest)
		print tabulate([[i['id'], i['name'], i['budget'], i['menu'], i['rating'], i['address']] for i in restaurants], headers=['Id', 'Name', 'Budget', 'Menu', 'Rating', 'Address'])
	except:
		print "Oops! Something went wrong! \n A lot many restaurants wait for you!!"
		return


def search(name):
	try:
		url = 'https://developers.zomato.com/api/v2.1/search?q=' + str(name) + '&count=10&lat=' + str(config['lat']) + '&lon=' + str(config['lon'])
		r = requests.get(url,headers=headers)
		restaurants = []
		if r.status_code != 200:
			print "Oops! Something went wrong! \nA lot many restaurants wait for you!!"
			return
		if len(r.json()['restaurants'])	<= 0:	
			print "Oops! Something went wrong! \nA lot many restaurants wait for you!!"
			return
		for res in r.json()['restaurants']:	
			rest = {}
			rest['id'] = res['restaurant']['id']
			rest['name'] = res['restaurant']['name']
			rest['budget'] = res['restaurant']['currency'] + ' ' + str(float(res['restaurant']['average_cost_for_two'])/2)
			rest['menu'] = url_shorten(res['restaurant']['menu_url'])			
			rest['rating'] = res['restaurant']['user_rating']['aggregate_rating']
			rest['address'] = res['restaurant']['location']['address'][:40]
			restaurants.append(rest)
		print tabulate([[i['id'], i['name'], i['budget'], i['menu'], i['rating'], i['address']] for i in restaurants], headers=['Id', 'Name', 'Budget', 'Menu', 'Rating', 'Address'])
	except:
		print "Oops! Something went wrong! \n A lot many restaurants wait for you!!"
		return

def budget(max_budget):
	try:
		url = 'https://developers.zomato.com/api/v2.1/search?q=&count=100&lat=' + str(config['lat']) + '&lon=' + str(config['lon']) +' &sort=cost&order=asc'
		r = requests.get(url,headers=headers)
		restaurants = []
		if r.status_code != 200:
			print "Oops! Something went wrong! \nA lot many restaurants wait for you!!"
			return
		if len(r.json()['restaurants'])	<= 0:	
			print "Oops! Something went wrong! \nA lot many restaurants wait for you!!"
			return
		for res in r.json()['restaurants']:
			if 	float(res['restaurant']['average_cost_for_two'])/2 <= int(max_budget):		
				rest = {}
				rest['id'] = res['restaurant']['id']
				rest['name'] = res['restaurant']['name']
				rest['budget'] = res['restaurant']['currency'] + ' ' + str(float(res['restaurant']['average_cost_for_two'])/2)
				rest['menu'] = url_shorten(res['restaurant']['menu_url'])			
				rest['rating'] = res['restaurant']['user_rating']['aggregate_rating']
				rest['address'] = res['restaurant']['location']['address'][:40]
				restaurants.append(rest)
			else:	
				break
		print tabulate([[i['id'], i['name'], i['budget'], i['menu'], i['rating'], i['address']] for i in restaurants], headers=['Id', 'Name', 'Budget', 'Menu', 'Rating', 'Address'])
	except:
		print "Oops! Something went wrong! \n A lot many restaurants wait for you!!"
		return


