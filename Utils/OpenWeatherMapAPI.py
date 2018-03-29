import requests, json, os
from Utils import FacebookAPI
from flask import url_for

# Environment variable on heroku
#OPEN_WEATHER_MAP_API_KEY = os.environ['OPEN_WEATHER_MAP_API_KEY']

# JUST FOR DEBUG PURPOSES
OPEN_WEATHER_MAP_API_KEY = '6979706d12688265a5ba7d3b5590625f'

# Requesting current weather based on user's location
# Example: http://api.openweathermap.org/data/2.5/weather?lat=41.556933003653&lon=-8.3991009308468&units=metric&appid=6979706d12688265a5ba7d3b5590625f
def getCurrentWeather(latitude, longitude):
    api_key = OPEN_WEATHER_MAP_API_KEY
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params = {'lat': latitude, 'lon': longitude, 'units': 'metric', 'APPID': api_key})
    return r.json() 

# Sending weather info through an image (weather.icon), current temperature and weather description
def sendWeatherInfo(sender_id, data):
    icon = data['weather'][0]['icon']
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    icon_url = f'http://openweathermap.org/img/w/{icon}.png'
    FacebookAPI.send_picture(sender_id, icon_url, f'{temperature} ºC', f'Description: {description}')
