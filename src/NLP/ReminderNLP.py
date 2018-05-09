from src.APIs import FacebookAPI, SchedulerAPI
from src.Models import Client
from src.MsgBuilder import ReminderMB
from datetime import datetime, timedelta

import json

def process_message(results, cli):
    print('REMINDER REQUEST')
    (context, output, _) = results

    json_context = json.dumps(context, indent=2)
    Client.update_client_context(cli.id, json_context)
    
    for m in output:
        if m == '[OK] Process request':
            datetime = f"{context['date']} {context['time']}"
            word = context['word']
            description = context['description']
            print(datetime)
            
            SchedulerAPI.schedule_remind(datetime, cli.id, word, description)
            FacebookAPI.send_message(cli.id, f'I received your request to remind you {word} {description} at {datetime}.')
            Client.update_client_context(cli.id, None)
            cli.context = None
        elif m != '':
            FacebookAPI.send_message(cli.id, m)        

def send_reminder(cli, word, description):
    FacebookAPI.send_message(cli, ReminderMB.getDescription(word, description))
