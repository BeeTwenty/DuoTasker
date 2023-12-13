# base/routing.py

from django.urls import re_path
from .consumers import TaskListConsumer

websocket_urlpatterns = [
    re_path(r'^ws/tasks/$', TaskListConsumer.as_asgi()),
]
