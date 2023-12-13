from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task



def index(request):
    tasks = Task.objects.all()
    return render(request, 'list.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        task = Task(title=title)
        task.save()
        return redirect('list')
    return render(request, 'list')


def complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = True
        task.save()
        return JsonResponse({'status': 'success'})

def undo_complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = False
        task.save()
        return JsonResponse({'status': 'success'})

def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return JsonResponse({'status': 'success'})