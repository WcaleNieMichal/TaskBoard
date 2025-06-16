from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NewTaskForm(FlaskForm):
    title = StringField('Tytuł zadania', [DataRequired()])
    submit = SubmitField('Dodaj')
