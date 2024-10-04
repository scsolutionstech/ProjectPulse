from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_project, name="create_project"),
    path("<int:pk>/", views.project_detail, name="project_detail"),
    path("<int:pk>/", views.update_task_status, name="update_task_status"),
]
