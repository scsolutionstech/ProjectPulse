from accounts.models import UserRole
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from tasks.models import Task

from projects.models import Project

from .forms import ProjectForm, TaskStatusForm


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.project_manager = request.user
            project.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect("project_detail", pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, "projects/create_project.html", {"form": form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    progress = project.progress(request.user)  # Calculate progress based on user

    user_role = getattr(request.user, "role", None)

    if user_role == UserRole.TEAM_MEMBER:
        tasks = project.tasks.filter(assigned_to=request.user)
    else:
        tasks = project.tasks.all()
    return render(
        request,
        "projects/project_detail.html",
        {"project": project, "tasks": tasks, "progress": progress},
    )


def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task status updated successfully!")
            return redirect("project_detail", pk=task.project.pk)
    else:
        form = TaskStatusForm(instance=task)

    context = {
        "task": task,
        "form": form,
    }
    return render(request, "projects/project_detail.html", context)
