from django.urls import path
from .views import signup_view, login_view, logout_view, profile_view, delete_profile_view, edit_profile_view



app_name = "accounts"

urlpatterns = [
     path("signup/", signup_view, name="signup"),
     path("login/", login_view, name="login"),
     path("logout/", logout_view, name="logout"),
     path("profile/<str:username>/", profile_view, name="profile"),
     path("profile/<str:username>/edit/", edit_profile_view, name="edit"),
     path("delete/", delete_profile_view, name="delete"),
     path("friends/profile/<str:username>/", profile_view, name="friend_profile"),
]


