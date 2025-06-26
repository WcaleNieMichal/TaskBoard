from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Hasło', [DataRequired()])
    submit = SubmitField('Zaloguj Się')


class RegisterForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Hasło', [DataRequired()])
    password_confirmed = PasswordField('Powtórz hasło', [DataRequired(), EqualTo(
        'password', message="Hasła muszą byc identyczne")])
    submit = SubmitField('Zarejestruj Się')
