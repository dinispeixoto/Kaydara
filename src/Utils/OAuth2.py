import os
import httplib2

from googleapiclient.discovery import build
from oauth2client import client, tools
from oauth2client.file import Storage

# only for tests
from src.APIs import GmailAPI
from src.APIs import CalendarAPI
import Utils

SCOPES = Utils.gen_array(os.environ['GOOGLE_SCOPES'])
CLIENT_SECRET_FILE = os.environ['CLIENT_SECRET_FILE']
APPLICATION_NAME = os.environ['APPLICATION_NAME']

class OAuth2:
    def __init__(self):
        self.__credentials = None
        self.__http = None
            
    # extract some flags
    def __get_flags(self):
        try:
            import argparse
            return argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            return  None   

    # get the credentials to call the APIs
    # in ~/.credentials is stored a token 
    def __get_credentials(self):
        flags = self.__get_flags()

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'gmail-python.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            print(' '.join(SCOPES))
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, ' '.join(SCOPES))
            flow.user_agent = APPLICATION_NAME
            print('Flags: ' + str(flags))
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials
    
    # start new service  
    def start_service(self, service, version):
        if(self.__credentials == None):
            self.__credentials = self.__get_credentials()
            self.__http = self.__credentials.authorize(httplib2.Http())

        return build(service, version, http=self.__http)

"""
# example where explains how use two google APIs
if __name__ == '__main__':
    oauth = OAuth2()                                                # only one instance of OAuth2

    # User information
    user_info_service = oauth.start_service('oauth2', 'v2')
    user_email = GmailAPI.user_email(user_info_service)             # get user email
    
    # Gmail example
    gmail_service = oauth.start_service('gmail', 'v1')
    
    sender = user_email                                             # own email
    to = '...' # TODO                                               # destination email 
    subject = 'teste'   
    message = 'Ola :)'
    msg = GmailAPI.create_mail(sender, to, subject, message)
    
    # GmailAPI.send_mail(gmail_service, 'me', msg)

    # Calendar example
    calendar_service = oauth.start_service('calendar', 'v3')        
    CalendarAPI.list_events(calendar_service, 3)                    # list the 3 next events
    
    event = {
        'summary': 'Testing API',
        'location': 'Braga',
        'start': {
            'dateTime': '2018-04-04T10:00:00.000-07:00',
            'timeZone': 'America/Los_Angeles'
        },
        'end': {
            'dateTime': '2018-04-05T10:25:00.000-07:00',
            'timeZone': 'America/Los_Angeles'
        }
    }
    CalendarAPI.regist_event(calendar_service, event)               # register the above event example
    
    print('Works.')
"""
