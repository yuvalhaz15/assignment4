from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector
import time
import requests

import asyncio
import aiohttp
app = Flask(__name__)
app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)


@app.route('/')
def first_page():  # put application's code here
    return redirect(url_for('display_home_page'))


@app.route('/home')
def display_home_page():  # put application's code here
    return render_template('homePage.html')


@app.route('/conact')
def display_conact_us():  # put application's code here
    return render_template('conactUs.html')


@app.route('/assignment3_1')
def display_hobbies_page():
    my_hobbies = ('swimming', 'crossfit', 'playing music')
    return render_template('assignment3_1.html',
                           hobbies_dic=my_hobbies,
                           no_hobbies_message='no hobbies to display')




users = {
    "user1": {"name": "Edinson", "email": "Cavani@gmail.com", "user_name": "El matador"},
    "user2": {"name": "Cristiano", "email": "CR7@gmail.com", "user_name": "CR7"},
    "user3": {"name": "Bruno", "email": "Bruno@gmail.com", "user_name": "BR"},
    "user4": {"name": "Messi", "email": "Messi@gmail.com", "user_name": "The flea"},
    "user5": {"name": "Kobe", "email": "kobe@gmail.com", "user_name": "The black mamba"}
}
user_data = {
    'El matador': '1234',
    'CR7': '1235',
    'BR': '1236',
    'The flea': '1237',
    'The black mamba': '1238',
}


@app.route('/assignment3_2', methods=['GET', 'POST'])
def display_users_page():  # put application's code here
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        if user_name in user_data:
            user_password = user_data[user_name]
            if user_password == password:
                session['user_name'] = user_name
                session['loged_in'] = True
                return render_template('assignment3_2.html',
                                       message='Hello',
                                       user_name=user_name)
            else:
                return render_template('assignment3_2.html',
                                       message='Incorrect password!')
        else:
            return render_template('assignment3_2.html',
                                   message='Please sign in!')
    else:
        if 'name' in request.args:
            name = request.args["name"]
            if name == '':
                return render_template('assignment3_2.html', users=users)
            details = None
            for user_name in users.values():
                if user_name['name'] == name:
                    details = user_name
                    break
            if details:
                return render_template('assignment3_2.html',
                                       name=details['name'],
                                       email=details['email'],
                                       user_name=details['user_name']
                                        )
            else:
                return render_template('assignment3_2.html',
                                       no_user_message='No user found')
        return render_template('assignment3_2.html'
                               )

@app.route('/log_out')
def logout_func():
    session['loged_in'] = False
    session.clear()
    return redirect(url_for('display_users_page'))


@app.route('/session')
def session_func():
    return jsonify(dict(session))



from pages.assignment_4.assignment_4 import assignment_4
app.register_blueprint(assignment_4)



if __name__ == '__main__':
    app.run()
