# tasks/urls.py
from django.urls import path
from .views import (
    UserINFOListAPIView,
    StartListAPIView,
    InitTestListAPIView,
    ContinueListAPIView,
)
from .views import get_csrf_token


app_name = "API_TEST"

urlpatterns = [
    path("user-register", UserINFOListAPIView.as_view(), name="user_info"),
    path("start/", StartListAPIView.as_view(), name="test_in_progress"),
    path("init_test/", InitTestListAPIView.as_view(), name="init_test"),
    path("continue/", ContinueListAPIView.as_view(), name="continue"),
]

urlpatterns += [
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
]   

