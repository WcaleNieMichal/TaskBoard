from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.String(20), nullable=False, default="todo")
    description = db.Column(db.String(120), nullable=False)
    task_board_id = db.Column(db.Integer, ForeignKey("task_boards.id"))
    task_board = relationship("TaskBoard", back_populates="tasks")


class TaskBoard(db.Model):
    __tablename__ = "task_boards"
    name = db.Column(db.String(120), unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    # owner_id = db.Column(db.Integer, nullable=False)
    tasks = relationship("Task", back_populates="task_board")
