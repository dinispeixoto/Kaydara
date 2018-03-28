import requests, json, os
from flask import url_for

# Environment varibles on heroku
#VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
#PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']

# JUST FOR DEBUG PURPOSES
VERIFY_TOKEN = 'TESTINGTOKEN'
PAGE_ACCESS_TOKEN = 'EAAEauAoeQ1cBAMaDSOs9uC9VMNIJLdH7l3lQ2LZAjc8VA83mIJL6IXvBmFJGfEVZBQZA7Y1FeVOGRDfa7iBuwiTGUWxITUo49mZA53nbvRLpCQ2akmjI4PuLHNErrq2mWkw9etNFA4q7BvAqjU7P6L5ITnQz62samm4VofvZCvwZDZD'

# Show typing effect
def show_typing(user_id, action='typing_on'):
    params = {
        'access_token': PAGE_ACCESS_TOKEN
    }
    data = json.dumps({
        'recipient': {'id': user_id},
        'sender_action': action
    })
    headers = {
        'Content-type': 'application/json'
    }
    r = requests.post('https://graph.facebook.com/v2.6/me/messages', params = params, headers = headers, data = data)
    if r.status_code != requests.codes.ok:
        print(r.status_code + ': ' + r.text)

# Sending text message
def send_message(user_id, text):
    params = {
        'access_token': PAGE_ACCESS_TOKEN
    }
    data = json.dumps({
        'recipient': {'id': user_id},
        'message': {'text': text}
    })
    headers = {
        'Content-type': 'application/json'
    }
    r = requests.post('https://graph.facebook.com/v2.6/me/messages', params = params, headers = headers, data = data)
    if r.status_code != requests.codes.ok: # != 200
        print(r.status_code + ': ' + r.text)

# Sending picture
def send_picture(user_id, imageUrl, title="", subtitle=""):
    if title != "":
        data = {"recipient": {"id": user_id},
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
              }
    else:
        data = { "recipient": {"id": user_id},
                "message":{
                  "attachment": {
                      "type": "image",
                      "payload": {
                          "url": imageUrl
                      }
                  }
                }
            }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params = {"access_token": PAGE_ACCESS_TOKEN}, data = json.dumps(data), headers = {'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.status_code + ': ' + r.text)   