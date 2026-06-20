from django.urls import path

from .views import (
    ProjectListCreateView,
    ProjectDetailView,
    CollaboratorListView,
    InviteCollaboratorView,
    RemoveCollaboratorView
)

urlpatterns = [
    path("",ProjectListCreateView.as_view()),
    path("<int:pk>/",ProjectDetailView.as_view()),
    path("<int:project_id>/invite/",InviteCollaboratorView.as_view()),
    path("<int:project_id>/collaborators/",CollaboratorListView.as_view()),
    path("<int:project_id>/collaborators/<int:user_id>/",RemoveCollaboratorView.as_view()),
]