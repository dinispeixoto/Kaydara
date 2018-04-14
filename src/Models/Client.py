import json
from src.DB.Database import Database

class Client():
    def __init__(self, id, context):
        self.id = id
        self.context = context


def insert_client(id, context):
    db = Database()
    db.query_params('INSERT INTO clients (facebook_id, client_context) VALUES (%s, %s)', (id, context,))
    db.close()
    return Client(id, context)


def update_client_context(id, context):
    db = Database()
    db.query_params('UPDATE clients SET client_context = %s WHERE facebook_id = %s', (context, id,))
    db.close()


def get_client(id):
    db = Database()
    db.query_params('SELECT client_context FROM clients WHERE facebook_id = %s', (id,))
    rs = db.result_set()
    db.close()
    
    if len(rs) != 0:
        if rs[0][0] is None:
            return Client(id, None)
        else:
            return Client(id, json.loads(rs[0][0]))
    else:
        return None