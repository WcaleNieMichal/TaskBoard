from flask import Blueprint, jsonify, render_template, request
from app.models import Task
from app.extensions import db

task_board = Blueprint('task_board', __name__)


@task_board.route('/')
def home():
    tasks = Task.query.all()
    return render_template('task_board.html', tasks=tasks)


@task_board.route('/update_task', methods=['POST'])
def update_column():
    print("⏺ Żądanie POST /update_task otrzymane")
    print("Nagłówki:", request.headers)
    print("Body:", request.data)

    data = request.get_json(force=True, silent=True)
    if not data:
        print("❌ Brak danych JSON w żądaniu!")
        return jsonify({"status": "error", "message": "Brak danych JSON"}), 400

    try:
        task_id = int(data.get('id'))
        new_column = data.get('column')
        print(f"📦 Parsed JSON: id={task_id}, column={new_column}")

        task = Task.query.get(task_id)
        if not task:
            return jsonify({"status": "error", "message": "Task not found"}), 404

        task.column = new_column
        db.session.commit()
        print(f"✔ Task {task.id} zaktualizowany -> {new_column}")
        return jsonify({"status": "success"})

    except Exception as e:
        print("❗ Błąd:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
