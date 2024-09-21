from django.urls import path
from . import views


app_name = 'dashboard' 
urlpatterns = [
    path('', views.dashboards, name='dashboards'),
    path('', views.dashboard, name='dashboard'),
    path('search/', views.search_dashboard, name='search_dashboard'),

]
