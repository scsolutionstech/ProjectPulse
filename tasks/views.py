from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from projects.models import Project

from tasks.models import Task

from .forms import TaskForm


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        comment_content = request.POST.get("comment")
        if comment_content:
            if task.comments:
                new_content = f"{task.content}\n{comment_content}"
            else:
                new_content = comment_content
            task.content = new_content
            task.save()
            return redirect("task_detail", pk=task.pk)

    return render(
        request,
        "tasks/task_details.html",
        {
            "task": task,
        },
    )


@login_required
def create_task(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("project_detail", pk=project.pk)
    else:
        form = TaskForm()
    return render(request, "tasks/create_task.html", {"form": form, "project": project})
