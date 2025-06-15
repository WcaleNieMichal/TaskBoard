from flask import Blueprint, jsonify, redirect, request, url_for
from app.extensions import db

from app.models import Task
from .forms import NewTaskForm

task_bp = Blueprint('task', __name__)


@task_bp.route('/update_task', methods=['POST'])
def update_column():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "Brak danych JSON"}), 400

    try:
        task_id = int(data.get('id'))
        new_column = data.get('column')

        task = Task.query.get(task_id)
        if not task:
            return jsonify({"status": "error", "message": "Task not found"}), 404

        task.column = new_column
        db.session.commit()
        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@task_bp.route('/add_task', methods=['POST'])
def add_task():
    form = NewTaskForm()
    print(form.task_board_id.data)
    if form.validate_on_submit():
        new_task = Task(
            description=form.title.data,
            task_board_id=int(form.task_board_id.data)
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('task_board.show_board', board_id=form.task_board_id.data))


@task_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):

    task_to_delete = db.session.query(Task).filter_by(
        id=task_id, column='done').first()
    board = task_to_delete.task_board
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
    return redirect(url_for('task_board.show_board', board_id=board.id))
