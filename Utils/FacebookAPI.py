import requests, json, os
from flask import url_for
from Utils import OpenWeatherMapAPI 

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

# Send text message
def send_message(user_id, text):
    data = json.dumps({
        'recipient': {'id': user_id},
        'message': {'text': text}
    })

    response = requests.post('https://graph.facebook.com/v2.6/me/messages', params = params, headers = headers, data = data)
    if response.status_code != response.ok: 
        print(response.status_code)
        print(response.text)

# Send picture
def send_picture(user_id, imageUrl, title="", subtitle=""):
    if title != "":
        data = json.dumps({
            "recipient": {"id": user_id},
                "message":{
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "image_aspect_ratio": "square",
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

# Send trending news (carousel of generic templates)
def send_carousel(user_id, elements):
    data = json.dumps({
        'recipient': {'id': user_id},
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': elements[:10]               # scrollable carousel supports up to 10 generic templates
                }
            }
        }
    })

    response = requests.post("https://graph.facebook.com/v2.6/me/messages", params = params, data = data, headers = headers)
    if response.status_code != response.ok:
        print(response.status_code)
        print(response.text)    

def send_list(user_id, elements, header_style = 'compact'):
    data = json.dumps({
        'recipient': {'id': user_id},
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'list',
                    'top_element_style': header_style, 
                    'elements': elements[:4]               # list supports up to 4 elements
                }
            }
        }
    })

    response = requests.post("https://graph.facebook.com/v2.6/me/messages", params = params, data = data, headers = headers)
    if response.status_code != response.ok:
        print(response.status_code)
        print(response.text)        