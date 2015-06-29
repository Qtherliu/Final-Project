#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_improved.py
# A payments application with basic security improvements added.

import DB, uuid, pprint
from time import gmtime, strftime
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for, jsonify)
import random

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
    chartsData = DB.getCharts(DB.open_database(), orderBy)
    UsersData = DB.getUserList(DB.open_database())
    return render_template('index.html', chartsData=chartsData, UsersData=UsersData
                           , account=account, username=username, orderBy=orderBy)

@app.route('/createAccount', methods=['POST'])
def createAccount():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        account = request.form.get('account', '').strip()
        password = request.form.get('password', '').strip()
        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        db = DB.open_database()
        DB.create_account(db, account, password, username, curTime)
        db.commit()
        session['username'] = username
        session['account'] = account
        return redirect(url_for('index'))

@app.route('/challenge', methods=['GET', 'POST'])
def challenge():
    username = session.get('username')
    account = session.get('account')
    if not username:
        return redirect(url_for('login'))

    msg = ''
    if request.method == 'POST': #Game over, send you the game result
        roundCost = request.form.get('roundCost','').strip()
        timeCost = request.form.get('timeCost','').strip()
        message = request.form.get('message','').strip()
        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        db = DB.open_database()
        DB.create_record(db, account, roundCost, timeCost, curTime, message)
        db.commit()
        return redirect(url_for('index'))
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
    msg = 'If computer take more than 3 round, you win!'
    if request.method == 'POST': #Game start, user send you the number
        userNum = request.form.get('userNum','').strip()
        ans=int(userNum,10)
        ans_a=int(ans/1000)
        ans_b=int((ans%1000)/100)
        ans_c=int(((ans%1000)%100)/10)
        ans_d=int(((ans%1000)%100)%10)
        ans_tuple=ans_a,ans_b,ans_c,ans_d
        cnt=0
        flag=0
        record=[]
        while cnt<=2 :
            guess_a=random.randrange(1,9)
            while True:
                guess_b=random.randrange(0,9)
                if guess_b!=guess_a:
                    break
            while True:
                guess_c=random.randrange(0,9)
                if guess_c != guess_a and guess_c != guess_a:
                    break
            while True:    
                guess_d=random.randrange(0,9)
                if guess_d!=guess_a and guess_d != guess_b and guess_d != guess_c:
                    break
            cnt_A=0
            cnt_B=0
            guess_tuple=guess_a,guess_b,guess_c,guess_d
            guess=guess_a*1000+guess_b*100+guess_c*10+guess_d
            cnt+=1
            if ans_a==guess_a and ans_b==guess_b and ans_c==guess_c and ans_d==guess_d :
                flag=1
                record=record+(guess,'4A0B')
                break
            else:
                if guess_a==ans_a:
                    cnt_A+=1
                if guess_b==ans_b:
                    cnt_A+=1
                if guess_c==ans_c:
                    cnt_A+=1
                if guess_d==ans_d:
                    cnt_A+=1
                pprint.pprint(ans_tuple[0])
                for i in range(0,4,1):
                    for j in range(0,4,1):
                        if guess_tuple[i]==ans_tuple[j] and i != j:
                            cnt_B+=1
                tmp=str(cnt_A)+'A'+str(cnt_B)+'B'
                b=(guess,tmp)
                record.append(b)
        pprint.pprint(record)
        return render_template('beatComputer.html', msg=msg, account=account, data=record, count=len(record) )
    else:
        return render_template('beatComputer.html', msg=msg, account=account, count=0)

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
