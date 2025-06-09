from extensions import db


class User(db.Model):
    __tablename__ = "users"  # dwa podkreślenia z obu stron
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
