from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


TASK_EVENT_GROUP = "task_list"
ALLOWED_TASK_ACTIONS = {"created", "completed", "undone", "deleted"}


def broadcast_task_event(task_id: int, action: str, title: str) -> bool:
    if action not in ALLOWED_TASK_ACTIONS:
        return False

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        TASK_EVENT_GROUP,
        {
            "type": f"task.{action}",
            "task_id": task_id,
            "action": action,
            "title": title,
        },
    )
    return True
