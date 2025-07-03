from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    """Formularz logowania użytkownika.

    Zawiera pola do wprowadzania adresu email i hasła.

    Attributes:
        email (StringField): Pole do wprowadzania adresu email.
        password (PasswordField): Pole do wprowadzania hasła.
        submit (SubmitField): Przycisk do wysłania formularza.
    """
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Hasło', [DataRequired()])
    submit = SubmitField('Zaloguj Się')


class RegisterForm(FlaskForm):
    """Formularz rejestracji nowego użytkownika.

    Zawiera pola do utworzenia nowego konta użytkownika z potwierdzeniem hasła.

    Attributes:
        email (StringField): Pole do wprowadzania adresu email.
        password (PasswordField): Pole do wprowadzania hasła.
        password_confirmed (PasswordField): Pole do potwierdzenia hasła.
        submit (SubmitField): Przycisk do wysłania formularza.
    """
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Hasło', [DataRequired()])
    password_confirmed = PasswordField('Powtórz hasło', [DataRequired(), EqualTo(
        'password', message="Hasła muszą byc identyczne")])
    submit = SubmitField('Zarejestruj Się')
