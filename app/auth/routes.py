from flask import Blueprint, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from app.extensions import db
from app.models import User
from .forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Obsługuje proces logowania użytkownika.

    Renderuje formularz logowania i przetwarza dane przesłane przez użytkownika.
    W przypadku poprawnych danych, loguje użytkownika i przekierowuje do strony głównej.

    Returns:
        flask.Response: Wyrenderowany szablon formularza logowania lub przekierowanie
            do strony głównej po udanym logowaniu.

    Note:
        Jeśli dane logowania są nieprawidłowe, dodaje komunikat o błędzie do formularza.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        form.password.errors.append("Nieprawidłowy email lub hasło")
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Obsługuje proces rejestracji nowego użytkownika.

    Renderuje formularz rejestracji i przetwarza przesłane dane.
    Tworzy nowe konto użytkownika jeśli email nie jest zajęty.

    Returns:
        flask.Response: Wyrenderowany szablon formularza rejestracji lub przekierowanie
            do strony głównej po udanej rejestracji.

    Note:
        Jeśli email jest już zajęty, dodaje komunikat o błędzie do formularza.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            new_user = User(email=form.email.data,
                            password=generate_password_hash(form.password.data))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('main.home'))
        form.email.errors.append("Email jest już zarejestrowany")

    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Wylogowuje aktualnie zalogowanego użytkownika.

    Wymaga zalogowanego użytkownika (dekorator login_required).

    Returns:
        flask.Response: Przekierowanie do strony logowania.
    """
    logout_user()
    return redirect(url_for('auth.login'))
