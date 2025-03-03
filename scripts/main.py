

from flask import Flask, jsonify, render_template, request

# Это callable WSGI-приложение
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello!'

# @app.get('/users')
# def users_get():
#     return 'GET /users'
#
# @app.post('/users')
# def users_post():
#     return 'POST /users'


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

# @app.route('/users/<id>')
# def show_user(id):
#     """ Отображение пользователя с выводом HTML"""
#     return render_template(
#         'show.html',
#         id=id,
#     )

users = [
    {'id': 1, 'name': 'mike'},
    {'id': 2, 'name': 'mishel'},
    {'id': 3, 'name': 'adel'},
    {'id': 4, 'name': 'keks'},
    {'id': 5, 'name': 'kamila'}
]

@app.route('/users')
def show_users():
    search_term = request.args.get('search', '').lower()
    filtered_users = [user for user in users if search_term in user['name'].lower()]
    return render_template('users/index.html', users=filtered_users)