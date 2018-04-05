from Utils import IBMWatsonAPI
from Utils import NLPWeather
from Utils import NLPNews
from Utils import FacebookAPI
from Utils.db import example
import json


def process_message(client_id, msg):
    if example.get_client(client_id) is None:
        example.insert_client(client_id, None)
        print('CLIENT CREATED')

    cli = example.get_client(client_id)

    print(cli.context)

    (intents, entities, newContext, output) = IBMWatsonAPI.send_message(msg, cli.context)

    print(newContext)

    if newContext['node'] == 'WeatherRequest':
        print('WEATHER REQUEST')
        NLPWeather.process_message(msg, cli)

    elif newContext['node'] == 'NewsRequest':
        print('NEWS REQUEST')
        NLPNews.process_message(msg, cli)

    else:
        print('ANYTHING ELSE')
        json_newContext = json.dumps(newContext, indent=2)
        example.update_client_context(cli.id, json_newContext)
        for m in output:
            FacebookAPI.send_message(cli.id, m)
