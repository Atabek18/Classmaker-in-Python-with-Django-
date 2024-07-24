from django.urls import path
from . import views

app_name = "TestingSystem"
urlpatterns = [
    path("smth/", views.main, name="index"),
    path("test/", views.TestViews, name="tests"),
    path(
        "question/<int:test_id>/<slug:test_description>/",
        views.QuestionView,
        name="questions",
    ),
    path("test/test/new/", views.home, name="home"),
    path(
        "create-question/multiple/<int:test_id>/<slug:test_description>/",
        views.CreateQuestionAndMultpleOptions,
        name="create-multiple",
    ),
    path(
        "edit/multiple/<int:question_id>/<slug:question_description>/",
        views.EditQuestionAndMultpleOptions,
        name="question_edit_multiple",
    ),
    path(
        "edit/free-text/<int:question_id>/<slug:question_description>/",
        views.EditQuestionAndFreeTextOptions,
        name="question_edit_freetext",
    ),
    path(
        "edit/matching/<int:question_id>/<slug:question_description>/",
        views.EditQuestionAndMatchingOptions,
        name="question_edit_matching",
    ),
    path(
        "edit/true-false/<int:question_id>/<slug:question_description>/",
        views.EditQuestionAndTrueFalseOptions,
        name="question_edit_truefalse",
    ),
    path(
        "create-question/true-false/<int:test_id>/<slug:test_description>/",
        views.CreateQuestionAndTrueFalseOptions,
        name="create-true-false",
    ),
    path(
        "create-question/free-text/<int:test_id>/<slug:test_description>/",
        views.CreateQuestionAndFreeTextOptions,
        name="create-free-text",
    ),
    path(
        "create-question/matching/<int:test_id>/<slug:test_description>/",
        views.CreateQuestionAndMatchingOptions,
        name="create-matching",
    ),
    path("send/", views.send_email_view, name="send_email"),
    path("profile/", views.profile, name="profile-edit"),
    path("questions/db/", views.QuestionsView, name="questions-views"),
    path("links/db/", views.LinksView, name="links-views"),
    path("", views.Dashboard, name="dashboard"),
    path("statistic/statshome", views.StatsHome, name="statshome"),
    path("statistic/byLink", views.StatisticsByLinks, name="statisticByLink"),
    path("statistic/byTest", views.StatisticsByTest, name="statisticByTest"),
    path("webhook/", views.webhook_view, name="webhook"),
]
