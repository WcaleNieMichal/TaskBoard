from flask import Blueprint, render_template, url_for
from werkzeug.security import generate_password_hash
from flask_login import login_user
from app.extensions import db
from app.models import User
from .forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return 'Success'
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data,
                        password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        url_for('main.home')

    return render_template('register.html', form=form)
