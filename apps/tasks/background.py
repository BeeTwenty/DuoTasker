from celery import shared_task

from base.models import Task
from apps.realtime.events import broadcast_task_event


@shared_task
def delete_task_if_still_completed(task_id: int) -> None:
    task = Task.objects.filter(id=task_id).first()
    if not task or not task.completed:
        return

    title = task.title
    task.delete()
    broadcast_task_event(task_id, "deleted", title)


def schedule_delete_if_still_completed(task_id: int, delay_seconds: int = 5) -> None:
    # In environments without a running broker this should not break request flow.
    try:
        delete_task_if_still_completed.apply_async(args=[task_id], countdown=delay_seconds)
    except Exception:
        return
