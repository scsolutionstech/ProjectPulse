from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.views import View
from django.contrib.auth import logout



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

def is_admin(user):
    return user.groups.filter(name='Administrator').exists()

@user_passes_test(is_admin)
def admin_view(request):
    # Admin-only view logic
    pass


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')