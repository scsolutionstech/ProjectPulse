from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('create/<int:project_pk>/', views.create_task, name='create_task'),
    path('update_status/<int:pk>/', views.update_task_status, name='update_task_status'),
]
