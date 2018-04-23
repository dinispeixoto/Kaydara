from watson_developer_cloud import AssistantV1
from src.Utils import Utils

import json, os

WORKSPACE_ID = os.environ['WORKSPACE_ID']
ASSISTANT = AssistantV1(
    username = os.environ['IBM_USERNAME'],
    password = os.environ['IBM_PASSWORD'],
    version = os.environ['IBM_VERSION'])

# extract all entities in the json
def extract_entities(list):
    entites = []
    for e in list:
        entites.append(e['value'])
    return entites

# send the message and return the intent, entities and the response
def send_message(message, context):
    ASSISTANT.set_http_config({'timeout': 100})
    encoded_msg = Utils.encode_msg(message)
    response = ASSISTANT.message(workspace_id = WORKSPACE_ID, input={'text': encoded_msg }, context=context)

    json_response = json.dumps(response, indent = 2)
    dict_response = json.loads(json_response)

    # intents = dict_response['intents']
    # entities = extract_entities(dict_response['entities'])
    newContext = dict_response['context']
    output = dict_response['output']['text']

    return (newContext, output, message)
