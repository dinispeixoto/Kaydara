from __future__ import print_function
from googleapiclient.discovery import build
from oauth2client import client, tools
from oauth2client.file import Storage

import httplib2, os, base64, mimetypes, datetime

# list the N next events 
# TODO must be generic 
def list_events(service, num_events):
    now = datetime.datetime.utcnow().isoformat() + 'Z'                          # 'Z' indicates UTC time
    eventsResult = (service.events()
                           .list(calendarId='primary',                          # is the primary calendar defined in Google Calendar, but can be the email 
                                 timeMin=now,                                   # since...
                                 orderBy='startTime',                           # order list
                                 singleEvents=True,
                                 maxResults=num_events)                         # get the "num_events" next events
                           .execute())                                        
    events = eventsResult.get('items', [])
    return events


# regist a new event in Calendar 
def regist_event(service, event):
    eventResult = (service.events()
                          .insert(calendarId='primary', body=event)             # is the primary calendar defined in Google Calendar, but can be the email 
                          .execute()) 
    return eventResult['id']
                    
                                           
