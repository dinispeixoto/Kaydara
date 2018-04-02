import requests, json, os
from flask import url_for

# Environment variables on heroku
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']

params = {'access_token': PAGE_ACCESS_TOKEN}
headers = {'Content-type': 'application/json'}

# Show typing effect
def show_typing(user_id, action='typing_on'):
    data = json.dumps({
        'recipient': {'id': user_id},
        'sender_action': action
    })

    response = requests.post('https://graph.facebook.com/v2.6/me/messages', params = params, headers = headers, data = data)
    if response.status_code != response.ok:
        print(response.status_code)
        print(response.text)

# Sending text message
def send_message(user_id, text):
    data = json.dumps({
        'recipient': {'id': user_id},
        'message': {'text': text}
    })

    response = requests.post('https://graph.facebook.com/v2.6/me/messages', params = params, headers = headers, data = data)
    if response.status_code != response.ok: 
        print(response.status_code)
        print(response.text)

# Sending picture
def send_picture(user_id, imageUrl, title="", subtitle=""):
    if title != "":
        data = json.dumps({
            "recipient": {"id": user_id},
                "message":{
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": [{
                                "title": title,
                                "subtitle": subtitle,
                                "image_url": imageUrl
                            }]
                        }
                    }
                }
              })
    else:
        data = json.dumps({ 
            "recipient": {"id": user_id},
                "message":{
                    "attachment": {
                        "type": "image",
                        "payload": {
                            "url": imageUrl
                        }
                    }
                }
            })

    response = requests.post("https://graph.facebook.com/v2.6/me/messages", params = params, data = data, headers = headers)
    if response.status_code != response.ok:
        print(response.status_code)
        print(response.text)   

# Sending trending news (carousel of generic templates)
def send_trending_news(user_id, data):
    posts = []

    for element in data:
        post = {
            "title": element['title'],
            "image_url": element['urlToImage'],
            "subtitle": element['description'],
            "buttons": [
                {
                    'type': 'web_url',
                    'url': element['url'],
                    'title': 'Read more'
                }
            ]
        }
        posts.append(post)

    data = json.dumps({
        'recipient': {'id': user_id},
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': posts[:10]          # scrollable carousel supports up to 10 generic templates
                }
            }
        }
    })

    response = requests.post("https://graph.facebook.com/v2.6/me/messages", params = params, data = data, headers = headers)
    if response.status_code != response.ok:
        print(response.status_code)
        print(response.text)    