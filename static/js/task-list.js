(function () {
    var taskIntervals = {};

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function markTaskCompleted(taskId) {
        var title = document.getElementById('task-title-' + taskId);
        var button = document.getElementById('complete-button-' + taskId);
        if (!title || !button) {
            return;
        }
        title.classList.add('has-text-grey-light', 'is-striked');
        button.innerHTML = '<i class="fas fa-undo"></i>';
        button.classList.remove('is-success');
        button.classList.add('is-warning');
        button.setAttribute('onclick', 'undoCompleteTask(' + taskId + '); return false;');
    }

    function markTaskUndone(taskId) {
        var title = document.getElementById('task-title-' + taskId);
        var button = document.getElementById('complete-button-' + taskId);
        if (!title || !button) {
            return;
        }
        title.classList.remove('has-text-grey-light', 'is-striked');
        button.innerHTML = '<i class="fas fa-check"></i>';
        button.classList.remove('is-warning');
        button.classList.add('is-success');
        button.setAttribute('onclick', 'completeTask(' + taskId + '); return false;');
    }

    function removeCategoryIfEmpty(categoryId) {
        if (!categoryId) {
            return;
        }
        fetch('/get_tasks/' + categoryId + '/')
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.tasks.length === 0) {
                    var categoryElement = document.getElementById('category-' + categoryId);
                    if (categoryElement) {
                        categoryElement.remove();
                    }
                }
            })
            .catch(function () {});
    }

    function deleteTask(taskId) {
        var taskElement = document.getElementById('task-' + taskId);
        var categoryId = taskElement ? taskElement.dataset.categoryId : null;

        fetch('/api/v1/tasks/' + taskId + '/delete/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Delete failed');
                }
                if (taskElement) {
                    taskElement.classList.add('fade-out');
                    taskElement.addEventListener('animationend', function () {
                        taskElement.remove();
                    });
                }
                removeCategoryIfEmpty(categoryId);
            })
            .catch(function () {});
    }

    function startDeleteCountdown(taskId) {
        if (taskIntervals[taskId]) {
            clearInterval(taskIntervals[taskId]);
        }

        var countdown = 5;
        taskIntervals[taskId] = setInterval(function () {
            countdown -= 1;
            if (countdown < 0) {
                clearInterval(taskIntervals[taskId]);
                delete taskIntervals[taskId];
            }
        }, 1000);
    }

    function completeTask(taskId) {
        markTaskCompleted(taskId);
        fetch('/api/v1/tasks/' + taskId + '/state/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ completed: true })
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Complete failed');
                }
                startDeleteCountdown(taskId);
            })
            .catch(function () {
                markTaskUndone(taskId);
            });
    }

    function undoCompleteTask(taskId) {
        if (taskIntervals[taskId]) {
            clearInterval(taskIntervals[taskId]);
            delete taskIntervals[taskId];
        }

        fetch('/api/v1/tasks/' + taskId + '/state/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ completed: false })
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Undo failed');
                }
                markTaskUndone(taskId);
            })
            .catch(function () {});
    }

    function ensureTaskElement(data) {
        var existing = document.getElementById('task-' + data.task_id);
        if (existing) {
            return existing;
        }

        var taskWrapper = document.createElement('div');
        taskWrapper.className = 'box';
        taskWrapper.id = 'task-' + data.task_id;
        taskWrapper.dataset.categoryId = '';
        taskWrapper.innerHTML =
            '<article class="media">' +
            '  <div class="media-content">' +
            '    <div class="content">' +
            '      <h3 id="task-title-' + data.task_id + '"><strong>' + data.title + '</strong></h3>' +
            '    </div>' +
            '  </div>' +
            '  <div class="media-right">' +
            '    <a href="javascript:void(0);" id="complete-button-' + data.task_id + '" class="button is-success" onclick="completeTask(' + data.task_id + ');">' +
            '      <i class="fas fa-check"></i>' +
            '    </a>' +
            '  </div>' +
            '</article>';

        var section = document.querySelector('.section');
        if (section) {
            section.appendChild(taskWrapper);
        }
        return taskWrapper;
    }

    function setupWebSocket() {
        var wsScheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        var taskSocket = new WebSocket(wsScheme + window.location.host + '/ws/tasks/');

        taskSocket.onmessage = function (e) {
            var data = JSON.parse(e.data);
            if (data.action === 'created') {
                ensureTaskElement(data);
            } else if (data.action === 'completed') {
                markTaskCompleted(data.task_id);
            } else if (data.action === 'undone') {
                markTaskUndone(data.task_id);
            } else if (data.action === 'deleted') {
                var taskElement = document.getElementById('task-' + data.task_id);
                if (taskElement) {
                    taskElement.remove();
                }
            }
        };
    }

    window.completeTask = completeTask;
    window.undoCompleteTask = undoCompleteTask;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupWebSocket);
    } else {
        setupWebSocket();
    }
})();
