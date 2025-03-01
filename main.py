from flask import Flask, jsonify

# Это callable WSGI-приложение
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello!'

@app.get('/users')
def users_get():
    return 'GET /users'

@app.post('/users')
def users_post():
    return 'POST /users'


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