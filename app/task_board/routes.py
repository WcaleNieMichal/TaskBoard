from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from app.decorators import role_required
from app.models import TaskBoard
from app.extensions import db
from app.task.forms import NewTaskForm

task_board = Blueprint('task_board', __name__)


@task_board.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))


@role_required('moderator', 'viewer')
@task_board.route('/view_board/<int:board_id>')
def show_board(board_id):
    form = NewTaskForm()
    board = TaskBoard.query.filter_by(
        id=board_id, owner_id=current_user.id).first()
    if board:
        return render_template('task_board.html', form=form, board=board)
    return redirect(url_for('task_board.home'))


@task_board.route('/')
def home():
    boards = TaskBoard.query.filter_by(owner_id=current_user.id)
    return render_template('dash_board.html', boards=boards)


@task_board.route('/add_task_board', methods=['POST'])
def add_task_board():
    data = request.get_json()
    table_name = data.get('tableName', '').strip()

    # Walidacja pustego pola
    if not table_name:
        return jsonify({'message': 'Nazwa tablicy nie może być pusta'}), 400

    # Sprawdzenie, czy tablica już istnieje
    if TaskBoard.query.filter_by(name=table_name, owner_id=current_user.id).first():
        return jsonify({'message': 'Tablica już istnieje', 'name': table_name}), 400

    # Dodanie nowej tablicy
    new_board = TaskBoard(name=table_name, owner_id=current_user.id)
    db.session.add(new_board)
    db.session.commit()

    return jsonify({'message': 'Dodano tablicę', 'name': table_name, 'id': new_board.id})


@role_required('moderator')
@task_board.route('/delete/<int:board_id>', methods=['DELETE'])
def delete_board(board_id):
    board = TaskBoard.query.filter_by(
        id=board_id, owner_id=current_user.id).first()
    if not board:
        return jsonify({'error': 'Tablica nie istnieje'}), 404

    db.session.delete(board)
    db.session.commit()
    return jsonify({'message': 'Tablica usunięta'})
