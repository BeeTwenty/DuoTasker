import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from base.models import Task
from apps.realtime.events import broadcast_task_event
from apps.tasks.background import schedule_delete_if_still_completed
from apps.tasks.services import TaskCreationInput, TaskService


def _json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return {}


@login_required
@require_http_methods(["GET"])
def list_tasks_api(request):
    queryset = Task.objects.select_related("category").order_by("-category__is_important", "title")
    category_id = request.GET.get("category_id")
    completed = request.GET.get("completed")

    if category_id:
        queryset = queryset.filter(category_id=category_id)

    if completed in {"true", "false"}:
        queryset = queryset.filter(completed=(completed == "true"))

    tasks = [
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "category_id": task.category_id,
            "category_name": task.category.name if task.category else None,
        }
        for task in queryset
    ]
    return JsonResponse({"tasks": tasks})


@login_required
@require_http_methods(["POST"])
def create_task_api(request):
    payload = _json_body(request)
    title = (payload.get("title") or "").strip()
    if not title:
        return JsonResponse({"status": "error", "message": "title is required"}, status=400)

    category_id = payload.get("category_id")
    task = TaskService.create_task(
        TaskCreationInput(title=title, category_id=int(category_id) if category_id else None)
    )
    broadcast_task_event(task.id, "created", task.title)
    return JsonResponse(
        {
            "status": "success",
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "category_id": task.category_id,
            },
        },
        status=201,
    )


@login_required
@require_http_methods(["POST"])
def update_task_state_api(request, task_id):
    payload = _json_body(request)
    if "completed" not in payload:
        return JsonResponse({"status": "error", "message": "completed is required"}, status=400)

    task = get_object_or_404(Task, id=task_id)
    completed = bool(payload.get("completed"))
    if completed:
        TaskService.mark_completed(task)
        schedule_delete_if_still_completed(task.id, delay_seconds=5)
        broadcast_task_event(task.id, "completed", task.title)
    else:
        TaskService.mark_undone(task)
        broadcast_task_event(task.id, "undone", task.title)

    return JsonResponse({"status": "success", "task": {"id": task.id, "completed": task.completed}})


@login_required
@require_http_methods(["POST", "DELETE"])
def delete_task_api(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task_title = TaskService.delete_task(task)
    broadcast_task_event(task_id, "deleted", task_title)
    return JsonResponse({"status": "success", "task_id": task_id})
