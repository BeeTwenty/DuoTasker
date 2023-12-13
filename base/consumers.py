from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TaskListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("task_list", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("task_list", self.channel_name)

    async def receive(self, text_data):
        # Handle messages received from the WebSocket
        pass

    async def task_message(self, event):
        # Call this to send a message to the group
        await self.send(text_data=json.dumps(event["text"]))