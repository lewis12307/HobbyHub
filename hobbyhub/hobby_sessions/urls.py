from django.urls import path
from django.shortcuts import redirect

from .views import create_session_view, delete_session_view



app_name = "hobby_sessions"

urlpatterns = [
     path("hobbies/<str:hobby_name>/sessions", lambda request, hobby_name: redirect("hobbies:hobby_detail", name=hobby_name)),
     path("hobbies/<str:hobby_name>/sessions/add/", create_session_view, name="create_session"),
     path("hobbies/<str:hobby_name>/sessions/<int:session_id>/delete/", delete_session_view, name="delete_session"),
]