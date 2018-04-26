from flask import url_for
from dateutil import parser
import json, os

"""
Module where we build a perfect message to the client
"""

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
def generateSimpleForecastDay(data, date, hour):
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
# Hours: 3:00, 9:00, 15:00, 21:00
def generateForecastDay(data, date, showAll = False):
    posts = []

    data_list = data['list']
    for element in data_list:
        if date in element['dt_txt'] or len(posts) < 4:
            if showAll or date not in element['dt_txt'] or (not showAll and ('03:00:00' in element['dt_txt'] or '09:00:00' in element['dt_txt'] or '15:00:00' in element['dt_txt'] or '21:00:00' in element['dt_txt'])):
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

def quick_reply_location():
    return [
                {
                    "content_type":"location"
                }
            ]
    
