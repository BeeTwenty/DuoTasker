from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TaskListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("task_list", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("task_list", self.channel_name)

    async def task_update(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            "task_id": event["task_id"],
            "action": event["action"],
            "title": event["title"],

    
        }))

    async def task_deleted(self, event):
        # Handle the 'deleted' action here and update the UI
        await self.send(text_data=json.dumps({
            "task_id": event["task_id"],
            "action": event["action"],
            "title": event["title"],
        }))

    async def task_created(self, event):
        # Handle the 'created' action here and update the UI
        await self.send(text_data=json.dumps({
            "task_id": event["task_id"],
            "action": event["action"],
            "title": event["title"],
        }))

    async def task_completed(self, event):
        # Handle the 'completed' action here and update the UI
        await self.send(text_data=json.dumps({
            "task_id": event["task_id"],
            "action": event["action"],
            "title": event["title"],
        }))

    async def task_undone(self, event):
        # Handle the 'undone' action here and update the UI
        await self.send(text_data=json.dumps({
            "task_id": event["task_id"],
            "action": event["action"],
            "title": event["title"],
        }))

    

