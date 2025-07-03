"""Moduł zarządzania rolami i uprawnieniami użytkowników.

Ten moduł zawiera funkcjonalność związaną z zarządzaniem uprawnieniami
użytkowników do tablic zadań, w tym dodawanie i usuwanie ról.
"""

from flask import Blueprint

role = Blueprint('role', __name__, url_prefix='/task_board/view_board')
