from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication Routes
    path('', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Task Routes (require login)
    path('tasks', views.task_list, name='task_list'),
    path('filter/<str:filter_type>/', views.task_list, name='filtered_tasks'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('update-task-completion/', views.update_task_completion, name='update_task_completion'),
    path('filter/<str:filter_type>/', views.filtered_tasks, name='filtered_tasks'),
]
