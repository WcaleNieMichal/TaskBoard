from flask import Blueprint, redirect, url_for
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    return redirect(url_for('task_board.home'))
