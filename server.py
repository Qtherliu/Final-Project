#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_improved.py
# A payments application with basic security improvements added.

import DB, uuid
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    Msg = 'Welcome to 1A2B game filed.<br>Please log in to start a game.' #you can put error message here
    if request.method == 'POST': #push login button
        #if OK:
        #   {add username,account into session}
        #   return redirect(url_for('index'))
        #else: Mes='error!'
    return render_template('login.html', username=username, msg=Msg)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
def index():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    ### Show charts
    orderBy = request.args.get('orderBy') #user GET form to tell you how to order the charts
    # your code
    return render_template('index.html', chartsData=chartsData, account=account, username=username, orderBy=orderBy)

@app.route('/challenge', methods=['GET', 'POST'])
def challenge():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    msg = ''
    if request.method == 'POST': #Game over, send you the game result
        # your code
    else:
        msg = 'Start your game!'
    return render_template('challenge.html', msg=msg, account=account)

@app.route('/beatComputer', methods=['GET', 'POST'])
def beatComputer(data_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    db = DB.open_database()
    if request.method == 'POST': #Game start, user send you the number
        # your code
    else:
        msg = 'If computer take more than 3 round, you win!'
    return render_template('beatComputer.html', msg=msg)

@app.route('/userInfo/<account>', methods=['GET'])
def userRecord(account):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    # your code
    return render_template('challenge.html', userRecord=userRecord, username=username)

if __name__ == '__main__':
    app.debug = True
    app.run()
