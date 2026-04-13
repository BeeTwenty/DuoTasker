from channels.generic.websocket import AsyncWebsocketConsumer
import json


class TaskListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("task_list", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("task_list", self.channel_name)

    async def _send_task_payload(self, event):
        await self.send(text_data=json.dumps({
            "task_id": event["task_id"],
            "action": event["action"],
            "title": event["title"],
        }))

    async def task_update(self, event):
        await self._send_task_payload(event)

    async def task_deleted(self, event):
        await self._send_task_payload(event)

    async def task_created(self, event):
        await self._send_task_payload(event)

    async def task_completed(self, event):
        await self._send_task_payload(event)

    async def task_undone(self, event):
        await self._send_task_payload(event)

    

