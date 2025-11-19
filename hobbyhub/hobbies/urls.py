from django.urls import path

from .views import create_hobby_view, hobby_detail_view, delete_hobby_view, hobbies_view




app_name = "hobbies"

urlpatterns = [
     path("", hobbies_view, name="hobbies"),
     path("create/", create_hobby_view, name="create_hobby"),
     path("<str:name>/", hobby_detail_view, name="hobby_detail"),
     path("<str:name>/delete/", delete_hobby_view, name="delete_hobby"),
]