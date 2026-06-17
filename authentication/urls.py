from django.urls import path

from .views import SignupView, LoginView, CurrentUserView

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", CurrentUserView.as_view()),
]