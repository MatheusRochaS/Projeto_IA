from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome_view, name="welcome"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
]