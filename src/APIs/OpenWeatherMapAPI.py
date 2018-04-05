import requests, json, os

# Environment variable on heroku
OPEN_WEATHER_MAP_API_KEY = os.environ['OPEN_WEATHER_MAP_API_KEY']

# Requesting current weather based on user's location
# Example: http://api.openweathermap.org/data/2.5/weather?lat=41.556933003653&lon=-8.3991009308468&units=metric&appid=6979706d12688265a5ba7d3b5590625f
def getCurrentWeatherCoordinates(latitude, longitude):
    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params = {'lat': latitude, 'lon': longitude, 'units': 'metric', 'APPID': OPEN_WEATHER_MAP_API_KEY})
    if response.status_code != response.ok:
        print(response.status_code)
        print(response.text)
    return response.json()

# Requesting current weather based on a given city
# Query examples can be: 'Braga' or 'Braga, PT' or 'Braga, Portugal'.
# Example: http://api.openweathermap.org/data/2.5/weather?q=Braga&units=metric&appid=6979706d12688265a5ba7d3b5590625f
def getCurrentWeatherCity(query):
    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params = {'q': query, 'units': 'metric', 'APPID': OPEN_WEATHER_MAP_API_KEY})
    if response.status_code != response.ok:
        print(response.status_code)
        print(response.text)
    return response.json()

# Requesting forecast based on user's location
# Example: http://api.openweathermap.org/data/2.5/forecast?lat=41.556933003653&lon=-8.3991009308468&units=metric&appid=6979706d12688265a5ba7d3b5590625f
def getForecastCoordinates(latitude, longitude):
    response = requests.get('http://api.openweathermap.org/data/2.5/forecast', params = {'lat': latitude, 'lon': longitude, 'units': 'metric', 'APPID': OPEN_WEATHER_MAP_API_KEY})
    if response.status_code != response.ok:
        print(response.status_code)
        print(response.text)
    return response.json()

# Requesting forecast based on a given city
# Example: http://api.openweathermap.org/data/2.5/forecast?q=Braga&units=metric&appid=6979706d12688265a5ba7d3b5590625f
def getForecastCity(query):
    response = requests.get('http://api.openweathermap.org/data/2.5/forecast', params = {'q': query, 'units': 'metric', 'APPID': OPEN_WEATHER_MAP_API_KEY})
    if response.status_code != response.ok:
        print(response.status_code)
        print(response.text)
    return response.json()
