from django.urls import path
from .views import signup_view, login_view, logout_view, profile_view, delete_user_view



app_name = "accounts"

urlpatterns = [
     path("signup/", signup_view, name="signup"),
     path("login/", login_view, name="login"),
     path("profile/<str:username>/", profile_view, name="profile"),
     path("logout/", logout_view, name="logout"),
     path("delete/", delete_user_view, name="delete"),
]