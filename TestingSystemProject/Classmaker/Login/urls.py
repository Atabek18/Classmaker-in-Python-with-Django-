from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "Login"

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]