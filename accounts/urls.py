from django.urls import path
from  accounts.views import CustomLoginView,RegisterView,ProfileView,LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  

]
