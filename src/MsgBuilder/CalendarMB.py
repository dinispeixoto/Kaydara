from flask import url_for
from src.Utils import Utils

# extract events from json 
def list_events(events_json):
    events_list = []
    for event in events_json:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        end_time = event['end'].get('dateTime', event['start'].get('date'))
        print(event)
        event_json = {
            'title': event['summary'],
            'image_url': url_for('static', filename=f'assets/img/calendar/goo.png', _external=True),
            'subtitle': 'Start: ' + Utils.parse_date(start_time) + '\nEnd: ' + Utils.parse_date(end_time),
            "buttons": [
                {
                    'type': 'web_url',
                    'url': event['htmlLink'],
                    'title': 'Go to the event'
                }
            ]
        }
        events_list.append(event_json)
    return events_list

# generate an event
def generate_event(context):
    return {
        'summary': context['summary'],
        'start': {
            'dateTime': context['date'] + 'T' + context['startTime'] + '+01:00',
        },
        'end': {
            'dateTime': context['date'] + 'T' + context['endTime'] + '+01:00',
        }
    }
    

