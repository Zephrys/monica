r"""

monica helps you order food from the terminal

Usage:
  monica surprise
  monica <restaurant-name>
  monica search <restaurant name>
  monica reviews
  monica budget <per-person-cost>
  monica cuisine (<name> | list)
  monica config

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

from docopt import docopt
from config import config
from config import configure
from tabulate import tabulate
import random

__version__ = '0.0.2'
headers = {'Accept' : 'application/json', 'user_key': config['api_key'], 'User-Agent': 'curl/7.35.0'}


def url_shorten(longurl):
  url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyA76APOb611GHyJS_7ly_l-0Btvr798Lc'
  headers = {'Content-Type' : 'application/json'}
  try:
    response = requests.post(url, headers = headers, data = {'longUrl': longurl})
    if response.status_code == 200:
      data = response.json()
      return data['id']
    else:
      return longurl
  except:
    return longurl


def surprise():
  url = 'https://developers.zomato.com/api/v2.1/geocode?lat=%s&lon=%s' %(config['lat'], config['lon'])
  try:
    response =requests.get(url, headers = headers)
  except:
    print 'Something went wrong!'
  if response.status_code == 200:
    data = response.json()
    restaurants = data['nearby_restaurants']
    while True:
      if restaurants == {}:
        print 'Sorry nothing in your budget :('
      key = random.choice(restaurants.keys())
      budget = restaurant[key]['average_cost_for_two']
      if float(budget)/2 <= config['budget']:
        restaurant = restaurant[key]
        break
      else:
        restaurants.pop(key, None)
    table = [[restaurant["id"] , restaurant["name"], restaurant["curency"]
    if not restaurant.has_key("phone_numbers"):
      restaurant["phone_numbers"] = "Not Found"
    + " " + str(float(restaurant['average_cost_for_two'])/2)] , url_shorten(restaurant["url"]), restaurant["user_rating"]["aggregate_rating"], restaurant["location"]["address"][:50]]
    print tabulate(table, headers=["ID", "Name", "Budget", "Menu", "Rating", "Address"])
  else:
    print 'Something went wrong!'



def restaurant():
  pass

def cuisine(cuisine):
  if cuisine == 'list':
    url = "https://developers.zomato.com/api/v2.1/cuisines?city_id=%s&lat%s&lon=%s" %(config.city_id, config.lat, config.lon)
    try:
      response = requests.get(url, headers=headers)
    except:
      print 'Something went wrong!'
    if response.status_code == 200:
      data = response.json()
      cuisines = data['cuisines']
      cuisine_list = []
      for cuisine in cuisines:
        cuisine_list.append(cuisine["cuisine_id"], cuisine["cuisine_name"])
      print tabulate(cuisine_list, headers=["ID", "Cuisine Name"])
  else:
    url = "https://developers.zomato.com/api/v2.1/search?count=10&lat=%s&lon=%s&cuisines=%s&sort=cost" %(config.lat, config.lon, cuisine)
    try:
      response= requests.get(url, headers=headers)
    except:
      print 'Something went wrong!'
    if response.status_code == 200:
      data = response.json()
      count  = data['results_found']
      if count == 0:
        print "Nothing Found!"
      else:
        restaurants = data["restaurants"]
        restaurants_list = []
        for restaurant in restaurants:
          if not restaurant.has_key("phone_numbers"):
            restaurant["phone_numbers"] = "Not Found"
          restaurants_list.append(restaurant["id"] , restaurant["name"], restaurant["curency"]
    + " " + str(float(restaurant['average_cost_for_two'])/2)] , url_shorten(restaurant["url"]), restaurant["user_rating"]["aggregate_rating"], restaurant["location"]["address"][:50])
        print tabulate(restaurants_list, headers=["ID", "Name", "Budget", "Menu", "Rating", "Address"])
    else:
      print "Something went wrong!"

def search():
  pass

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
        print "--------------"
        print review["rating"]
        print review["rating_text"]
        print review["review_text"]
        print review["review_time_friendly"]
        print "--------------"
  else:
    print 'Something went wrong'


def budget():
  pass

def config():
  configure()

def main():