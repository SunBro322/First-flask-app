import json
import os.path
from typing import List
import logging
from logging.handlers import RotatingFileHandler
from urllib.parse import unquote

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, get_flashed_messages, abort

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

@app.errorhandler(404)
def not_found(error):
    app.logger.error(f'404 ошибка: {error}')
    return 'Page not found', 404

@app.errorhandler(500)
def arise_errors(error):
    app.logger.error(f'500 ошибка - Ошибка в main: {error}')
    return 'Script has errors', 500

def validate(data):
    """ Проверяем входящие данные с формы """
    errors = {}

    if not data.get('email'):
        errors['email'] = "Can't be blank"

    return errors

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

@app.route('/users/<path:email>/edit')
def users_edit(email):
    users = load_users()
    decoded_email = unquote(email)

    info_user = next((user for user in users if user['email'] == decoded_email), None)
    errors = []

    if not info_user:
        app.logger.error(f"Пользователь с email {decoded_email} не найден")
        abort(404)

    return render_template(
        'users/edit.html',
        errors=errors,
        user=info_user,
    )

@app.route('/users/<path:email>/patch', methods=['POST'])
def user_patch(email):
    """ Редактирование Email """
    users = load_users()
    decoded_email = unquote(email)

    user_index = next((i for i, user in enumerate(users) if user['email'] == decoded_email), None)

    if user_index is None:
        app.logger.error(f"Пользователь {decoded_email} не найден для обновления")
        abort(404)

    data = request.form.to_dict()
    app.logger.info("Отправляем в валидатор")
    errors = validate(data)

    if errors:
        return render_template(
            'users/edit.html',
            user={'email': decoded_email},
            errors=errors,
        ), 422


    users[user_index]['email'] = data['email'].strip()
    save_user(users)

    flash('Email has been updated', 'success')
    return redirect(url_for('get_users'))


@app.route('/user/<id>/delete', methods=['POST'])
def user_delete(id):
    users = load_users()
    user_index = next((i for i, user in enumerate(users) if str(user['id']) == str(id)), None)

    if user_index is None:
        app.logger.error(f"Пользователь {id} не найден для удаления")
        abort(404)

    users.pop(user_index)
    save_user(users)

    flash('User has been deleted', 'success')
    return redirect(url_for('get_users'))



@app.route('/users')
def get_users():
    """ Вывод пользователей """
    messages = get_flashed_messages(with_categories=True)
    users = load_users()
    app.logger.info('Вывод пользователей')
    return render_template('users/users.html', users=users, messages=messages)
