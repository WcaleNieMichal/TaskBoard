from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from app.extensions import db, csrf, migrate

from app.models import User
from app.extensions import login_manager

login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    """Ładuje użytkownika na podstawie jego identyfikatora.

    Funkcja wymagana przez Flask-Login do ładowania użytkownika z sesji.

    Args:
        user_id: Identyfikator użytkownika do załadowania.

    Returns:
        User: Obiekt użytkownika lub None jeśli nie znaleziono.
    """
    return User.query.get(int(user_id))


def create_app():
    """Tworzy i konfiguruje aplikację Flask.

    Inicjalizuje wszystkie rozszerzenia Flask, rejestruje blueprinty
    i konfiguruje podstawowe ustawienia aplikacji.

    Returns:
        Flask: Skonfigurowana instancja aplikacji Flask.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import i rejestracja blueprintów
    from .routes import main
    from .auth.routes import auth
    from .task_board.routes import task_board
    from .task.routes import task_bp
    from .role import role

    # Import routes after blueprint registration to avoid circular imports
    from .role import routes

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(task_board, url_prefix='/task_board')
    app.register_blueprint(task_bp)
    app.register_blueprint(role)

    return app
