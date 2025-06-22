from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired


class AddUserRoles(FlaskForm):
    email = StringField('Email', [DataRequired()])
    choice = RadioField('Wybierz role', choices=[
                        ('moderator', 'Moderator'), ('viewer', 'Gość')], validators=[DataRequired()])
    submit = SubmitField('Dodaj')
