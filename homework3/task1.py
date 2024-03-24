'''
Задание

Создать форму для регистрации пользователей на сайте. Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль"
и кнопку "Зарегистрироваться". При отправке формы данные должны сохраняться в базе данных, а пароль должен быть
зашифрован.
'''

import secrets

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm
from models import User, db
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('base.html')


@app.cli.command('init-db')
def init_db():
    db.create_all()


@app.route('/registration/', methods=['GET', 'POST'])
def add_user():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        db.session.add(
            User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data)
            ))
        db.session.commit()
        return 'Registration completed.<br> <a href="/">To Home Page.</a>'
    return render_template('registration.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)