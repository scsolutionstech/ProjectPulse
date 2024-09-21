from django.shortcuts import render, redirect
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from projects.models import Project
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.project_manager = request.user
            project.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})
