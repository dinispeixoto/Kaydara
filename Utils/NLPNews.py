from Utils import IBMWatsonAPI
from Utils import FacebookAPI
from Utils import NewsAPI
from Utils.db import example
import json


def process_message(msg, cli):
    (intents, entities, newContext, output) = IBMWatsonAPI.send_message(msg, cli.context)

    json_newContext = json.dumps(newContext, indent=2)
    example.update_client_context(cli.id, json_newContext)

    for m in output:
        FacebookAPI.send_message(cli.id, m)
        if m == 'I got you!':
            send_news(newContext, cli)


def send_news(context, cli):
    news = NewsAPI.getTopHeadlines(context['topic'])
    elements = NewsAPI.generateNewsPosts(news)
    FacebookAPI.send_carousel(cli.id, elements)
    example.update_client_context(cli.id, None)
