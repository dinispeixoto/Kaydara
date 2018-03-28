import requests, json
from flask import url_for

# Sending text message
def send_message(token, user_id, text):
    params = {
        'access_token': token
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

# Show typing effect
def show_typing(token, user_id, action='typing_on'):
    params = {
        'access_token': token
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
