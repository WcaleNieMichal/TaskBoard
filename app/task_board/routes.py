from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from app.decorators import role_required
from app.models import TaskBoard, User, TaskBoardPermission
from app.extensions import db
from app.task.forms import NewTaskForm
from app.role.forms import AddUserRoles

task_board = Blueprint('task_board', __name__)


@task_board.before_request
def require_login():
    """Sprawdza, czy użytkownik jest zalogowany przed każdym żądaniem.

    Returns:
        flask.Response: Przekierowanie do strony logowania jeśli użytkownik nie jest zalogowany.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))


@task_board.route('/view_board/<int:board_id>')
@role_required('moderator', 'viewer')
def show_board(board_id):
    """Wyświetla szczegóły tablicy zadań.

    Wymaga roli moderatora lub widza. Renderuje widok tablicy z zadaniami
    i formularzami do zarządzania.

    Args:
        board_id (int): Identyfikator tablicy zadań.

    Returns:
        flask.Response: Wyrenderowany szablon tablicy zadań lub przekierowanie
            do dashboard'u jeśli tablica nie istnieje.
    """
    new_task_form = NewTaskForm()
    user_role_form = AddUserRoles()
    board = TaskBoard.query.filter_by(
        id=board_id).first()
    task_board_permissions = TaskBoardPermission.query.filter_by(
        task_board_id=board_id).all()
    user_role = TaskBoardPermission.query.filter_by(
        task_board_id=board_id,
        user_id=current_user.id).first()
    if user_role:
        user_role = user_role.role

    if board:
        return render_template('task_board.html', user_role=user_role, current_user=current_user, task_form=new_task_form, role_form=user_role_form, board=board, task_board_permissions=task_board_permissions)
    return redirect(url_for('task_board.home'))


@task_board.route('/')
def home():
    """Wyświetla dashboard z tablicami zadań użytkownika.

    Pobiera tablice zadań należące do użytkownika oraz te, do których
    ma udostępnione uprawnienia.

    Returns:
        flask.Response: Wyrenderowany szablon dashboard'u z listą tablic zadań.
    """
    boards = TaskBoard.query.filter_by(owner_id=current_user.id).all()
    shared_boards = [x.task_board for x in TaskBoardPermission.query.filter_by(
        user_id=current_user.id).all()]
    return render_template('dash_board.html', shared_boards=shared_boards, boards=boards, user_email=current_user.email)


@task_board.route('/add_task_board', methods=['POST'])
def add_task_board():
    """Tworzy nową tablicę zadań.

    Przetwarza żądanie JSON z nazwą nowej tablicy.

    Returns:
        flask.Response: Odpowiedź JSON z informacją o sukcesie lub błędzie.

    Note:
        Nazwa tablicy musi być unikalna dla danego użytkownika.
    """
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


@task_board.route('/delete/<int:board_id>', methods=['DELETE'])
@role_required('moderator')
def delete_board(board_id):
    """Usuwa tablicę zadań.

    Wymaga roli moderatora. Tablica może być usunięta tylko przez jej właściciela.

    Args:
        board_id (int): Identyfikator tablicy zadań do usunięcia.

    Returns:
        flask.Response: Odpowiedź JSON z potwierdzeniem usunięcia lub błędem.

    Raises:
        404: Tablica nie istnieje lub użytkownik nie jest jej właścicielem.
    """
    board = TaskBoard.query.filter_by(
        id=board_id, owner_id=current_user.id).first()
    if not board:
        return jsonify({'error': 'Tablica nie istnieje'}), 404

    db.session.delete(board)
    db.session.commit()
    return jsonify({'message': 'Tablica usunięta'})
