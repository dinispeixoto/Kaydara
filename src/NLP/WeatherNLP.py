from src.APIs import OpenWeatherMapAPI as WeatherAPI, FacebookAPI
from src.MsgBuilder import WeatherMB
from src.Models import Client

import json, datetime

def process_message(results, cli):
    print('WEATHER REQUEST')
    (newContext, output, message) = results

    json_newContext = json.dumps(newContext, indent=2)
    Client.update_client_context(cli.id, json_newContext)

    for m in output:
        if m == '[OK] Process request':
            if newContext['date'] is None and newContext['time'] is None:
                if newContext['type'] == 'weather':
                    current_weather(newContext, cli)
                elif newContext['type'] == 'forecast':
                    next_days_forecast(newContext, cli)
            elif newContext['time'] is not None:
                simple_forecast(newContext, cli, True)
            else:
                simple_forecast(newContext, cli)
        elif m != '':
            FacebookAPI.send_message(cli.id, m)


def current_weather(context, cli):
    prevision = WeatherAPI.getCurrentWeatherCity(context['location'])
    icon, title, subtitle = WeatherMB.generateCurrentWeatherInfo(prevision)
    FacebookAPI.send_picture(cli.id, icon, title, subtitle)


def simple_forecast(context, cli, hour=False):
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


def next_days_forecast(context, cli):
    prevision = WeatherAPI.getForecastCity(context['location'])
    elements = WeatherMB.generateForecastPosts(prevision)
    FacebookAPI.send_list(cli.id, elements)
    Client.update_client_context(cli.id, None)
