from Utils import IBMWatsonAPI
from Utils import FacebookAPI
from Utils import OpenWeatherMapAPI as WeatherAPI
from Utils.db import example
import json


def process_message(msg, cli):
    (intents, entities, newContext, output) = IBMWatsonAPI.send_message(msg, cli.context)

    json_newContext = json.dumps(newContext, indent=2)
    example.update_client_context(cli.id, json_newContext)

    for m in output:
        FacebookAPI.send_message(cli.id, m)
        if m == 'I got you!':
            if newContext['date'] is None:
                next_days_forecast(newContext, cli)
            elif newContext['time'] is not None:
                simple_forecast(newContext, cli, True)
            else:
                simple_forecast(newContext, cli)


def simple_forecast(context, cli, hour=False):
    prevision = WeatherAPI.getForecastCity(context['location'])
    if hour:
        icon, title, subtitle = WeatherAPI.generateSimpleForecastDay(prevision, context['date'], context['time'])
        FacebookAPI.send_picture(cli.id, icon, title, subtitle)
    else:
        elements = WeatherAPI.generateForecastDay(prevision, context['date'])
        FacebookAPI.send_list(cli.id, elements)
    example.update_client_context(cli.id, None)


def next_days_forecast(context, cli):
    prevision = WeatherAPI.getForecastCity(context['location'])
    elements = WeatherAPI.generateForecastPosts(prevision)
    FacebookAPI.send_list(cli.id, elements)
    example.update_client_context(cli.id, None)
