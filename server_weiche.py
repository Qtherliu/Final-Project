#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_improved.py
# A payments application with basic security improvements added.

import DB, uuid, pprint
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for, jsonify)

app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'

@app.route('/login', methods=['GET', 'POST'])
def login():
    account = request.form.get('account', '')
    password = request.form.get('password', '')
    Msg = 'Welcome to 1A2B game filed.<br>Please log in to start a game.' #you can put error message here
    if request.method == 'POST': #push login button
        db = DB.open_database()
        userInfo = DB.getUserInfo(db, account)
        pprint.pprint(userInfo)
        if password == userInfo[2]:
            session['username'] = userInfo[3]
            session['account'] = userInfo[1]
            session['csrf_token'] = uuid.uuid4().hex
            return redirect(url_for('index'))
        else:
            Msg = 'Please check your account/password'
    return render_template('login.html', account=account, msg=Msg)

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
    account = session.get('account')
    if not orderBy:
        orderBy = "roundCost"
    chartsData=DB.getCharts(DB.open_database(), orderBy)
    return render_template('index.html', chartsData=chartsData, account=account, username=username, orderBy=orderBy)

@app.route('/challenge', methods=['GET', 'POST'])
def challenge():
    username = session.get('username')
    account = session.get('account')
    if not username:
        return redirect(url_for('login'))

    msg = ''
    if request.method == 'POST': #Game over, send you the game result
        msg=request.form.get('GUESS','').strip()
        # your code	
    else:
        msg = 'Start your game!'
    return render_template('challenge.html', msg=msg, account=account)

@app.route('/beatComputer', methods=['GET', 'POST'])
def beatComputer():
    username = session.get('username')
    account = session.get('account')
    if not username:
        return redirect(url_for('login'))
    
    db = DB.open_database()
    if request.method == 'POST': #Game start, user send you the number
        msg=request.form.get('send','').strip()
        # your code
	
    else:
        msg = 'If computer take more than 3 round, you win!'
    return render_template('beatComputer.html', msg=msg, account=account)

@app.route('/userInfo/<account>', methods=['GET'])
def userRecord(account):
    username = session.get('username')
    account = session.get('account')

    if not username:
        return redirect(url_for('login'))
    userRecord=DB.userRecord(DB.open_database(),account)
    # your code
    return render_template('userInfo.html', userRecord=userRecord, username=username, account=account)

if __name__ == '__main__':
    app.debug = True
    app.run()
