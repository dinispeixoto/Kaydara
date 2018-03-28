import os, sys, traceback, json, argparse, requests

from datetime import datetime
from Utils import FacebookAPI as FB
from flask import Flask, request


app = Flask(__name__)

@app.route('/', methods=['GET'])
# Handling webhook's verification: checking hub.verify_token and returning received hub.challenge
def handle_verification():
    print('Handling Verification.')
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):  
        if request.args.get('hub.verify_token') == os.environ['VERIFY_TOKEN']:
            print('Webhook verified.')
            return request.args.get('hub.challenge'), 200
        else:
            print('Wrong verification token!'), 403
    return 'Kaydara is working.', 200


@app.route('/', methods=['POST'])
# Handling received messages
def handle_messages():
    payload = request.get_data()
    token = os.environ['PAGE_ACCESS_TOKEN']
    webhook_type = get_type_from_payload(payload)

    # Handle messages
    if webhook_type == 'message':
        for sender_id, message in messaging_events(payload):
            # Only process message in here
            if not message:
                return 'ok'

            # Start processing valid requests
            try:
                FB.show_typing(token, sender_id)
                response = processIncoming(sender_id, message)
                FB.show_typing(token, sender_id, 'typing_off')

                print('RESPONSE: ' + str(response))
                FB.send_message(token, sender_id, response)

            except Exception as e:
                print('EXCEPTION ' + str(e))
                traceback.print_exc()
                #FB.send_message(os.environ['PAGE_ACCESS_TOKEN'], sender_id, NLP.oneOf(NLP.error))
    return 'ok'

def processIncoming(user_id, message):

    # Text message
    if message['type'] == 'text':
        message_text = message['data']
        return message_text

    # Location message type 
    elif message['type'] == 'location':
        response = "I've received location (%s,%s) (y)"%(message['data'][0],message['data'][1])
        return response

    # Image message type 
    elif message['type'] == 'image':
        image_url = message['data']
        return "I've received your image: %s"%(image_url)

    # Audio message type 
    elif message['type'] == 'audio':
        audio_url = message['data']
        return "I've received your audio: %s"%(audio_url)

    # Video message type
    elif message['type'] == 'video':
        video_url = message['data']
        return "I've received your video: %s"%(video_url)  

    # File message type
    elif message['type'] == 'file':
        file_url = message['data']
        return "I've received your file: %s"%(file_url)      


    # Unrecognizable incoming 
    else:
        return "*scratch my head*"

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
                coordinates = event['message']['attachments'][
                    0]['payload']['coordinates']
                latitude = coordinates['lat']
                longitude = coordinates['long']

                yield sender_id, {'type':'location','data':[latitude, longitude],'message_id': event['message']['mid']}

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
#def postback_events(payload):
#    data = json.loads(payload)
    
#    postbacks = data["entry"][0]["messaging"]
    
#    for event in postbacks:
#        sender_id = event["sender"]["id"]
#        postback_payload = event["postback"]["payload"]
#        yield sender_id, postback_payload

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
    