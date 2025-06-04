from django.test import TestCase

from .models import Category, Task


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

