from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from tasks.models import Task


@login_required
def dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user).order_by("due_date")
    return render(request, "dashboard/dashboard.html", {"tasks": tasks})


@login_required
def dashboards(request):
    tasks = Task.objects.filter(assigned_to=request.user).order_by("due_date")
    overdue_tasks = tasks.filter(
        due_date__lt=timezone.now(), status__in=["todo", "in_progress"]
    )
    return render(
        request,
        "dashboard/dashboard.html",
        {"tasks": tasks, "overdue_tasks": overdue_tasks},
    )


@login_required
def search_dashboards(request):
    try:
        query = request.GET.get("q", "").strip()
        status_filter = request.GET.get("status", "").strip()
        tasks = Task.objects.filter(assigned_to=request.user)

        if query:
            tasks = tasks.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        if status_filter:
            tasks = tasks.filter(status=status_filter)

        today = timezone.now().date()
        overdue_tasks = tasks.filter(
            due_date__lt=today, status__in=["todo", "in_progress"]
        )

        # paginator = Paginator(tasks, 10)  # Show 10 tasks per page
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)

        return render(
            request,
            "dashboard/dashboard.html",
            {
                "tasks": tasks,
                "overdue_tasks": overdue_tasks,
                "search_query": query,
                "status_filter": status_filter,
            },
        )
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


@login_required
def search_dashboard(request):
    return dashboard(request)
