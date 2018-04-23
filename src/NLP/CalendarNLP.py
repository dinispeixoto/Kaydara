import json, google.oauth2.credentials, google_auth_oauthlib.flow, googleapiclient.discovery

from src.APIs import FacebookAPI, CalendarAPI
from src.MsgBuilder import CalendarMB, GmailMB
from src.Models import Client, Session
from src.Utils import Utils


def process_message(results, cli):
    print('CALENDAR REQUEST')
    (newContext, output, message) = results

    json_newContext = json.dumps(newContext, indent=2)
    session = Session.get_session(cli.id)

    if not session:
        msg = GmailMB.generate_login(cli.id)
        FacebookAPI.send_carousel(cli.id, msg)
        Client.update_client_last_msg(cli.id, message)
    else:
        Client.update_client_context(cli.id, json_newContext)        
        for m in output:
            if m == '[OK] Process request [List]':
                list_events(newContext, cli, session)
            elif m == '[OK] Process request [Register]':
                register_events(newContext, cli, session)
            elif m != '':
                FacebookAPI.send_message(cli.id, m)


def list_events(context, cli, session):
    credentials = google.oauth2.credentials.Credentials(**session.credentials)
    Session.update_session(cli.id, credentials)
    calendar_service = __start_service('calendar', 'v3', credentials)        
    
    if context['number'] is not None:
        events = CalendarAPI.list_events(calendar_service, int(context['number'])) 
    else:
        events = CalendarAPI.list_events(calendar_service, 3)         
    elements = CalendarMB.list_events(events)
    FacebookAPI.send_carousel(cli.id, elements)  
    Client.end_context(cli.id)                 


def register_events(context, cli, session):
    credentials = google.oauth2.credentials.Credentials(**session.credentials)
    Session.update_session(cli.id, credentials)
    calendar_service = __start_service('calendar', 'v3', credentials)   
    
    event = CalendarMB.generate_event(context)
    CalendarAPI.regist_event(calendar_service, event)   
    FacebookAPI.send_message(cli.id, 'The event is registered =D')               # register the above event example
    Client.end_context(cli.id)                 


def __start_service(service, version, credentials):
    return googleapiclient.discovery.build(
        service, version, credentials=credentials)