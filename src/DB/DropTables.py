from src.DB.Database import Database

def drop_tables(db):
    db.query('DROP TABLE IF EXISTS clients;')
    db.query('DROP TABLE IF EXISTS sessions;')


if __name__ == "__main__":
    db = Database()
    drop_tables(db)
    db.close()