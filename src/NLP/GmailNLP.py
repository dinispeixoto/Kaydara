from flask import session
from src.APIs import FacebookAPI, GmailAPI
from src.MsgBuilder import GmailMB
from src.Models import Client
from src.Utils import Utils
from src.Models import Session

import json
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery


def process_message(results, cli):
    print('EMAIL REQUEST')
    (intents, entities, newContext, output) = results

    json_newContext = json.dumps(newContext, indent=2)
    Client.update_client_context(cli.id, json_newContext)
    session = Session.get_session(cli.id)

    if not session:
        msg = GmailMB.generate_login(cli.id)
        FacebookAPI.send_carousel(cli.id, msg)
    else: 
        for m in output:
            if m == '[OK] Process request':
                send_mail(newContext, cli, session)
            elif m != '':
                FacebookAPI.send_message(cli.id, m)


def send_mail(context, cli, session):
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session.credentials)

    user_info_service = __start_service('oauth2', 'v2', credentials)
    user_email, user_name = GmailAPI.user_email(user_info_service)             # get user email

    gmail_service = __start_service('gmail', 'v1', credentials)
    msg = GmailMB.generate_email(user_email, user_name, context)

    GmailAPI.send_mail(gmail_service, 'me', msg)
    FacebookAPI.send_message(cli.id, 'E-mail sent :)')
    Client.update_client_context(cli.id, None)


def __start_service(service, version, credentials):
    return googleapiclient.discovery.build(
        service, version, credentials=credentials)