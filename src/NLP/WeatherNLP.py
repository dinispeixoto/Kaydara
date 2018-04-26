from src.APIs import OpenWeatherMapAPI as WeatherAPI, FacebookAPI
from src.MsgBuilder import WeatherMB
from src.Models import Client

import json, datetime

def process_message(results, cli):
    print('WEATHER REQUEST')
    (context, output, message) = results

    json_context = json.dumps(context, indent=2)
    Client.update_client_context(cli.id, json_context)

    for m in output:
        if m == '[OK] Process request':
            print(f"LOCATION = {context['location']}")
            coordinates = (context['location'] == ' or coordinates')
            if not coordinates:
                context['location'] = process_keyword(context['location']) 
                print(f"LOCATION = {context['location']}")

            if context['date'] is None and context['time'] is None:
                if context['type'] == 'weather':
                    current_weather(context, cli, coordinates)
                elif context['type'] == 'forecast':
                    next_days_forecast(context, cli, coordinates)
            elif context['time'] is not None:
                simple_forecast(context, cli, coordinates, True)
            else:
                simple_forecast(context, cli, coordinates)
        elif m == 'Can you give me a location?':
            FacebookAPI.send_quick_replies(cli.id, WeatherMB.quick_reply_location(), m)
        elif m != '':
            FacebookAPI.send_message(cli.id, m)

def current_weather(context, cli, coordinates):
    if coordinates:
        prevision = WeatherAPI.getCurrentWeatherCoordinates(context['lat'], context['long'])
    else:
        prevision = WeatherAPI.getCurrentWeatherCity(context['location'])
    icon, title, subtitle = WeatherMB.generateCurrentWeatherInfo(prevision)
    FacebookAPI.send_picture(cli.id, icon, title, subtitle)

def simple_forecast(context, cli, coordinates, hour=False):
    if coordinates:
        prevision = WeatherAPI.getForecastCoordinates(context['lat'], context['long'])
    else:
        prevision = WeatherAPI.getForecastCity(context['location'])

    if hour:
        icon, title, subtitle = WeatherMB.generateSimpleForecastDay(prevision, context['date'], context['time'])
        FacebookAPI.send_picture(cli.id, icon, title, subtitle)
    else:
        current_day = datetime.date.today().strftime('%y-%m-%d')
        current_hour = datetime.datetime.now().strftime('%H')

        if current_day in context['date']:
            if current_hour < '03:00:00':
                elements = WeatherMB.generateForecastDay(prevision, context['date'])
            else:
                elements = WeatherMB.generateForecastDay(prevision, context['date'], True)
        else:
            elements = WeatherMB.generateForecastDay(prevision, context['date'])
        FacebookAPI.send_list(cli.id, elements)
    Client.update_client_context(cli.id, None)


def next_days_forecast(context, cli, coordinates):
    if coordinates:
        prevision = WeatherAPI.getForecastCoordinates(context['lat'], context['long'])
    else:
        prevision = WeatherAPI.getForecastCity(context['location'])
    elements = WeatherMB.generateForecastPosts(prevision)
    FacebookAPI.send_list(cli.id, elements)
    Client.update_client_context(cli.id, None)

def process_keyword(keyword):
    if keyword:
        return ' '.join(i for i in keyword.split() if i != 'or')
    else:
        return None
