from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from app.extensions import db


class User(db.Model, UserMixin):
    """Model użytkownika systemu.

    Przechowuje podstawowe informacje o użytkowniku oraz jego relacje
    z tablicami zadań i uprawnieniami.

    Attributes:
        id (int): Unikalny identyfikator użytkownika.
        email (str): Adres email użytkownika (unikalny).
        password (str): Zahaszowane hasło użytkownika.
        task_boards (list[TaskBoard]): Lista tablic zadań utworzonych przez użytkownika.
        permissions (list[TaskBoardPermission]): Lista uprawnień użytkownika do tablic.
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    task_boards = relationship("TaskBoard", back_populates="owner")
    permissions = relationship("TaskBoardPermission", back_populates="user")


class Task(db.Model):
    """Model zadania w tablicy zadań.

    Reprezentuje pojedyncze zadanie, które może być przypisane do jednej z kolumn
    w tablicy zadań.

    Attributes:
        id (int): Unikalny identyfikator zadania.
        column (str): Nazwa kolumny, w której znajduje się zadanie (domyślnie: "todo").
        description (str): Opis zadania.
        task_board_id (int): Identyfikator tablicy zadań, do której należy zadanie.
        task_board (TaskBoard): Tablica zadań, do której należy zadanie.
    """
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.String(20), nullable=False, default="todo")
    description = db.Column(db.String(120), nullable=False)
    task_board_id = db.Column(db.Integer, ForeignKey("task_boards.id"))
    task_board = relationship("TaskBoard", back_populates="tasks")


class TaskBoard(db.Model):
    """Model tablicy zadań.

    Reprezentuje tablicę zadań, która może zawierać wiele zadań i mieć
    wielu użytkowników z różnymi uprawnieniami.

    Attributes:
        id (int): Unikalny identyfikator tablicy.
        name (str): Nazwa tablicy.
        owner_id (int): Identyfikator właściciela tablicy.
        owner (User): Właściciel tablicy.
        tasks (list[Task]): Lista zadań w tablicy.
        permissions (list[TaskBoardPermission]): Lista uprawnień użytkowników do tablicy.

    Note:
        Nazwa tablicy musi być unikalna dla danego właściciela.
    """
    __tablename__ = "task_boards"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="task_boards")
    tasks = relationship("Task", back_populates="task_board",
                         cascade="all, delete-orphan")
    permissions = relationship(
        "TaskBoardPermission", back_populates="task_board", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('name', 'owner_id',
                         name='uq_taskboard_name_per_user'),
    )


class TaskBoardPermission(db.Model):
    """Model uprawnień użytkownika do tablicy zadań.

    Definiuje rolę użytkownika w kontekście konkretnej tablicy zadań.

    Attributes:
        user_id (int): Identyfikator użytkownika.
        task_board_id (int): Identyfikator tablicy zadań.
        role (str): Rola użytkownika w tablicy ('moderator' lub 'viewer').
        user (User): Użytkownik, którego dotyczy uprawnienie.
        task_board (TaskBoard): Tablica zadań, której dotyczy uprawnienie.
    """
    __tablename__ = "task_board_permissions"
    user_id = db.Column(db.Integer, ForeignKey("users.id"), primary_key=True)
    task_board_id = db.Column(db.Integer, ForeignKey(
        "task_boards.id"), primary_key=True)
    role = db.Column(db.String(10), nullable=False)

    user = relationship("User", back_populates="permissions")
    task_board = relationship("TaskBoard", back_populates="permissions")
