from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from apps.tasks.services import TaskCreationInput, TaskService
from apps.tasks.background import schedule_delete_if_still_completed
from apps.realtime.events import broadcast_task_event

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

@login_required
def create_task(request):
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        if not title:
            return redirect('list')

        category_id = request.POST.get('category') or None
        payload = TaskCreationInput(title=title, category_id=int(category_id) if category_id else None)
        task = TaskService.create_task(payload)
        broadcast_task_event(task.id, 'created', task.title)
        return redirect('list')
    else:
        categories = Category.objects.all().order_by('-is_important', 'name')
        return render(request, 'create_task.html', {'categories': categories})


@login_required
def complete_task(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    task = get_object_or_404(Task, id=task_id)
    TaskService.mark_completed(task)
    schedule_delete_if_still_completed(task.id, delay_seconds=5)
    broadcast_task_event(task.id, 'completed', task.title)
    return JsonResponse({'status': 'success'})

@login_required
def undo_complete_task(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    task = get_object_or_404(Task, id=task_id)
    TaskService.mark_undone(task)
    broadcast_task_event(task.id, 'undone', task.title)
    return JsonResponse({'status': 'success'})

@login_required
def delete_task(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    task = get_object_or_404(Task, id=task_id)
    task_title = TaskService.delete_task(task)
    broadcast_task_event(task_id, 'deleted', task_title)
    return JsonResponse({'status': 'success'})


@login_required
def uncategorized_tasks(request):
    tasks = Task.objects.filter(category__isnull=True)
    categories = Category.objects.all()

    return render(request, 'uncategorized_tasks.html', {
        'tasks': tasks,
        'categories': categories,
    })

@login_required
def save_category_for_task(request):
    if request.method != 'POST':
        return redirect('uncategorized_tasks')

    for key, value in request.POST.items():
        if not key.startswith('category_for_task_'):
            continue

        task_id = key.split('_')[-1]
        category_id = value
        if not task_id or not category_id:
            continue

        try:
            task = Task.objects.get(id=task_id)
            category = Category.objects.get(id=category_id)
        except (Task.DoesNotExist, Category.DoesNotExist):
            continue

        TaskService.assign_task_category(task, category, learn_keyword=True)

    return redirect('uncategorized_tasks')


@login_required
def get_tasks(request, category_id):
    tasks = TaskService.tasks_for_category(category_id)
    return JsonResponse({'tasks': list(tasks)})