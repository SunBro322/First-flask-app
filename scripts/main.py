import json
import os.path
from typing import List
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, get_flashed_messages

# Это callable WSGI-приложение
app = Flask(__name__)
app.secret_key = "secret_key"
path_JSON = os.path.abspath(r'data base/user.json')

if not app.debug:
    # Создание обработчика
    log_dir = os.path.abspath('logs')
    log_file = os.path.join(log_dir, 'log')
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )

    # Формат сообщений
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

@app.route('/')
def hello_world():
    app.logger.info('Главная страница запрошена')
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
    app.logger.error(f'404 ошибка: {error}')
    return 'Page not found', 404

@app.errorhandler(500)
def arise_errors(error):
    app.logger.error(f'500 ошибка - Ошибка в main: {error}')
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
    app.logger.info('Производится поиск пользователей')
    search_term = request.args.get('search', '').lower()
    users = load_users()
    filtered_users = [user for user in users if search_term in user['name'].lower()]
    return render_template('users/index.html', users=filtered_users)

def load_users() -> List:
    """ Считывание данных из Json """
    app.logger.info('Считывание данных с Json')
    if not os.path.exists(path_JSON):
        return []

    with open(path_JSON) as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = []
    return users

def save_user(users):
    """ Сохранение данных по пользователям """
    app.logger.info('Сохранение данных по пользователям')
    with open(path_JSON, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/create-users', methods=['POST', 'GET'])
def create_user():
    """ Создание нового пользователя """
    app.logger.info('Создание нового пользователя')
    if request.method == 'POST':
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
            flash('User was added successfully', 'success')
            return redirect(url_for('get_users'))
        elif (not name and email) or (name and not email):
            flash('User was not added', 'warning')

    messages = get_flashed_messages(with_categories=True)
    return render_template('users/create_user.html', messages=messages)

@app.route('/users')
def get_users():
    """ Вывод пользователей """
    messages = get_flashed_messages(with_categories=True)
    users = load_users()
    app.logger.info('Вывод пользователей')
    return render_template('users/users.html', users=users, messages=messages)
