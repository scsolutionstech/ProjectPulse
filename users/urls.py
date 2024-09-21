from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users.views import logout_view


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

    # Add your URL patterns here
]
