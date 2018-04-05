from src.APIs import IBMWatsonAPI
from src.APIs import FacebookAPI
from src.APIs import OpenWeatherMapAPI as WeatherAPI
from src.MsgBuilder import WeatherMB
from src.Models import Client
import json


def process_message(results, cli):
    print('WEATHER REQUEST')
    (intents, entities, newContext, output) = results

    json_newContext = json.dumps(newContext, indent=2)
    Client.update_client_context(cli.id, json_newContext)

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
        icon, title, subtitle = WeatherMB.generateSimpleForecastDay(prevision, context['date'], context['time'])
        FacebookAPI.send_picture(cli.id, icon, title, subtitle)
    else:
        elements = WeatherMB.generateForecastDay(prevision, context['date'], True)
        FacebookAPI.send_list(cli.id, elements)
    Client.update_client_context(cli.id, None)


def next_days_forecast(context, cli):
    prevision = WeatherAPI.getForecastCity(context['location'])
    elements = WeatherMB.generateForecastPosts(prevision)
    FacebookAPI.send_list(cli.id, elements)
    Client.update_client_context(cli.id, None)
