from django import forms
from django.contrib.auth import get_user_model
from tasks.models import Task, TaskStatus

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "team_members",
            "billable_status",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        User = get_user_model()
        self.fields["team_members"].queryset = User.objects.all()
        self.fields["team_members"].label_from_instance = lambda obj: obj.email


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskStatusForm, self).__init__(*args, **kwargs)
        self.fields["status"].choices = TaskStatus.choices()
        print(TaskStatus.choices())
