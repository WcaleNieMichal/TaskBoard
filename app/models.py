from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    task_boards = relationship("TaskBoard", back_populates="owner")
    permissions = relationship("TaskBoardPermission", back_populates="user")


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.String(20), nullable=False, default="todo")
    description = db.Column(db.String(120), nullable=False)
    task_board_id = db.Column(db.Integer, ForeignKey("task_boards.id"))
    task_board = relationship("TaskBoard", back_populates="tasks")


class TaskBoard(db.Model):
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
    __tablename__ = "task_board_permissions"
    user_id = db.Column(db.Integer, ForeignKey("users.id"), primary_key=True)
    task_board_id = db.Column(db.Integer, ForeignKey(
        "task_boards.id"), primary_key=True)
    role = db.Column(db.String(10), nullable=False)

    user = relationship("User", back_populates="permissions")
    task_board = relationship("TaskBoard", back_populates="permissions")
