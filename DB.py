#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/bank.py
# A small library of database routines to power a payments application.

import os, pprint, sqlite3
from collections import namedtuple

def open_database(path='user.db'):
    new = not os.path.exists(path)
    db = sqlite3.connect(path)
    if new:
        c = db.cursor()
        #Create account table
        c.execute('CREATE TABLE user (id INTEGER PRIMARY KEY, account VARCHAR, password VARCHAR, '
                  'name VARCHAR, createOn DATETIME);')
        #Create record table
        c.execute('CREATE TABLE record (id INTEGER PRIMARY KEY, account VARCHAR, '
                  'roundCost INTEGER, timeCost INTEGER, time DATETIME, message TEXT);')

        create_account(db, 'TH', '123', 'T.H. Liu', '2015-06-27 17:56:00')
        create_account(db, 'Nick', '321', 'Nick Liang', '2015-06-26 17:56:00')
        create_record (db, 'TH', 4, 3600, '2015-06-27 17:57:00', 'I am funcking genius!!')
        create_record (db, 'TH', 10, 2600, '2015-06-26 17:57:00', 'Use brute force')
        create_record (db, 'Nick', 5, 4600, '2015-06-25 17:57:00', 'OK')
        create_record (db, 'Nick', 7, 8600, '2015-06-27 17:00:00', 'bitch!')
        db.commit()
    return db

def create_account(db, account, password, name, createOn):
    db.cursor().execute('INSERT INTO user (account, password, name, createOn)'
                        ' VALUES (?, ?, ?, ?)', (account, password, name, createOn))
   
def create_record (db, account, roundCost, timeCost, time, message):
    db.cursor().execute('INSERT INTO record (account, roundCost, timeCost, time, message)'
                        ' VALUES (?, ?, ?, ?, ?)', (account, roundCost, timeCost, time, message))

def getUserInfo (db, account):
    c = db.cursor()
    c.execute('SELECT * FROM user WHERE account= "'+ account +'"')
    userInfo = c.fetchone()
    return userInfo

def getCharts (db, orderBy): #order = roundCost/timeCost
    c = db.cursor()
    if orderBy == "timeCost":
        c.execute('SELECT user.account, user.name, record.roundCost, record.timeCost, record.time, record.message '
                  'FROM user, record WHERE record.account=user.account ORDER BY record.timeCost')
    else:
        c.execute('SELECT user.account, user.name, record.roundCost, record.timeCost, record.time, record.message '
                  'FROM user, record WHERE record.account=user.account ORDER BY record.roundCost')
    #return #c.fetchall()
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    return [Row(*row) for row in c.fetchall()]
def getCount (db):
    c = db.cursor()
    c.execute('SELECT count(*) AS count FROM user')
    data = c.fetchone()
    return data
def userRecord (db, account):
    c = db.cursor()
    c.execute('SELECT user.account, user.name, record.roundCost, record.timeCost, record.time, record.message '
              'FROM user, record WHERE record.account=user.account AND user.account="' + account + '" '
              'ORDER BY record.time DESC')
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    return [Row(*row) for row in c.fetchall()]
    
if __name__ == '__main__':
    db = open_database()
    create_account(db, 'TH', '123', 'T.H. Liu', '2015-06-27 17:56:00')
    create_account(db, 'Nick', '321', 'Nick Liang', '2015-06-26 17:56:00')
    create_record (db, 'TH', 4, 3600, '2015-06-27 17:57:00', 'I am funcking genius!!')
    create_record (db, 'TH', 10, 2600, '2015-06-26 17:57:00', 'Use brute force')
    create_record (db, 'Nick', 5, 4600, '2015-06-25 17:57:00', 'OK')
    create_record (db, 'Nick', 7, 8600, '2015-06-27 17:00:00', 'bitch!')  
    pprint.pprint(getCharts (db, 'roundCost'))
    pprint.pprint(userRecord (db, 'TH'))
