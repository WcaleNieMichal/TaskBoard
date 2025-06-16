from functools import wraps

from flask import abort, request
from flask_login import current_user

from .models import TaskBoard


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            task_board_id = kwargs.get("task_board_id")
            board = TaskBoard.query.get(task_board_id)
            if not board:
                return abort(404)

            if board.owner_id == current_user.id:
                return f(*args, **kwargs)
            if not current_user.is_authenticated:
                return abort(403)
            if task_board_id is None:
                return abort(404)
            for perm in current_user.permissions:
                if perm.task_board_id == task_board_id and perm.role in roles:
                    return f(*args, **kwargs)
            return abort(403)
        return decorated_function
    return decorator
