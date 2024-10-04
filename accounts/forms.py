# accounts/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="Required. Enter a valid email address."
    )

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control {existing_classes}"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


# login form
class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        label="Password",
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["profile_picture", "email"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "profile_picture": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }
