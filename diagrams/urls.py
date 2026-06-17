from django.urls import path
from .views import DiagramView, ShareDiagramView, PublicDiagramView

urlpatterns = [
    path("projects/<int:project_id>/diagram/",DiagramView.as_view()),
     path(
        "projects/<int:project_id>/share/",
        ShareDiagramView.as_view(),
    ),

    path(
        "share/<uuid:share_id>/",
        PublicDiagramView.as_view(),
    ),
]