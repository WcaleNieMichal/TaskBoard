from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from app.extensions import db, csrf, migrate

from app.models import User
from app.extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    # Import i rejestracja blueprintów
    from .routes import main
    from .auth.routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
