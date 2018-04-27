from __future__ import print_function
from googleapiclient.discovery import build
from oauth2client import client, tools
from oauth2client.file import Storage

import httplib2, os, base64, mimetypes

# send the email
def send_mail(service, user_id, message):
    try:
        message = (service.users()
                        .messages()
                        .send(userId = user_id, body = message)
                        .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)

# get the user email through the oauth2 service
def user_email(service): 
    try:
        user_info = (service.userinfo()
                            .get()
                            .execute())
        return user_info.get('email'), user_info.get('name')
    except Exception as error:
        print('An error occurred: %s', error)