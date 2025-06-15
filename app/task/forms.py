from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired


class NewTaskForm(FlaskForm):
    task_board_id = HiddenField()
    title = StringField('Tytuł zadania', [DataRequired()])
    submit = SubmitField('Dodaj')
