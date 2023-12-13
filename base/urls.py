from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='list'),
    path('create_task', views.create_task, name='create_task'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('undo_complete_task/<int:task_id>/', views.undo_complete_task, name='undo_complete_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
]