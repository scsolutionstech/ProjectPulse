from django.urls import path

from accounts.views import CustomLoginView, LogoutView, ProfileUpdateView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
]
