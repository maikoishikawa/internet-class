from flask import request, jsonify
import sqlite3
import json
import datetime
from . import db

def send_new():
    '''API to send a new message by the caller'''
    data = json.loads(request.data)
    ip = request.remote_addr
    hostname = data.get('sender', 'unknown')
    arrival = datetime.datetime.now()
    body = data.get('body', '')

    con = db.get_db()
    cur = con.cursor()
    cur.execute(
        'insert into msg (ip, hostname, arrival, body) values (?, ?, ?, ?)',
        (ip, hostname, arrival, body))
    rowid = cur.lastrowid
    con.commit()

    response = {'id': rowid, 'echo': body}
    return jsonify(response)

def get_messages():
    '''API to return all messages'''
    return jsonify(get_messages())

def get_last100_messages():
    '''Internal method to retrieve last 100 messages.'''
    return db.get_db().execute(
        'select ip, hostname, body'
        ' from msg'
        ' order by arrival desc limit 100'
    ).fetchall()
