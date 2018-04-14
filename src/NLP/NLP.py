from src.APIs import IBMWatsonAPI
from src.APIs import FacebookAPI
from src.NLP import WeatherNLP
from src.NLP import NewsNLP
from src.Models import Client
import json

# processes the client message and select the related API
def process_message(client_id, msg):
    cli = Client.get_client(client_id)
    if cli is None:
        cli = Client.insert_client(client_id, None)

    results = IBMWatsonAPI.send_message(msg, cli.context)
    __selectAPI(results, cli)

# method select the correct API and deals with invalid request
def __selectAPI(results, cli):
    (_,_,newContext,output) = results

    switch_request = {
        'WeatherRequest': WeatherNLP.process_message,
        'NewsRequest': NewsNLP.process_message,
    }
    switch_request.get(newContext['node'], __invalid_request)(results, cli)

# method deals with invalid request
def __invalid_request(results, cli):
    print('ANYTHING ELSE')
    (_,_,newContext,output) = results
    json_newContext = json.dumps(newContext, indent=2)
    Client.update_client_context(cli.id, json_newContext)

    for m in output:
        FacebookAPI.send_message(cli.id, m)
