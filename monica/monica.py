r"""

monica helps you order food from the terminal

Usage:
  monica surprise
  monica restaurant <restaurant-id>
  monica search <name>
  monica reviews <id>
  monica budget <budget>
  monica cuisine (<id>| list)
  monica configure
  monica (-h |--help)

Options:
  -h --help   Show this screen.
  --version   Show version.

"""
import requests
from docopt import docopt
import sys
import json
from config import configure
from pprint import pprint

try:
  from config import config
except:
  print 'No Configuration File Found'

from tabulate import tabulate
import random

__version__ = '0.0.2'
headers = {'Accept' : 'application/json', 'user_key': config['api_key'], 'User-Agent': 'curl/7.35.0'}


def url_shorten(longurl):
  url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyA76APOb611GHyJS_7ly_l-0Btvr798LcE'
  try:
    response = requests.post(url, headers = {'Content-Type' : 'application/json'}, data = json.dumps({'longUrl': longurl}))
    if response.status_code == 200:
      data = response.json()
      return data['id']
    else:
      return "Couldn't Shorten"
  except:
    return "Couldnt Shorten"

def surprise():
  url = 'https://developers.zomato.com/api/v2.1/geocode?lat=%s&lon=%s' %(config['lat'], config['lon'])
  try:
    response =requests.get(url, headers = headers)
    if response.status_code == 200:
      data = response.json()
      restaurants = data['nearby_restaurants']
      while True:
        if restaurants == {}:
          print 'Sorry nothing in your budget :('
          return
        key = random.choice(restaurants.keys())
        budget = restaurants[key]['restaurant']['average_cost_for_two']
        if float(budget)/2 <= config['budget']:
          restaurant = restaurants[key]['restaurant']
          break
        else:
          restaurants.pop(key, None)
      table = [[restaurant["id"] , restaurant["name"], restaurant["currency"] + " " + str(float(restaurant['average_cost_for_two'])/2) , url_shorten(restaurant["menu_url"]), restaurant["user_rating"]["aggregate_rating"], restaurant["location"]["address"][:40] ]]
      print tabulate(table, headers=["ID", "Name", "Budget", "Menu", "Rating", "Address"])
    else:
      print 'Api Issues!'
  except:
    print 'Network Issues!'


def cuisine(cuisine):
  if cuisine == 'list':
    url = "https://developers.zomato.com/api/v2.1/cuisines?city_id=%s&lat%s&lon=%s" %(config['city_id'], config['lat'], config['lon'])
    try:
      response = requests.get(url, headers=headers)
      if response.status_code == 200:
        data = response.json()
        cuisines = data['cuisines']
        cuisine_list = []
        for cuisine in cuisines:
          cuisine = cuisine['cuisine']
          cuisine_list.append([cuisine["cuisine_id"], cuisine["cuisine_name"]])
        print tabulate(cuisine_list, headers=["ID", "Cuisine Name"])
      else:
        print 'Api Error'
    except:
      print 'Network Error'
      return
  else:
    url = "https://developers.zomato.com/api/v2.1/search?count=10&lat=%s&lon=%s&cuisines=%s&sort=cost" %(config['lat'], config['lon'], cuisine)
    try:
      response= requests.get(url, headers=headers)
      if response.status_code == 200:
        data = response.json()
        count  = data['results_found']
        if count == 0:
          print "Nothing Found!"
        else:
          restaurants = data["restaurants"]
          restaurants_list = []
          for restaurant in restaurants:
            restaurant = restaurant['restaurant']
            restaurants_list.append([restaurant["id"] , restaurant["name"], restaurant["currency"]
      + " " + str(float(restaurant['average_cost_for_two'])/2) , url_shorten(restaurant["menu_url"]), restaurant["user_rating"]["aggregate_rating"], restaurant["location"]["address"][:40]])
          print tabulate(restaurants_list, headers=["ID", "Name", "Budget", "Menu", "Rating", "Address"])
      else:
        print "Something went wrong!"
    except:
      print 'Something went wrong!'
def restaurant(resid):
	try:
		url = 'https://developers.zomato.com/api/v2.1/restaurant?res_id=' + str(resid)
		r = requests.get(url,headers=headers)
		restaurants = []
		if r.status_code != 200:
			print "Something went wrong!"
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
		print tabulate([[i['id'], i['name'], i['budget'], i['menu'], i['rating'], i['address']] for i in restaurants], headers=['ID', 'Name', 'Budget', 'Menu', 'Rating', 'Address'])
	except:
		print "Something went wrong!"
		return

def reviews(id):
  url = "https://developers.zomato.com/api/v2.1/reviews?res_id=%s&count=5"%(id)
  try:
    response = requests.get(url, headers=headers)
  except:
    print 'Something went wrong!'
  if response.status_code == 200:
    data = response.json()
    count= data["reviews_count"]
    if count == 0:
      print 'No Reviews!'
    else:
      for review in data["user_reviews"]:
        review  = review["review"]
        print review["rating"]
        print review["review_text"]
        print "Posted: ",
        print review["review_time_friendly"]
        print "--------------"
  else:
    print 'Something went wrong'

def search(name):
	try:
		url = 'https://developers.zomato.com/api/v2.1/search?q=' + str(name) + '&count=10&lat=' + str(config['lat']) + '&lon=' + str(config['lon'])
		r = requests.get(url,headers=headers)
		restaurants = []
		if r.status_code != 200:
			print "Something went wrong!!"
			return
		if len(r.json()['restaurants'])	<= 0:
			print "Something went wrong!!"
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
		print tabulate([[i['id'], i['name'], i['budget'], i['menu'], i['rating'], i['address']] for i in restaurants], headers=['ID', 'Name', 'Budget', 'Menu', 'Rating', 'Address'])
	except:
		print "Something went wrong!"
		return

def budget(max_budget):
	try:
		url = 'https://developers.zomato.com/api/v2.1/search?q=&count=100&lat=' + str(config['lat']) + '&lon=' + str(config['lon']) +' &sort=cost&order=asc'
		r = requests.get(url,headers=headers)
		restaurants = []
		if r.status_code != 200:
			print "Something went wrong!!"
			return
		if len(r.json()['restaurants'])	<= 0:
			print "Something went wrong!!"
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
		print tabulate([[i['id'], i['name'], i['budget'], i['menu'], i['rating'], i['address']] for i in restaurants], headers=['ID', 'Name', 'Budget', 'Menu', 'Rating', 'Address'])
	except:
		print "Something went wrong!"
		return

def main():
  '''monica helps you order food from the timeline'''
  arguments = docopt(__doc__, version=__version__)

  if arguments['configure']:
    configure()
  if arguments['cuisine']:
    if arguments['list']:
      cuisine('list')
    else:
      cuisine(arguments['<id>'])
  elif arguments['surprise']:
    surprise()
  elif arguments['reviews']:
    reviews(arguments['<id>'])
  elif arguments['search']:
    search(arguments['<name>'])
  elif arguments['search']:
      search(arguments['<name>'])
  elif arguments['budget']:
    try:
      money = arguments['<budget>']
      money = float(money)
      budget(money)
    except:
      print 'Budget should be a number!'
  elif arguments['restaurant']:
    restaurant(arguments['<restaurant-id>'])
  else:
    print (__doc__)



if __name__ == '__main__':
  main()