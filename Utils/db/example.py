from Database import Database

def create_tables(db):
    db.query('CREATE TABLE IF NOT EXISTS clients (' + 
             'client_id SERIAL PRIMARY KEY,' + 
             'client_context VARCHAR(1024) NOT NULL);')

def insert_client(db, id, context):
    db.query_params('INSERT INTO clients (client_id, client_context) VALUES (%s, %s)', (id, context,))

def get_client(db, id):
    db.query_params('SELECT client_context FROM clients WHERE client_id = %s', (id,))
    return db.result_set()

def destroy(db):
    db.query('DROP TABLE IF EXISTS clients;')

def populate(db):
    destroy(db)
    create_tables(db)
    insert_client(db, 1, 'context')
    rows = get_client(db, 1)

    for row in rows:
        print(row[0])
 
if __name__ == '__main__':
    db = Database()
    populate(db)
    db.close()
