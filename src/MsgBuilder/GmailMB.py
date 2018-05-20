import base64

from flask import url_for
from src.APIs import FacebookAPI
from src.Utils import Utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

# generate the login 
def generate_login(user_id):
    return [{
        "title": 'Login with Google',
        "image_url": url_for('static', filename=f'assets/img/login/login.png', _external=True),
        "subtitle": 'You have to open it in an external browser!',
        "buttons": [
            {
                'type': 'web_url',
                'url': "https://kaydara.herokuapp.com/authorize?id=" + str(user_id),
                'title': 'Log in'
            }
        ]
    }]


# generate the email
def generate_email(user_email, user_name, context):
    sender = user_email                                             
    to = context['destination']          
    subject = Utils.rm_subject(context['subject'])
    decoded_msg = Utils.decode_msg(context['emailmessage'])
    message = Utils.rm_quotes(decoded_msg) + __signature(user_name)
    info = 'To: ' + to + '\n\n' + message 
    mail = __create_mail(sender, to, subject, message)
    return (mail, subject, info)


# add a signature
def __signature(user_name):
    return '\n\nBest regards,\n' + user_name


# create an email with text only
def __create_mail(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw }