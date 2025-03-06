import json
import os.path
from contextlib import redirect_stderr
from typing import List

from flask import Flask, jsonify, render_template, request, redirect, url_for

# Это callable WSGI-приложение
app = Flask(__name__)

@app.route('/')
def hello_world():
    return redirect(url_for('get_users'))


@app.get('/dict')
def get_dict():
    """ Обработка словарей и вывод пользователю"""

    data = {
        'name': 'John Doe',
        'age': 30,
        'is_student': False,
        'courses': ['Math', 'Science', 'History']
    }
    return jsonify(data)

@app.route('/courses/<id>')
def courses_show(id):
    return f"Course id: {id}"

@app.errorhandler(404)
def not_found(error):
    return 'Page not found', 404

@app.errorhandler(500)
def arise_errors(error):
    return 'Script has errors', 500

@app.route('/users_id/<id>')
def show_user(id):
    """ Отображение пользователя с выводом HTML"""
    return render_template(
        'show.html',
        id=id,
    )


@app.route('/find_user')
def find_user():
    """ Поиск пользователей """
    search_term = request.args.get('search', '').lower()
    users = load_users()
    filtered_users = [user for user in users if search_term in user['name'].lower()]
    return render_template('users/index.html', users=filtered_users)

def load_users() -> List:
    """ Считывание данных из Json """
    if not os.path.exists(r"..\First-flask-app\data base\user.json"):
        return []

    with open(r"..\First-flask-app\data base\user.json") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = []
    return users

def save_user(users):
    """ Сохранение данных по пользователям """
    with open(r'..\First-flask-app\data base\user.json', 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/create-users', methods=['POST', 'GET'])
def create_user():
    """ Создание нового пользователя """
    if request.method:
        name = request.form.get('name')
        email = request.form.get('email')
        if name and email:
            users = load_users()
            new_id = max(user['id'] for user in users) + 1 if users else 1
            new_user = {'id': new_id,
                        'name': name,
                        'email': email}
            users.append(new_user)
            save_user(users)
            return redirect(url_for('get_users'))
    return render_template('users/create_user.html')

@app.route('/users')
def get_users():
    """ Вывод пользователей """
    users = load_users()
    return render_template('users/users.html', users=users)
