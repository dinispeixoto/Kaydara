import os
import urllib.parse as urlparse


def config(filename='database.ini', section='postgresql'):
    db = {}

    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    db['database'] = url.path[1:]
    db['user'] = url.username
    db['password'] = url.password
    db['host'] = url.hostname
    db['port'] = url.port

    return db
