import requests, json, os
from flask import url_for
from src.APIs import OpenWeatherMapAPI 

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
    __send(data)

# Send text message
def send_message(user_id, text):
    show_typing(user_id,'typing_off')
    data = json.dumps({
        'recipient': {'id': user_id},
        'message': {'text': text}
    })
    __send(data)

# Send picture
def send_picture(user_id, imageUrl, title="", subtitle=""):
    show_typing(user_id,'typing_off')    
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
    __send(data) 

# Send trending news (carousel of generic templates)
def send_carousel(user_id, elements):
    show_typing(user_id,'typing_off')    
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
    __send(data)  

def send_list(user_id, elements, header_style = 'compact'):
    show_typing(user_id,'typing_off')    
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
    __send(data) 


def __send(data):
    response = requests.post("https://graph.facebook.com/v2.6/me/messages", params = params, data = data, headers = headers)
    if response.status_code != response.ok:
        print(response.status_code)
        print(response.text)  