from django.urls import path
from .views import (
    answer_question_view,
    previews_questions,
    # registration_view,
    # init_test,
    # start_test,
    index
)

app_name = "UserResponse"
urlpatterns = [
    path(
        "start/online-test/<slug:assign_slug>/",
        answer_question_view,
        name="responses",
    ),
    path("previews/online-test/<int:test_id>/", previews_questions, name="preview"),
    path('index', index, name='index')
]
