from django.urls import path
from .views import UserScoreResults, score
app_name = 'UserScore'
urlpatterns = [
    path('score/<int:user_id>/<slug:assign_slug>', UserScoreResults, name='score'),
    path('email/result/<int:user_id>/<slug:assign_slug>', score, name='results'),
]   