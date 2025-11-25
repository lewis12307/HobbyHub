from django.urls import path
from .views import friends_view, add_friend_view, search_friend_view, respond_friend_request_view, remove_friend_view



app_name = "friends"

urlpatterns = [
     path("", friends_view, name="friends"),
     path("add/search/", search_friend_view, name="search_friend"),
     path("add/", add_friend_view, name="add_friend"),
     path("respond_friend_request/", respond_friend_request_view, name="respond_friend_request"),
     path("remove_friend/", remove_friend_view, name="remove_friend"),
]