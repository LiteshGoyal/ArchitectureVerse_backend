from django.urls import path

from .views import ReviewArchitectureView, GenerateArchitectureView, ExplainArchitectureView, ArchitectureChatView, ChatHistoryView, ImproveArchitectureView, ReviewHistoryView

urlpatterns=[
    path("review/",ReviewArchitectureView.as_view()),
    path("generate/",GenerateArchitectureView.as_view()),
    path("explain/",ExplainArchitectureView.as_view()),
    path("chat/",ArchitectureChatView.as_view()),
    path("history/<int:project_id>/",ChatHistoryView.as_view()),
    path("improve/",ImproveArchitectureView.as_view()),
    path("reviews/<int:project_id>/",ReviewHistoryView.as_view()),
]