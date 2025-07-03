import os


class Config:
    """Klasa konfiguracyjna aplikacji Flask.

    Zawiera wszystkie ustawienia konfiguracyjne aplikacji, w tym
    klucz sekretny, ustawienia bazy danych i inne parametry.

    Attributes:
        SECRET_KEY (str): Klucz sekretny używany do szyfrowania sesji.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Wyłącza śledzenie modyfikacji SQLAlchemy.
        SQLALCHEMY_DATABASE_URI (str): URI połączenia z bazą danych.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' +
        os.path.join(os.path.abspath(os.path.dirname(__file__)),
                     '..', 'instance', 'taskboard.db')
    )
