from django.urls import path

from . import views

urlpatterns = [
    path("task<int:pk>/", views.task_detail, name="task_detail"),
    path("create/<int:project_pk>/", views.create_task, name="create_task"),
]
