from flask import abort, jsonify, redirect, url_for
from flask_login import current_user
from app.decorators import role_required
from app.models import TaskBoard, User, TaskBoardPermission
from app.extensions import db
from .forms import AddUserRoles

# Import blueprintu z __init__.py
from . import role


@role.route('/<int:board_id>/add_role', methods=["POST"])
@role_required()
def add_user_role(board_id):
    """Dodaje uprawnienia użytkownikowi do tablicy zadań.

    Wymaga bycia właścicielem tablicy (sprawdzane przez dekorator role_required).
    Przetwarza formularz z emailem użytkownika i wybraną rolą.
    W przypadku niepoprawnego formularza przekierowuje z powrotem do tablicy.

    Args:
        board_id (int): Identyfikator tablicy zadań.

    Returns:
        flask.Response: Przekierowanie do widoku tablicy zadań.

    Raises:
        404: Tablica nie istnieje, użytkownik nie istnieje lub uprawnienie już istnieje.
    """
    form = AddUserRoles()
    if form.validate_on_submit():

        board = TaskBoard.query.filter_by(id=board_id).first()
        user = User.query.filter_by(email=form.email.data).first()

        if not board or not user:
            abort(404)
        if user.id == current_user.id:
            return redirect(url_for('task_board.show_board', board_id=board_id))

        perm = TaskBoardPermission.query.filter_by(
            user_id=user.id,
            task_board_id=board.id,
            role=form.choice.data,
        ).first()
        if perm:
            abort(404)
        new_permision = TaskBoardPermission(
            user_id=user.id,
            task_board_id=board.id,
            role=form.choice.data,
        )
        db.session.add(new_permision)
        db.session.commit()
    return redirect(url_for('task_board.show_board', board_id=board_id))


@role.route('/<int:board_id>/remove_role/<int:user_id>', methods=['DELETE'])
@role_required('moderator', 'viewer')
def remove_user_role(board_id, user_id):
    """Usuwa uprawnienia użytkownika do tablicy zadań.

    Implementuje hierarchię uprawnień:
    - Właściciel może usunąć wszystkich użytkowników (oprócz siebie)
    - Moderator może usunąć tylko gości
    - Gość nie może usuwać nikogo

    Args:
        board_id (int): Identyfikator tablicy zadań.
        user_id (int): Identyfikator użytkownika do usunięcia.

    Returns:
        flask.Response: Odpowiedź JSON z informacją o sukcesie lub błędzie.

    Raises:
        404: Tablica nie istnieje, użytkownik nie istnieje lub uprawnienie nie istnieje.
        403: Brak uprawnień do usunięcia lub próba usunięcia własnych uprawnień.
    """
    # Sprawdzenie czy użytkownik nie próbuje usunąć własnych uprawnień
    if user_id == current_user.id:
        return jsonify({'error': 'Nie można usunąć własnych uprawnień'}), 403

    # Pobranie tablicy i sprawdzenie czy istnieje
    board = TaskBoard.query.get(board_id)
    if not board:
        return jsonify({'error': 'Tablica nie istnieje'}), 404

    # Sprawdzenie czy uprawnienie do usunięcia istnieje
    permission_to_remove = TaskBoardPermission.query.filter_by(
        user_id=user_id,
        task_board_id=board_id
    ).first()

    if not permission_to_remove:
        return jsonify({'error': 'Uprawnienie nie istnieje'}), 404

    # Sprawdzenie uprawnień użytkownika wykonującego akcję
    if current_user.id == board.owner_id:
        # Właściciel może usunąć wszystkich (oprócz siebie - już sprawdzone wyżej)
        pass
    else:
        # Sprawdzenie czy użytkownik jest moderatorem
        user_permission = TaskBoardPermission.query.filter_by(
            user_id=current_user.id,
            task_board_id=board_id
        ).first()

        if not user_permission or user_permission.role != 'moderator':
            return jsonify({'error': 'Brak uprawnień do usuwania użytkowników'}), 403

        # Moderator może usunąć tylko gości
        if permission_to_remove.role != 'viewer':
            return jsonify({'error': 'Moderator może usuwać tylko gości'}), 403

    # Usunięcie uprawnienia
    db.session.delete(permission_to_remove)
    db.session.commit()

    return jsonify({'message': 'Uprawnienia zostały usunięte'})
