from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Hasło', [DataRequired()])
    submit = SubmitField('Zaloguj Się')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Nie ma takiego użytkownika")


class RegisterForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Hasło', [DataRequired()])
    password_confirmed = PasswordField('Powtórz hasło', [DataRequired(), EqualTo(
        'password', message="Hasła muszą byc identyczne")])
    submit = SubmitField('Zarejestruj Się')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email jest już zarejestrowany")
