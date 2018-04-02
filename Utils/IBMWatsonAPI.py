from watson_developer_cloud import AssistantV1
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
def send_message(message,context):
    ASSISTANT.set_http_config({'timeout': 100})
    response = ASSISTANT.message(workspace_id = WORKSPACE_ID, input={'text': message }, context=context)

    json_response = json.dumps(response, indent = 2)
    dict_response = json.loads(json_response)

    intents = dict_response['intents']
    entities = extract_entities(dict_response['entities'])
    newContext = dict_response[u'context']
    output = dict_response['output']['text']

    return (intents, entities, newContext, output)

"""
if __name__ == '__main__':
    (intent, entities, output) = send_message('hi Ricardo')
    print(intent)
    print(entities)
    print(output)
"""
