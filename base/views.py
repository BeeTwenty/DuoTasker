from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task, Category
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from celery import shared_task
from datetime import datetime
from celery.schedules import crontab
from datetime import timedelta


CELERY_BEAT_SCHEDULE = {
    'delete-completed-tasks': {
        'task': 'myapp.tasks.delete_completed_tasks',
        'schedule': timedelta(seconds=1),  # Run every second
    },
}

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def index(request):
    tasks = Task.objects.select_related('category').order_by('-category__is_important', 'title')
    categories = Category.objects.all().order_by('-is_important', 'name')
    uncategorized_tasks = Task.objects.filter(category__isnull=True)

    return render(request, 'list.html', {'tasks': tasks, 'categories': categories, 'uncategorized_tasks': uncategorized_tasks})

def send_task_update(task_id, action, task_title):
    channel_layer = get_channel_layer()
    # Determine the correct message type based on the action
    message_type = f"task.{action}"  # This will create 'task.created', 'task.completed', etc.
    async_to_sync(channel_layer.group_send)(
        "task_list",
        {
            "type": message_type,  # Send specific method type
            "task_id": task_id,
            "action": action,
            "title": task_title,
        },
    )

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category', None)  # Get category ID from the form

        # Attempt to auto-categorize the task based on title keywords, or use the selected category
        category = None  # Default to None if no category is found or selected
        all_categories = Category.objects.all()
        for cat in all_categories:
            if cat.keywords:
                keywords = [kw.strip().lower() for kw in cat.keywords.split(',')]
                if any(keyword == title.lower().strip() for keyword in keywords):
                    category = cat
                    break
        
        # If auto-categorization did not find a category, and a category was manually selected
        if not category and category_id:
            try:
                category = Category.objects.get(id=category_id)
            except (ValueError, Category.DoesNotExist):
                category = None  # If category_id is invalid or does not exist, default to None

        task = Task(title=title, category=category)
        task.save()
        send_task_update(task.id, 'created', task.title)
        return redirect('list')
    else:
        categories = Category.objects.all().order_by('-is_important', 'name')
        return render(request, 'create_task.html', {'categories': categories})


@shared_task
@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = True
        task.completed_at = timezone.now()
        task.save()
        send_task_update(task.id, 'completed', task.title)
        return JsonResponse({'status': 'success'})

@login_required
def undo_complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = False
        task.save()
        send_task_update(task.id, 'undone', task.title)
        return JsonResponse({'status': 'success'})

@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        send_task_update(task_id, 'deleted', task.title)
        return JsonResponse({'status': 'success'})
