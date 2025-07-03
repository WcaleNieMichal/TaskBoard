from flask import Blueprint, abort, jsonify, redirect, request, url_for
from app.extensions import db

from app.models import Task
from .forms import NewTaskForm
from app.decorators import role_required

task_bp = Blueprint('task', __name__)


@task_bp.route('/task_boards/<int:board_id>/update_task', methods=['POST'])
@role_required('moderator')
def update_column(board_id):
    """Aktualizuje kolumnę zadania w tablicy zadań.

    Wymaga roli moderatora. Przetwarza żądanie JSON z nową kolumną dla zadania.

    Args:
        board_id (int): Identyfikator tablicy zadań.

    Returns:
        flask.Response: Odpowiedź JSON z informacją o sukcesie lub błędzie.

    Raises:
        400: Brak danych JSON lub niezgodność tablicy zadań.
        404: Nie znaleziono zadania.
        500: Błąd serwera podczas aktualizacji.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "Brak danych JSON"}), 400

    try:
        task_id = int(data.get('id'))
        new_column = data.get('column')

        task = Task.query.get(task_id)
        if not task:
            return jsonify({"status": "error", "message": "Task not found"}), 404
        if task.task_board_id != board_id:
            return jsonify({"status": "error", "message": "Task-board mismatch"}), 400

        task.column = new_column
        db.session.commit()
        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@task_bp.route('/task_boards/<int:board_id>/add_task', methods=['POST'])
@role_required('moderator')
def add_task(board_id):
    """Dodaje nowe zadanie do tablicy zadań.

    Wymaga roli moderatora. Przetwarza formularz z tytułem nowego zadania.
    W przypadku niepoprawnego formularza przekierowuje z powrotem do tablicy.

    Args:
        board_id (int): Identyfikator tablicy zadań.

    Returns:
        flask.Response: Przekierowanie do widoku tablicy zadań.
    """
    form = NewTaskForm()
    if form.validate_on_submit():
        new_task = Task(
            description=form.title.data,
            task_board_id=board_id
        )
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('task_board.show_board', board_id=board_id))


@task_bp.route('/task_boards/<int:board_id>/delete/<int:task_id>', methods=['POST'])
@role_required('moderator')
def delete_task(board_id, task_id):
    """Usuwa zadanie z tablicy zadań.

    Wymaga roli moderatora. Usuwa tylko zadania z kolumny 'done'.

    Args:
        board_id (int): Identyfikator tablicy zadań.
        task_id (int): Identyfikator zadania do usunięcia.

    Returns:
        flask.Response: Przekierowanie do widoku tablicy zadań.

    Raises:
        404: Zadanie nie istnieje lub nie jest w kolumnie 'done'.
    """
    task_to_delete = db.session.query(Task).filter_by(
        id=task_id, column='done').first()
    if not task_to_delete or task_to_delete.task_board_id != board_id:
        abort(404)
    board = task_to_delete.task_board
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
    return redirect(url_for('task_board.show_board', board_id=board.id))
