import os
import mysql.connector
from flask import Flask, Blueprint, render_template, request, redirect, jsonify
from flask import url_for
from datetime import timedelta
from flask import session
import requests
import asyncio
import aiohttp
from dotenv import load_dotenv

assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='static',
                         template_folder='templates')


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host=os.getenv('DB_HOST'),
                                         user=os.getenv('DB_USER'),
                                         passwd=os.getenv('DB_PASSWORD'),
                                         database=os.getenv('DB_NAME'))
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


@assignment_4.route('/assignment_4')
def genreal():
    query = 'select * from users'
    users = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=users)


@assignment_4.route('/insert', methods=['GET', 'POST'])
def insert_user():
    if request.method == 'POST':
        username = request.form['user_name']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        query = 'select * from users'
        users = interact_db(query, query_type='fetch')

        for user in users:
            if email == user.email:
                return render_template('assignment_4.html', users=users, message='email already exist')

        query = "INSERT INTO users(user_Name, name, email, password) VALUES ('%s','%s', '%s', '%s')" % (username, name,
                                                                                            email, password)
        interact_db(query=query, query_type='commit')
        query = 'select * from users'
        users = interact_db(query, query_type='fetch')
        return render_template('assignment_4.html', users=users, message='user added ')


@assignment_4.route('/update_user', methods=['GET', 'POST'])
def update_user():
    user_name = request.form['user_name']
    name = request.form['name']
    email = request.form['new_email']
    password = request.form['password']
    query = 'select * from users'
    users = interact_db(query, query_type='fetch')
    for user in users:
        if email == user.email:
            query = "UPDATE users SET name ='%s',email ='%s',password='%s', user_Name='%s' WHERE email='%s';" % (
                name, email, password, user_name, email)
            interact_db(query=query, query_type='commit')
            query = 'select * from users'
            users_update = interact_db(query, query_type='fetch')
            return render_template('assignment_4.html', users=users_update, message=f'{user_name} was updated')
    return render_template('assignment_4.html', users=users, message='no user was found')



@assignment_4.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    email_to_delete = request.form['email_to_delete']
    query = 'select * from users'
    users_delete = interact_db(query, query_type='fetch')
    for user in users_delete:
        if email_to_delete == user.email:
            query = "DELETE FROM users WHERE email ='%s';" % email_to_delete
            interact_db(query, query_type='commit')
            query = 'select * from users'
            users_after_changes = interact_db(query, query_type='fetch')
            return render_template('assignment_4.html', users=users_after_changes,
                                   message=f'{email_to_delete} was deleted')
    return render_template('assignment_4.html', users=users_delete, message='no user was found')


@assignment_4.route('/assignment_4/users', methods=['GET'])
def get_users():
    query = 'select * from users'
    users = interact_db(query, query_type='fetch')
    users_to_jason = []
    for user in users:
        users_to_jason.append({
            'username': user.user_Name,
            'email': user.email,
            'name': user.name
        })
    return jsonify(users_to_jason)


@assignment_4.route('/assignment_4/outer_source', methods=['GET'])
def outer_source():
    if 'id' in request.args:
        user_id = request.args['id']
        result = requests.get('https://reqres.in/api/users/' + user_id)
        user_to_display = result.json()['data']
        return render_template('fetch.html', user_to_display=user_to_display)
    return render_template('fetch.html')


@assignment_4.route('/assignment_4/restapi_users/', methods=['GET'])


def get_default_user():
    query = 'select * from users where user_id=5'
    user = interact_db(query, query_type='fetch')[0]
    users_details = {
        'username': user.user_Name,
        'email': user.email,
        'name': user.name
    }
    return jsonify(users_details)


@assignment_4.route('/assignment_4/restapi_users/<int:USER_ID>', methods=['GET'])
def get_user(USER_ID):
    query = "select * from users where user_id='%s'" % USER_ID
    user = interact_db(query, query_type='fetch')
    users_details=[]
    for user_details in user:
        users_details.append({
            'username': user_details.user_Name,
            'email': user_details.email,
            'name': user_details.name
        })
        return jsonify(users_details)
    return jsonify({
        'error': '404',
        'message': 'User not found!!'
    })
