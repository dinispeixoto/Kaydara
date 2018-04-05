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