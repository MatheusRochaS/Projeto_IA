from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome_view, name="welcome"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("main", views.main, name="main"),
    path("catalogo", views.catalogo_geral, name="catalogo"),
    path("infos/<int:video_id>", views.infos, name="infos"),
    path("lista", views.lista_geral, name="lista"),
]