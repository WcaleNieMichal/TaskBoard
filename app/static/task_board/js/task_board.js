async function createTable() {
    const tableName = document.getElementById('tableName').value.trim();
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const messageBox = document.getElementById('message');

    const response = await fetch('/task_board/add_task_board', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ tableName: tableName })
    });

    const result = await response.json();

    if (response.ok) {
        const id = result.id;
        const name = result.name || tableName;

        const link = document.createElement('a');
        link.href = `/task_board/view_board/${id}`;
        link.textContent = name;
        link.className = 'd-block text-decoration-none text-dark flex-grow-1';

        const deleteButton = document.createElement('button');
        deleteButton.className = 'btn btn-sm btn-danger ms-2';
        deleteButton.innerHTML = '<i class="bi bi-trash"></i>';
        deleteButton.onclick = function () {
            deleteBoard(id);
        };

        const li = document.createElement('li');
        li.className = 'list-group-item d-flex align-items-center';
        li.setAttribute('data-id', id);

        li.appendChild(link);
        li.appendChild(deleteButton);

        const list = document.getElementById('taskBoardList');
        list.appendChild(li);

        document.getElementById('tableName').value = '';
        messageBox.textContent = '';
    } else {
        messageBox.textContent = result.message || 'Coś poszło nie tak';
    }

}

async function deleteBoard(boardId) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const confirmed = confirm("Na pewno chcesz usunąć tę tablicę?");
    if (!confirmed) return;

    const response = await fetch(`/task_board/delete/${boardId}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
        }
    });

    const result = await response.json();

    if (response.ok) {
        // Usuń element z DOM
        const item = document.querySelector(`[data-id='${boardId}']`);
        if (item) item.remove();
    } else {
        alert(result.error || "Błąd przy usuwaniu");
    }
}