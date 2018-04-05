from src.APIs import IBMWatsonAPI
from src.APIs import FacebookAPI
from src.APIs import NewsAPI
from src.MsgBuilder import NewsMB
from src.Models import Client
import json


def process_message(results, cli):
    print('NEWS REQUEST')
    (intents, entities, newContext, output) = results
    
    json_newContext = json.dumps(newContext, indent=2)
    Client.update_client_context(cli.id, json_newContext)

    for m in output:
        FacebookAPI.send_message(cli.id, m)
        if m == 'I got you!':
            send_news(newContext, cli)


def send_news(context, cli):
    news = NewsAPI.getTopHeadlines(context['topic'])
    elements = NewsMB.generateNewsPosts(news)
    FacebookAPI.send_carousel(cli.id, elements)
    Client.update_client_context(cli.id, None)
    cli.context = None
