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
<<<<<<< HEAD
    path('unassigned-tasks/', views.unassigned_tasks, name='unassigned_tasks'),
    path('assign-category-to-task/', views.assign_to_category, name='assign_category_to_task'),
=======
    path('uncategorized_tasks/', views.uncategorized_tasks, name='uncategorized_tasks'),
    path('save_category_for_task/', views.save_category_for_task, name='save_category_for_task'),

>>>>>>> e97cf58452d26ab47a62e28af3b6da77ba011a73
]
