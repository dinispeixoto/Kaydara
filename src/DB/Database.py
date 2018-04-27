from src.DB import Config

import psycopg2

class Database():
    def __init__(self):
        try:
            params = Config.config()
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)

    def query_params(self, query, params):
        return self.cur.execute(query, params)

    def result_set(self):
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()
