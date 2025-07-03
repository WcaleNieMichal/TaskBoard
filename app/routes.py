from flask import Blueprint, redirect, url_for
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    """Przekierowuje do strony głównej tablicy zadań.

    Wymaga zalogowanego użytkownika. Funkcja pełni rolę punktu wejścia
    do aplikacji, przekierowując do dashboard'u z tablicami zadań.

    Returns:
        flask.Response: Przekierowanie do strony głównej tablicy zadań.
    """
    return redirect(url_for('task_board.home'))
