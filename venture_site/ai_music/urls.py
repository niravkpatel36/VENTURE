from django.urls import path
from . import views

urlpatterns = [
    path("", views.ai_music_page, name="ai_music"),
    path("api/generate/", views.ai_generate_api, name="ai_generate_api"),
]
