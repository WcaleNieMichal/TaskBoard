from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NewTaskForm(FlaskForm):
    """Formularz dodawania nowego zadania.

    Zawiera pole do wprowadzania tytułu nowego zadania.

    Attributes:
        title (StringField): Pole do wprowadzania tytułu zadania.
        submit (SubmitField): Przycisk do wysłania formularza.
    """
    title = StringField('Tytuł zadania', [DataRequired()])
    submit = SubmitField('Dodaj')
