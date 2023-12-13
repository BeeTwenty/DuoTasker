from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


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

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        task = Task(title=title)
        task.save()
        return redirect('list')
    return render(request, 'list')

@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = True
        task.save()
        return JsonResponse({'status': 'success'})
@login_required
def undo_complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = False
        task.save()
        return JsonResponse({'status': 'success'})
@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return JsonResponse({'status': 'success'})