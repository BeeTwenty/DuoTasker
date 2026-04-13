from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from apps.tasks import api as task_api


urlpatterns = [
    path('setup/', views.setup, name='setup'),
    path('', views.index, name='list'),
    path('create_task', views.create_task, name='create_task'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('undo_complete_task/<int:task_id>/', views.undo_complete_task, name='undo_complete_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('get_tasks/<int:category_id>/', views.get_tasks, name='get_tasks'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('uncategorized_tasks/', views.uncategorized_tasks, name='uncategorized_tasks'),
    path('save_category_for_task/', views.save_category_for_task, name='save_category_for_task'),

    # JSON API v1 (parallel interface for frontend migration).
    path('api/v1/tasks/', task_api.list_tasks_api, name='api_list_tasks'),
    path('api/v1/tasks/create/', task_api.create_task_api, name='api_create_task'),
    path('api/v1/tasks/<int:task_id>/state/', task_api.update_task_state_api, name='api_update_task_state'),
    path('api/v1/tasks/<int:task_id>/delete/', task_api.delete_task_api, name='api_delete_task'),

]
