from src.APIs import FacebookAPI, NewsAPI
from src.MsgBuilder import NewsMB
from src.Models import Client

import json

IRRELEVANT_WORDS = ['news', 'articles', 'most', 'recent', 'trending', 'new']

def process_message(results, cli):
    print('NEWS REQUEST')
    (newContext, output, message) = results

    json_newContext = json.dumps(newContext, indent=2)
    Client.update_client_context(cli.id, json_newContext)
    
    for m in output:
        if m == '[OK] Process request':
            print(f"ORIGINAL KEYWORD: {newContext['keyword']}")
            keyword = process_keyword(newContext['keyword'])
            print(f'RESULT KEYWORD: {keyword}')
            send_news(keyword, cli)
        elif m != '':
            FacebookAPI.send_message(cli.id, m)

def process_keyword(keyword):
    if keyword:
        return ' '.join(i for i in keyword.split() if i not in IRRELEVANT_WORDS)
    else:
        return None     

def send_news(keyword, cli): 
    if keyword:
        print(f"KEYWORD: {keyword}")
        news = NewsAPI.getTopHeadlines(keyword)
    else:
        print(f"KEYWORD: NULL")
        news = NewsAPI.getTopHeadlines()

    elements = NewsMB.generateNewsPosts(news)
    if len(elements) == 0:
        FacebookAPI.send_message(cli.id, f"Sorry but I couldn't find anything related to your keyword: {keyword}")
    else:    
        FacebookAPI.send_carousel(cli.id, elements)
    Client.update_client_context(cli.id, None)
    cli.context = None
