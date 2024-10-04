from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from accounts.forms import ProfileUpdateForm

from .forms import CustomLoginForm, CustomUserCreationForm
from .models import CustomUser


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            messages.success(
                request,
                f"Account created for {email}!  Please contact Administrator to activate your account.",
            )
            return redirect("login")
        return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        form = CustomLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_active:
                    messages.error(
                        request,
                        "Your account is not active. Please contact the Administrator.",
                    )
                    return render(request, self.template_name, {"form": form})
                if user.check_password(password):
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)

                messages.error(request, "Invalid password.")
            except CustomUser.DoesNotExist:
                messages.error(request, "A user with that email does not exist.")
        return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You are logged out successfully.")
        return redirect("login")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated!")
        return super().form_valid(form)

    def get_object(self):
        return self.request.user
