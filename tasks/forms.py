from django import forms
from django.contrib.auth import get_user_model

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "assigned_to",
            "priority",
            "due_date",
            "attachments",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        User = get_user_model()
        self.fields["assigned_to"].queryset = User.objects.all()
        self.fields["assigned_to"].label_from_instance = lambda obj: obj.email


class CommentForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "Add your comment here..."}
            ),
        }
