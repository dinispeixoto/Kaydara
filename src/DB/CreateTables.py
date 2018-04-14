from src.DB.Database import Database

def create_tables(db):
    db.query('CREATE TABLE IF NOT EXISTS clients (' + 
             'client_id SERIAL PRIMARY KEY, ' +
             'facebook_id BIGINT NOT NULL, ' + 
             'client_context VARCHAR(1024));')

    db.query('CREATE TABLE IF NOT EXISTS sessions (' +
             'id SERIAL PRIMARY KEY, '
             'facebook_id BIGINT NOT NULL, ' +
             'state VARCHAR(512) NOT NULL, ' +
             'token VARCHAR(512), ' +
             'refresh_token VARCHAR(512), ' + 
             'token_uri VARCHAR(512), ' +
             'client_id VARCHAR(512), ' +
             'client_secret VARCHAR(512));')


if __name__ == "__main__":
    db = Database()
    create_tables(db)
    db.close()