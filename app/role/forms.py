from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired


class AddUserRoles(FlaskForm):
    """Formularz dodawania uprawnień użytkownika do tablicy zadań.

    Zawiera pola do wyboru użytkownika i przypisania mu roli w tablicy zadań.

    Attributes:
        email (StringField): Pole do wprowadzania adresu email użytkownika.
        choice (RadioField): Pole do wyboru roli użytkownika (moderator/gość).
        submit (SubmitField): Przycisk do wysłania formularza.
    """
    email = StringField('Email', [DataRequired()])
    choice = RadioField('Wybierz role', choices=[
                        ('moderator', 'Moderator'), ('viewer', 'Gość')], validators=[DataRequired()])
    submit = SubmitField('Dodaj')
