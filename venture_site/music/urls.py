from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("search/", views.home, name="home"),
    path("album/<str:album_id>/", views.album_detail, name="album_detail"),
    path("artist/<str:artist_id>/", views.artist_detail, name="artist_detail"),
    path("explore/", views.explore, name="explore"),
    path("explore/<str:genre_id>/", views.explore_genre, name="explore_genre"),
]