from __future__ import print_function
import httplib2
import os
import base64
import mimetypes

from googleapiclient.discovery import build
from oauth2client import client, tools
from oauth2client.file import Storage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/userinfo.email'
    ]
CLIENT_SECRET_FILE = 'resources/client_secret.json'
APPLICATION_NAME = 'Kaydara'

# get the credentials to call the APIs
# in ~/.credentials is stored a token 
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, ' '.join(SCOPES))
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

# create an email with text only
def create_mail(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw }

# send the email
def send_mail(service, user_id, message):
    try:
        message = (service.users()
                        .messages()
                        .send(userId = user_id, body = message)
                        .execute())
        print('Message Id: %s' % message['id'])
        return message
    except error.HttpError as error:
        print('An error occurred: %s' % error)

# get the user email through the oauth2 service
def user_email(service): 
    try:
        user_info = (service.userinfo()
                            .get()
                            .execute())
        return user_info.get('email')
    except error.HttpError as error:
        print('An error occurred: %s', error)

"""
def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    
    # get user info (email)
    service_oauth = build('oauth2', 'v2', http=http)
    user_mail = user_email(service_oauth)
    
    # create an email and send it
    sender = user_mail
    to = '...'                      # destination email
    subject = 'teste'
    message = 'Ola :)'
    msg = create_mail(sender, to, subject, message)
    
    service_gmail = build('gmail', 'v1', http=http)
    send_mail(service_gmail, 'me' ,msg)

if __name__ == '__main__':
    main()
"""