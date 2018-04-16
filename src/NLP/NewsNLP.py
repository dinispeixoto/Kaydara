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
        if m == '[OK] Process request':
            send_news(newContext, cli)
        elif m != '':
            FacebookAPI.send_message(cli.id, m)


def send_news(context, cli):
    news = NewsAPI.getTopHeadlines(context['keyword'])
    elements = NewsMB.generateNewsPosts(news)
    FacebookAPI.send_carousel(cli.id, elements)
    Client.update_client_context(cli.id, None)
    cli.context = None
