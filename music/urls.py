# music/urls.py
from django.urls import path
from . import views

app_name = "music"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("search/", views.home, name="home"),
    path("album/<str:album_id>/", views.album_detail, name="album_detail"),
    path("artist/<str:artist_id>/", views.artist_detail, name="artist_detail"),
    path("explore/", views.explore, name="explore"),
    path("explore/<str:genre_id>/", views.explore_genre, name="explore_genre"),
    path("generate/", views.generate, name="generate"),
    # AI Studio (single coherent route)
    path("ai/", views.ai_view, name="ai_view"),
    path("ai/api/generate/", views.ai_generate_api, name="ai_generate_api"),
    path("album/", views.author_album, name="author_album"),
]
