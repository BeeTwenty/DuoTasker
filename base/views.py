from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task, Category, SiteConfiguration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from .forms import SetupForm
from apps.tasks.services import TaskCreationInput, TaskService
from apps.tasks.background import schedule_delete_if_still_completed
from apps.realtime.events import broadcast_task_event


PREDEFINED_CATEGORIES = {
    'en': [
        {'name': 'Dairy', 'icon': 'fa-cheese', 'keywords': 'milk,cheese,butter,yogurt,cream,eggs'},
        {'name': 'Bakery', 'icon': 'fa-bread-slice', 'keywords': 'bread,roll,bun,flour,tortilla'},
        {'name': 'Produce', 'icon': 'fa-apple-whole', 'keywords': 'apple,banana,tomato,potato,onion,salad'},
        {'name': 'Meat and Fish', 'icon': 'fa-drumstick-bite', 'keywords': 'chicken,beef,pork,fish,salmon,tuna'},
        {'name': 'Pantry', 'icon': 'fa-box-open', 'keywords': 'rice,pasta,beans,lentils,sugar,salt,oil'},
    ],
    'nb': [
        {'name': 'Meieri', 'icon': 'fa-cheese', 'keywords': 'melk,ost,smor,yoghurt,flote,egg'},
        {'name': 'Bakeri', 'icon': 'fa-bread-slice', 'keywords': 'brod,rundstykke,bolle,mel,tortilla'},
        {'name': 'Frukt og Gront', 'icon': 'fa-apple-whole', 'keywords': 'eple,banan,tomat,potet,lok,salat'},
        {'name': 'Kjott og Fisk', 'icon': 'fa-drumstick-bite', 'keywords': 'kylling,storfe,svin,fisk,laks,tunfisk'},
        {'name': 'Basisvarer', 'icon': 'fa-box-open', 'keywords': 'ris,pasta,bonner,linser,sukker,salt,olje'},
    ],
}


def _get_site_configuration():
    return SiteConfiguration.objects.first()


def _seed_predefined_categories(language_code):
    for category_data in PREDEFINED_CATEGORIES.get(language_code, []):
        category, created = Category.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'icon': category_data['icon'],
                'keywords': category_data['keywords'],
            },
        )
        if not created:
            existing_keywords = [part.strip() for part in (category.keywords or '').split(',') if part.strip()]
            incoming_keywords = [part.strip() for part in category_data['keywords'].split(',') if part.strip()]
            for keyword in incoming_keywords:
                if keyword.lower() not in {value.lower() for value in existing_keywords}:
                    existing_keywords.append(keyword)
            category.keywords = ','.join(existing_keywords)
            category.save(update_fields=['keywords'])


def setup(request):
    configuration = _get_site_configuration()
    if configuration and configuration.setup_complete and User.objects.filter(is_superuser=True).exists():
        return redirect('list')

    if request.method == 'POST':
        form = SetupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.email = form.cleaned_data['email']
            user.save()

            configuration, _ = SiteConfiguration.objects.get_or_create(id=1)
            configuration.default_language = form.cleaned_data['default_language']
            configuration.default_timezone = form.cleaned_data['default_timezone']
            configuration.setup_complete = True
            configuration.save()

            if form.cleaned_data['add_predefined_categories']:
                _seed_predefined_categories(configuration.default_language)

            login(request, user)
            return redirect('list')
    else:
        form = SetupForm()

    return render(request, 'setup.html', {'form': form})

def register(request):
    configuration = _get_site_configuration()
    if not configuration or not configuration.setup_complete:
        return redirect('setup')

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
        return JsonResponse({'status': 'error', 'message': _('Method not allowed')}, status=405)

    task = get_object_or_404(Task, id=task_id)
    TaskService.mark_completed(task)
    schedule_delete_if_still_completed(task.id, delay_seconds=5)
    broadcast_task_event(task.id, 'completed', task.title)
    return JsonResponse({'status': 'success'})

@login_required
def undo_complete_task(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': _('Method not allowed')}, status=405)

    task = get_object_or_404(Task, id=task_id)
    TaskService.mark_undone(task)
    broadcast_task_event(task.id, 'undone', task.title)
    return JsonResponse({'status': 'success'})

@login_required
def delete_task(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': _('Method not allowed')}, status=405)

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