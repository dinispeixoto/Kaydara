import requests, json, os
from flask import url_for
from dateutil import parser

# Environment variable on heroku
OPEN_WEATHER_MAP_API_KEY = os.environ['OPEN_WEATHER_MAP_API_KEY']

# Requesting current weather based on user's location
# Example: http://api.openweathermap.org/data/2.5/weather?lat=41.556933003653&lon=-8.3991009308468&units=metric&appid=6979706d12688265a5ba7d3b5590625f
def getCurrentWeatherCoordinates(latitude, longitude):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params = {'lat': latitude, 'lon': longitude, 'units': 'metric', 'APPID': OPEN_WEATHER_MAP_API_KEY})
    return r.json() 

# Requesting current weather based on a given city
# Query examples can be: 'Braga' or 'Braga, PT' or 'Braga, Portugal'.
# Example: http://api.openweathermap.org/data/2.5/weather?q=Braga&units=metric&appid=6979706d12688265a5ba7d3b5590625f
def getCurrentWeatherCity(query):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params = {'q': query, 'units': 'metric', 'APPID': OPEN_WEATHER_MAP_API_KEY})
    return r.json() 

# Requesting forecast based on user's location
# Example: http://api.openweathermap.org/data/2.5/forecast?lat=41.556933003653&lon=-8.3991009308468&units=metric&appid=6979706d12688265a5ba7d3b5590625f
def getForecastCoordinates(latitude, longitude):
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast', params = {'lat': latitude, 'lon': longitude, 'units': 'metric', 'APPID': OPEN_WEATHER_MAP_API_KEY})
    return r.json()

# Requesting forecast based on a given city
# Example: http://api.openweathermap.org/data/2.5/forecast?q=Braga&units=metric&appid=6979706d12688265a5ba7d3b5590625f
def getForecastCity(query):
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast', params = {'q': query, 'units': 'metric', 'APPID': OPEN_WEATHER_MAP_API_KEY})
    return r.json()

# Get icon_img based on given id and openweathermap's icon.
def getIcon(id, icon):
    icon_url = url_for('static', filename=f'assets/img/weather_icons/{id}-{icon}.png', _external=True)
    if not os.path.exists(icon_url):
        icon_url = url_for('static', filename=f'assets/img/weather_icons/{icon}.png', _external=True)
    return icon_url    

# Get weather description based on given description, temperature and (optionally) humidity.
def getDescription(description, temperature, humidity = None):
    if humidity:
        return f"Description: {description.capitalize()}\nTemperature: {temperature} ºC\nHumidity: {humidity}%" 
    else:
        return f"{temperature} ºC\n{description.capitalize()}"    

# Generate current weather info
def generateCurrentWeatherInfo(data):
    weather = data['weather'][0]
    icon_url = getIcon(weather['id'],weather['icon'])
    title = f"Weather in {data['name']}"
    subtitle = getDescription(weather['description'], data['main']['temp'], data['main']['humidity'])
    return icon_url, title, subtitle

# Generate weather info for specific day.
# date example = 2018-04-06
# hour example = 12:00:00
def generateSimpleForecastDay(data, date, hour = '12:00:00'):
    date_hour = f'{date} {hour}'
    data_list = data['list']
    for element in data_list:
        if element['dt_txt'] >= date_hour:
            weather = element['weather'][0]
            icon_url = getIcon(weather['id'],weather['icon'])
            title = f"Weather in {data['city']['name']} on {date} at {hour}"
            subtitle = getDescription(weather['description'], element['main']['temp'], element['main']['humidity'])
            return icon_url, title, subtitle

# Generate full forecast for specific day.
# Hours: 6:00, 12:00, 18:00, 00:00
def generateForecastDay(data, date, showAll = False):
    posts = []
    data_list = data['list']
    for element in data_list:
        if date in element['dt_txt']:
            if showAll or (not showAll and ('03:00:00' in element['dt_txt'] or '09:00:00' in element['dt_txt'] or '15:00:00' in element['dt_txt'] or '21:00:00' in element['dt_txt'])):
                weather = element['weather'][0]
                post = {
                    'title': parser.parse(element['dt_txt']).strftime('%H:%M'),
                    'image_url': getIcon(weather['id'], weather['icon']),
                    'subtitle': getDescription(weather['description'], element['main']['temp']),
                }
                posts.append(post)
    return posts              

# Generate forecast posts to send.
# Adding the first element on the list, since it's giving information about the current day.
# After that, it's only adding the elements that contain 'aproximate_hour', one for each different day.
def generateForecastPosts(data):
    posts = []
    data_list = data['list']
    aproximate_hour = parser.parse(data_list[0]['dt_txt']).strftime('%H:%M:%S')
    for element in data_list: 
        if aproximate_hour in element['dt_txt']:      
            weather = element['weather'][0]
            post = {
                'title': parser.parse(element['dt_txt']).strftime('%A'),
                'image_url': getIcon(weather['id'], weather['icon']),
                'subtitle': getDescription(weather['description'], element['main']['temp']),
            }
            posts.append(post)
    return posts
 