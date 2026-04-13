from dataclasses import dataclass
from typing import Optional

from base.models import Category, Task
from apps.tasks.categorization import resolve_category


@dataclass
class TaskCreationInput:
    title: str
    category_id: Optional[int] = None


class TaskService:
    """Service layer entrypoint for task lifecycle and categorization rules."""

    @staticmethod
    def _clean_title(title: str) -> str:
        return (title or "").strip()

    @staticmethod
    def _keyword_list(raw_keywords: Optional[str]) -> list[str]:
        if not raw_keywords:
            return []
        return [kw.strip() for kw in raw_keywords.split(',') if kw.strip()]

    @classmethod
    def _append_keyword_if_missing(cls, category: Category, keyword: str) -> None:
        keyword = cls._clean_title(keyword)
        if not keyword:
            return

        keywords = cls._keyword_list(category.keywords)
        if keyword.lower() in {item.lower() for item in keywords}:
            return

        keywords.append(keyword)
        category.keywords = ','.join(keywords)
        category.save(update_fields=['keywords'])

    @classmethod
    def _resolve_category_for_title(cls, title: str, category_id: Optional[int]) -> Optional[Category]:
        best_match = resolve_category(title, Category.objects.all())
        if best_match is not None:
            return best_match

        if category_id is None:
            return None
        return Category.objects.filter(id=category_id).first()

    @classmethod
    def create_task(cls, payload: TaskCreationInput) -> Task:
        title = cls._clean_title(payload.title)
        if not title:
            raise ValueError("Task title cannot be empty")

        category = cls._resolve_category_for_title(title, payload.category_id)
        return Task.objects.create(title=title, category=category)

    @staticmethod
    def mark_completed(task: Task) -> Task:
        if not task.completed:
            task.completed = True
            task.save(update_fields=['completed'])
        return task

    @staticmethod
    def mark_undone(task: Task) -> Task:
        if task.completed:
            task.completed = False
            task.save(update_fields=['completed'])
        return task

    @staticmethod
    def delete_task(task: Task) -> str:
        title = task.title
        task.delete()
        return title

    @classmethod
    def assign_task_category(cls, task: Task, category: Category, learn_keyword: bool = True) -> Task:
        if learn_keyword:
            cls._append_keyword_if_missing(category, task.title)

        task.category = category
        task.save(update_fields=['category'])
        return task

    @staticmethod
    def tasks_for_category(category_id: int):
        return Task.objects.filter(category_id=category_id).values('id', 'title', 'completed')
