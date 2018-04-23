from src.DB.Database import Database

import json

class Client():
    def __init__(self, id, context, last_msg):
        self.id = id
        self.context = context
        self.last_msg = last_msg


def insert_client(id, context):
    db = Database()
    db.query_params('INSERT INTO clients (facebook_id, client_context) VALUES (%s, %s)', (id, context,))
    db.close()
    return Client(id, context, None)


def update_client_context(id, context):
    db = Database()
    db.query_params('UPDATE clients SET client_context = %s WHERE facebook_id = %s', (context, id,))
    db.close()

def update_client_last_msg(id, msg):
    db = Database()
    db.query_params('UPDATE clients SET last_message = %s WHERE facebook_id = %s', (msg, id,))
    db.close()

def end_context(id):
    db = Database()
    db.query_params('UPDATE clients SET client_context = NULL WHERE facebook_id = %s', (id,))
    db.close()

def get_client(id):
    db = Database()
    db.query_params('SELECT client_context, last_message FROM clients WHERE facebook_id = %s', (id,))
    rs = db.result_set()
    db.close()
    
    if len(rs) != 0:
        if rs[0][0] is None:
            return Client(id, None, None)
        else:
            return Client(id, json.loads(rs[0][0]), rs[0][1])
    else:
        return None