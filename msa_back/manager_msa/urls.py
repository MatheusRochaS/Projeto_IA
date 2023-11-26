from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome_view, name="welcome"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("main", views.main, name="main"),
    path("catalogo", views.catalogo_geral, name="catalogo"),
    path("infos/<int:video_id>/<str:type>", views.infos, name="infos"),
    path("lista/<int:user_id>", views.lista_geral, name="lista"),
    path("delete/<int:video_id>", views.delete_movie, name="delete-movie"),
    path("rating/<int:video_id>/movie/<int:rating>", views.rating_movie, name="rating-movie"),
    path('search', views.search, name='search'),
]