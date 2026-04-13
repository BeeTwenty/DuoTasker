from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
import json
from django.test import TransactionTestCase, override_settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from unittest.mock import patch

from .models import Category, Task
from apps.tasks.services import TaskCreationInput, TaskService
from apps.realtime.events import broadcast_task_event
from DuoTasker.asgi import application


class CategoryModelTest(TestCase):
    def test_str_returns_name(self):
        category = Category.objects.create(name="Home", icon="home")
        self.assertEqual(str(category), "Home")


class TaskModelTest(TestCase):
    def test_create_task_with_category(self):
        category = Category.objects.create(name="Work", icon="briefcase")
        task = Task.objects.create(title="Finish report", category=category)
        self.assertEqual(str(task), "Finish report")
        self.assertEqual(task.category, category)


class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.client.login(username='tester', password='secret123')

    def test_complete_task_schedules_async_delete(self):
        task = Task.objects.create(title='Async window task')

        with patch('base.views.schedule_delete_if_still_completed') as mocked_schedule, patch(
            'base.views.broadcast_task_event'
        ) as mocked_broadcast:
            response = self.client.post(reverse('complete_task', args=[task.id]))

        self.assertEqual(response.status_code, 200)
        mocked_schedule.assert_called_once_with(task.id, delay_seconds=5)
        mocked_broadcast.assert_called_once_with(task.id, 'completed', task.title)

    def test_get_tasks_endpoint_returns_category_tasks(self):
        category = Category.objects.create(name="Work", icon="briefcase")
        Task.objects.create(title="Task A", category=category)
        Task.objects.create(title="Task B", category=category)
        Task.objects.create(title="Task C", category=None)

        response = self.client.get(reverse('get_tasks', args=[category.id]))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn('tasks', payload)
        self.assertEqual(len(payload['tasks']), 2)

    def test_save_category_for_task_updates_task_and_deduplicates_keywords(self):
        category = Category.objects.create(name="Home", icon="house", keywords="Buy milk")
        task = Task.objects.create(title="Buy milk")

        response = self.client.post(
            reverse('save_category_for_task'),
            {
                f'category_for_task_{task.id}': str(category.id),
            },
        )

        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        category.refresh_from_db()
        self.assertEqual(task.category_id, category.id)
        self.assertEqual(category.keywords, "Buy milk")


class TaskServiceTest(TestCase):
    def test_create_task_auto_matches_category_by_keyword(self):
        category = Category.objects.create(name="Home", icon="house", keywords="Wash dishes")

        created = TaskService.create_task(TaskCreationInput(title="Wash dishes"))

        self.assertEqual(created.category_id, category.id)

    def test_create_task_auto_matches_category_by_phrase_containment(self):
        category = Category.objects.create(name="Groceries", icon="cart", keywords="Buy milk")

        created = TaskService.create_task(TaskCreationInput(title="Buy milk and bread"))

        self.assertEqual(created.category_id, category.id)

    def test_create_task_prefers_more_specific_keyword_match(self):
        Category.objects.create(name="General", icon="note", keywords="Buy")
        specific = Category.objects.create(name="Groceries", icon="cart", keywords="Buy milk")

        created = TaskService.create_task(TaskCreationInput(title="Buy milk tonight"))

        self.assertEqual(created.category_id, specific.id)

    def test_create_task_matches_multilanguage_keyword(self):
        category = Category.objects.create(name="Dairy", icon="cart", keywords="milk, melk")

        created = TaskService.create_task(TaskCreationInput(title="melk"))

        self.assertEqual(created.category_id, category.id)

    def test_create_task_matches_accent_folded_keyword(self):
        category = Category.objects.create(name="Bakery", icon="bread", keywords="brod")

        created = TaskService.create_task(TaskCreationInput(title="brød"))

        self.assertEqual(created.category_id, category.id)

    def test_create_task_uses_builtin_statistical_match_from_existing_items(self):
        dairy = Category.objects.create(name="Dairy", icon="cart", keywords="milk, melk")
        Category.objects.create(name="Bakery", icon="bread", keywords="bread, brod")
        Task.objects.create(title="yoghurt naturell", category=dairy)

        created = TaskService.create_task(TaskCreationInput(title="gresk yoghurt"))

        self.assertEqual(created.category_id, dairy.id)

    def test_assign_task_category_adds_keyword_once(self):
        category = Category.objects.create(name="Work", icon="briefcase", keywords="Daily standup")
        task = Task.objects.create(title="Daily standup")

        TaskService.assign_task_category(task, category, learn_keyword=True)
        TaskService.assign_task_category(task, category, learn_keyword=True)

        category.refresh_from_db()
        self.assertEqual(category.keywords, "Daily standup")


class TaskApiTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='api-user', password='secret123')
        self.client.login(username='api-user', password='secret123')

    def test_api_create_and_list_tasks(self):
        category = Category.objects.create(name="Errands", icon="cart")
        with patch('apps.tasks.api.broadcast_task_event') as mocked_broadcast:
            create_response = self.client.post(
                reverse('api_create_task'),
                data=json.dumps({"title": "Buy apples", "category_id": category.id}),
                content_type='application/json',
            )

        self.assertEqual(create_response.status_code, 201)
        mocked_broadcast.assert_called_once()
        list_response = self.client.get(reverse('api_list_tasks'))
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()['tasks']), 1)

    def test_api_update_task_state(self):
        task = Task.objects.create(title="Draft summary")

        with patch('apps.tasks.api.broadcast_task_event') as mocked_broadcast, patch(
            'apps.tasks.api.schedule_delete_if_still_completed'
        ) as mocked_schedule:
            response = self.client.post(
                reverse('api_update_task_state', args=[task.id]),
                data=json.dumps({"completed": True}),
                content_type='application/json',
            )

        self.assertEqual(response.status_code, 200)
        mocked_schedule.assert_called_once_with(task.id, delay_seconds=5)
        mocked_broadcast.assert_called_once_with(task.id, 'completed', task.title)
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_api_delete_task(self):
        task = Task.objects.create(title="Remove me")

        with patch('apps.tasks.api.broadcast_task_event') as mocked_broadcast:
            response = self.client.post(reverse('api_delete_task', args=[task.id]))

        self.assertEqual(response.status_code, 200)
        mocked_broadcast.assert_called_once_with(task.id, 'deleted', 'Remove me')
        self.assertFalse(Task.objects.filter(id=task.id).exists())


class RealtimeEventTest(TestCase):
    def test_invalid_action_is_rejected(self):
        self.assertFalse(broadcast_task_event(1, 'invalid-action', 'Task'))


@override_settings(
    CHANNEL_LAYERS={
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }
)
class RealtimeWebsocketTest(TransactionTestCase):
    def test_websocket_receives_broadcast_event(self):
        from channels.testing.websocket import WebsocketCommunicator

        async def scenario():
            communicator = WebsocketCommunicator(application, '/ws/tasks/')
            connected, _ = await communicator.connect()
            self.assertTrue(connected)

            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                'task_list',
                {
                    'type': 'task.created',
                    'task_id': 123,
                    'action': 'created',
                    'title': 'Realtime task',
                },
            )

            payload = await communicator.receive_json_from(timeout=1)
            self.assertEqual(payload['task_id'], 123)
            self.assertEqual(payload['action'], 'created')
            self.assertEqual(payload['title'], 'Realtime task')
            await communicator.disconnect()

        async_to_sync(scenario)()

