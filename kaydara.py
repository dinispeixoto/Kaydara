from src.APIs import FacebookAPI, OpenWeatherMapAPI, NewsAPI, SchedulerAPI
from src.NLP import NLP, Multimedia
from src.Utils import Utils
from flask import Flask, request, session, url_for, redirect 
from src.Models import Session, Client

import traceback, json, argparse, os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

SCOPES = Utils.gen_array(os.environ['SCOPES'])
CLIENT_SECRET_FILE = os.environ['CLIENT_SECRET_FILE']
SchedulerAPI.init_scheduler()

# Handling webhook's verification: checking hub.verify_token and returning received hub.challenge
@app.route('/', methods=['GET'])
def handle_verification():
    print('Handling Verification.')
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if request.args.get('hub.verify_token') == FacebookAPI.VERIFY_TOKEN:
            print('Webhook verified.')
            return request.args.get('hub.challenge'), 200
        else:
            return 'Wrong verification token!', 403
    return 'Kaydara is working.', 200


# Handling received messages
@app.route('/', methods=['POST'])
def handle_messages():
    payload = request.get_data()
    webhook_type = get_type_from_payload(payload)

    # Handle messages
    if webhook_type == 'message':
        for sender_id, message in messaging_events(payload):
            # Only process message in here
            if not message:
                return 'ok'

            print(f'Received : {json.dumps(message, indent=4)}')
            # Start processing valid requests
            try:
                FacebookAPI.show_typing(sender_id)
                if message['type'] == 'text':
                    NLP.process_message(sender_id, message['data'])
                elif message['type'] == 'quick_reply':
                    NLP.process_quick_reply(sender_id, message['data'])
                else:
                    Multimedia.process_message(sender_id, message)
                
            except Exception as e:
                print('EXCEPTION ' + str(e))
                traceback.print_exc()

    return 'ok'


# Handling the requests for authorisation 
@app.route('/authorize')
def authorize():
    payload = request.args
    client_id = payload.get('id')
    
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state
    session['client_id'] = client_id

    return redirect(authorization_url)


# Handling the OAuth2 credentials 
@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    client_id = session['client_id']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    Session.insert_session(client_id, state, credentials)

    FacebookAPI.send_message(client_id, 'You\'re logged in! 😁')
    cli = Client.get_client(client_id)
    NLP.process_message(client_id, cli.last_msg)

    return '<h1>Login succeeded.</h1><br><h3>Back to the Messenger!</h3>', 200


# Generate tuples of (sender_id, message_text) from the provided payload.
# This part technically clean up received data to pass only meaningful data to processIncoming() function
def messaging_events(payload):
    data = json.loads(payload)
    messaging_events = data['entry'][0]['messaging']

    for event in messaging_events:
        sender_id = event['sender']['id']

        # Not a message
        if 'message' not in event:
            yield sender_id, None

        # Text message
        if 'message' in event and 'text' in event['message'] and 'quick_reply' not in event['message']:
            data = event['message']['text']
            yield sender_id, {'type':'text', 'data': data, 'message_id': event['message']['mid']}

        # Attachments
        elif 'attachments' in event['message']:

            # Location
            if 'location' == event['message']['attachments'][0]['type']:
                coordinates = event['message']['attachments'][0]['payload']['coordinates']
                yield sender_id, {'type':'location','data': coordinates,'message_id': event['message']['mid']}

            # Audio, Video, Image or File
            elif event['message']['attachments'][0]['type'] in ('audio', 'video', 'image', 'file'):
                url = event['message']['attachments'][0]['payload']['url']
                yield sender_id, {'type': event['message']['attachments'][0]['type'], 'data': url, 'message_id': event['message']['mid']}

            else:
                yield sender_id, {'type':'text','data':"I don't understand this [Attachment not verified]", 'message_id': event['message']['mid']}

        # Quick_reply
        elif 'quick_reply' in event['message']:
            data = event['message']['quick_reply']['payload']
            yield sender_id, {'type':'quick_reply','data': data, 'message_id': event['message']['mid']}

        else:
            yield sender_id, {'type':'text','data':"I don't understand this! [Not verified]", 'message_id': event['message']['mid']}


# Not used yet
def postback_events(payload):
    data = json.loads(payload)

    postbacks = data["entry"][0]["messaging"]

    for event in postbacks:
        sender_id = event["sender"]["id"]
        postback_payload = event["postback"]["payload"]
        yield sender_id, postback_payload


# Returning payloads' type - currently only supporting 'message'
def get_type_from_payload(payload):
    data = json.loads(payload)
    if 'message' in data['entry'][0]['messaging'][0]:
        return 'message'
    if 'postback' in data['entry'][0]['messaging'][0]:
        return 'postback'


# Allows running with simple `python kaydara <port>`
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'kaydara')
    parser.add_argument('-p','--port', help = 'running on customized port', type = int, default = 5000)
    args = parser.parse_args()

    app.run(port = args.port)

