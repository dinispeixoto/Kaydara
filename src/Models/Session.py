import json, os
from src.DB.Database import Database
from src.Utils import Utils

SCOPES = Utils.gen_array(os.environ['SCOPES'])

class Session():
    def __init__(self, id, state, token, refresh_token, token_uri, client_id, client_secret):
        self.id = id
        self.state = state
        self.credentials = {
            'token': token,
            'refresh_token': refresh_token,
            'token_uri': token_uri,
            'client_id': client_id,
            'client_secret': client_secret,
            'scopes': SCOPES
        }


def insert_session(id, state, credentials):
    db = Database()
    db.query_params('INSERT INTO sessions ('+
        'facebook_id, state, token, refresh_token, '+
        'token_uri, client_id, client_secret) '+
        'VALUES(%s, %s, %s, %s, %s, %s, %s)',
        (id, state, 
        credentials.token,
        credentials.refresh_token,
        credentials.token_uri,
        credentials.client_id,
        credentials.client_secret,))
    db.close()


def get_session(id):
    db = Database()
    db.query_params('SELECT * FROM sessions WHERE facebook_id = %s', (id,))
    rs = db.result_set()
    db.close()

    if len(rs) != 0:
        session = rs[0]
        return Session(session[1], session[2], session[3], session[4], session[5], session[6], session[7])
    else:
        return None
    