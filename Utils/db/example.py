import json
from Utils.db.Database import Database


class Client():
    def __init__(self, id, context):
        self.id = id
        self.context = context


def create_tables():
    db.query('CREATE TABLE IF NOT EXISTS clients (' +
             'client_id SERIAL PRIMARY KEY,' +
             'facebook_id BIGINT NOT NULL,' +
             'client_context VARCHAR(1024));')
    db.close()


def insert_client(id, context):
    db = Database()
    db.query_params('INSERT INTO clients (facebook_id, client_context) VALUES (%s, %s)', (id, context,))
    db.close()


def update_client_context(id, context):
    db = Database()
    db.query_params('UPDATE clients SET client_context = %s WHERE facebook_id = %s', (context, id,))
    db.close()


def get_client(id):
    db = Database()
    db.query_params('SELECT client_context FROM clients WHERE facebook_id = %s', (id,))
    rs = db.result_set()
    db.close()
    print(rs)
    if len(rs) != 0:
        print("EXISTE")
        if rs[0][0] is None:
            return Client(id, None)
        else:
            return Client(id, json.loads(rs[0][0]))
    else:
        print("NAO EXISTE")
        return None


def destroy():
    db = Database()
    db.query('DROP TABLE IF EXISTS clients;')
    db.close()


def populate():
    db = Database()
    destroy(db)
    create_tables(db)
    insert_client(db, 1, 'context')
    rows = get_client(db, 1)

    for row in rows:
        print(row[0])
    db.close()
