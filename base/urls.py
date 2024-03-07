from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='list'),
    path('create_task', views.create_task, name='create_task'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('undo_complete_task/<int:task_id>/', views.undo_complete_task, name='undo_complete_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('uncategorized_tasks/', views.uncategorized_tasks, name='uncategorized_tasks'),
    path('save_category_for_task/', views.save_category_for_task, name='save_category_for_task'),

]
