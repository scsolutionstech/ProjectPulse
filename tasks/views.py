from django.shortcuts import render, redirect
from .forms import TaskForm,TaskStatusForm
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.shortcuts import get_object_or_404
from tasks.models import Task
from django.contrib import messages




@login_required
def task_detail(request, pk):
    """
    View to display the details of a specific task.
    """
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def update_task_status(request, pk):
    """
    View to update the status of a specific task.
    """
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task status updated successfully!')
            return redirect('tasks:task_detail', pk=task.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskStatusForm(instance=task)
    
    return render(request, 'tasks/update_task_status.html', {'form': form, 'task': task})




@login_required
def create_task(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form, 'project': project})


@login_required
def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=task.project.pk)
    else:
        form = TaskStatusForm(instance=task)
    return render(request, 'tasks/update_task_status.html', {'form': form})
