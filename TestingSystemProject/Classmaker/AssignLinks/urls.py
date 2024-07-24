from django.urls import path
from . import views

app_name = "Assign"
urlpatterns = [
    path(
        "assign-test/settings/<int:test_id>/<slug:test_description>/",
        views.ShowLinks,
        name="showed-assign",
    ),
    path(
        "assign-test/edit/settings/<int:assign_id>/<slug:test_description>",
        views.ShowLinksEdit,
        name="edit-assign",
    ),
]
