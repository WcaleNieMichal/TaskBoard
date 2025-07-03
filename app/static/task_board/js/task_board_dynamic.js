class TaskBoardManager {
    constructor(boardId) {
        this.csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        this.userRole = document.querySelector('meta[name="user-role"]').getAttribute('content');
        this.isOwner = document.querySelector('meta[name="board-owner"]').getAttribute('content') === 'True';
        this.boardId = boardId;
        this.error = null;
        this.confirmDeleteTaskModal = null;
        this.taskToDelete = null;

        this.init();
    }

    init() {
        this.initSortable();
        this.initPermissionHandling();
        this.initTaskDeletion();
        this.updateAllTrashIcons();
    }

    initSortable() {
        const lists = ['todo', 'inprogress', 'done'];

        lists.forEach(id => {
            const element = document.getElementById(id);
            Sortable.create(element, {
                group: { name: 'tasks', pull: true, put: true },
                animation: 150,
                ghostClass: 'drag-ghost',
                onEnd: (evt) => this.handleTaskMove(evt)
            });
        });
    }

    handleTaskMove(evt) {
        const taskId = evt.item.dataset.id;
        const newColumn = evt.to.id;
        const newIndex = evt.newIndex;

        if (this.error !== 'Brak uprawnien') {
            this.updateTaskOnServer(taskId, newColumn)
                .then(success => {
                    if (success) {
                        this.updateTrashIconForTask(evt.item, newColumn);
                    } else {
                        // Revert the move if server update failed
                        this.revertTaskMove(evt);
                    }
                });
        }
    }

    async updateTaskOnServer(taskId, newColumn) {
        try {
            const response = await fetch(`/task_boards/${this.boardId}/update_task`, {
                method: 'POST',
                credentials: "include",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify({
                    id: taskId,
                    column: newColumn
                })
            });

            const data = await response.json();

            if (data.status === "success") {
                return true;
            } else {
                console.log(data);
                if (data.error === 'Brak uprawnien') {
                    if (this.error === null) {
                        alert("Nie masz uprawnień, ale możesz edytować lokalnie");
                        this.error = data.error;
                    }
                }
                return false;
            }
        } catch (err) {
            console.error("Błąd fetch:", err);
            alert("Błąd połączenia z serwerem");
            return false;
        }
    }

    revertTaskMove(evt) {
        // Move the task back to its original position
        const item = evt.item;
        const from = evt.from;
        const oldIndex = evt.oldIndex;

        from.insertBefore(item, from.children[oldIndex]);
    }

    canDeleteTasks() {
        return this.userRole === 'moderator' || this.userRole === 'none' || this.isOwner;
    }

    updateAllTrashIcons() {
        const allTasks = document.querySelectorAll('.list-group-item[data-id]');
        allTasks.forEach(task => {
            const column = task.parentElement.id;
            this.updateTrashIconForTask(task, column);
        });
    }

    updateTrashIconForTask(taskElement, column) {
        const actionsContainer = taskElement.querySelector('.task-actions');
        const existingIcon = actionsContainer.querySelector('.task-trash-icon');

        // Remove existing icon
        if (existingIcon) {
            existingIcon.remove();
        }

        // Add trash icon only if task is in 'done' column and user has permissions
        if (column === 'done' && this.canDeleteTasks()) {
            const trashIcon = this.createTrashIcon(taskElement.dataset.id);
            actionsContainer.appendChild(trashIcon);
        }
    }

    createTrashIcon(taskId) {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'btn btn-danger btn-sm task-trash-icon';
        button.title = 'Usuń';
        button.innerHTML = '<i class="bi bi-trash"></i>';
        button.onclick = () => this.showDeleteTaskModal(taskId);
        return button;
    }

    initTaskDeletion() {
        this.confirmDeleteTaskModal = new bootstrap.Modal(document.getElementById('confirmDeleteTaskModal'));

        document.getElementById('confirmDeleteTaskBtn').addEventListener('click', () => {
            if (this.taskToDelete) {
                this.deleteTask(this.taskToDelete);
            }
        });
    }

    showDeleteTaskModal(taskId) {
        this.taskToDelete = taskId;
        this.confirmDeleteTaskModal.show();
    }

    async deleteTask(taskId) {
        try {
            const response = await fetch(`/task_boards/${this.boardId}/delete/${taskId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': this.csrfToken
                }
            });

            if (response.ok) {
                // Remove task from DOM
                const taskElement = document.querySelector(`[data-id="${taskId}"]`);
                if (taskElement) {
                    taskElement.remove();
                }
                this.confirmDeleteTaskModal.hide();
            } else {
                alert('Błąd podczas usuwania zadania');
            }
        } catch (error) {
            console.error('Error deleting task:', error);
            alert('Błąd połączenia z serwerem');
        } finally {
            this.taskToDelete = null;
        }
    }

    initPermissionHandling() {
        const confirmDeleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
        let userToDelete = null;

        // Handle email clicks
        document.querySelectorAll('.clickable-email').forEach(email => {
            email.addEventListener('click', function () {
                const userId = this.dataset.userId;
                const userEmail = this.dataset.userEmail;
                userToDelete = userId;
                document.getElementById('userEmailSpan').textContent = userEmail;
                confirmDeleteModal.show();
            });
        });

        // Handle permission deletion confirmation
        document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
            if (userToDelete) {
                fetch(`/task_board/view_board/${this.boardId}/remove_role/${userToDelete}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrfToken
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message) {
                            location.reload(); // Still reload for permission changes
                        } else {
                            alert(data.error || 'Wystąpił błąd podczas usuwania uprawnień');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Wystąpił błąd podczas usuwania uprawnień');
                    })
                    .finally(() => {
                        confirmDeleteModal.hide();
                    });
            }
        });
    }
}

// Initialize TaskBoard when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    const boardId = document.querySelector('meta[name="board-id"]').getAttribute('content');
    new TaskBoardManager(parseInt(boardId));
}); 