from django.shortcuts import redirect,render
from collaboration.models import Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from tasks.models import Task

@login_required
def add_comment(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('task_detail', pk=task_pk)
    else:
        form = CommentForm()
    return render(request, 'collaboration/add_comment.html', {'form': form})
