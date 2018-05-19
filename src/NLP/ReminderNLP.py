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
            if context['flag'] == 'schedule':
                FacebookAPI.send_message(cli.id, f'I received your request to remind you {word} {description}{ReminderMB.getDatetimeDescription(datetime)}.')
            elif context['flag'] == 'reschedule':
                FacebookAPI.send_message(cli.id, f'I\'ll remind you {word} {description}{ReminderMB.getDatetimeDescription(datetime)} then.')
            Client.update_client_context(cli.id, None)
            cli.context = None

        elif m != '':
            FacebookAPI.send_message(cli.id, m)

def send_reminder(cli, word, description):
    new_context = {'word': word, 'description': description}
    json_context = json.dumps(new_context, indent=2)
    Client.update_client_context(cli, json_context)
    print(json_context)
    FacebookAPI.send_quick_replies(cli, ReminderMB.reminder_quick_replies(), ReminderMB.getDescription(word, description))
