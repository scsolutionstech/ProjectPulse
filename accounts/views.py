from django.shortcuts import redirect,render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CustomUserCreationForm,CustomLoginForm
from django.views import View
from .models import CustomUser
from django.contrib.auth import login
from django.conf import settings
from django.contrib import messages






class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

def is_admin(user):
    return user.groups.filter(name='Administrator').exists()

@user_passes_test(is_admin)
def admin_view(request):
    # Admin-only view logic
    pass


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!  Please contact Administrator to activate your account.')
            return redirect('login')
        else:
            return render(request, 'accounts/register.html', {'form': form})



class CustomLoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = CustomLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_active:
                    messages.error(request, 'Your account is not active. Please contact the Administrator.')
                    return render(request, self.template_name, {'form': form})
                if user.check_password(password):
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL) 
                 
                else:
                    messages.error(request, 'Invalid password.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'A user with that email does not exist.')
        return render(request, self.template_name, {'form': form})
    

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You are logged out successfully.")
        return redirect("login")