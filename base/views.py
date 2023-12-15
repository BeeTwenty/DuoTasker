from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
    tasks = Task.objects.all()
    return render(request, 'list.html', {'tasks': tasks})

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
        task = Task(title=title)
        task.save()
        send_task_update(task.id, 'created', task.title)
        return redirect('list')
    return render(request, 'list')

@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = True
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
